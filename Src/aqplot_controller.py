import sys
import threading
import serial
import serial.tools.list_ports
from aqplot_model import Model
from aqplot_view import *
from asammdf.gui.widgets.plot import Plot
import csv


class Controller:
    def __init__(self):
        self.app = QtWidgets.QApplication([])

        self.model = Model()
        self.serial = SerThread("AqPlot", self.model)
        self.view = View(QtWidgets.QMainWindow())

        self.view.open_meas_butt.clicked.connect(self.open_and_load_meas_file)
        self.view.clr_scr.clicked.connect(self.clear_graph)
        self.view.signal_list_box.itemSelectionChanged.connect(self.add_signal_to_plot)
        self.view.openFileAction_menubar.triggered.connect(self.open_and_load_meas_file)
        self.view.opendspAction_menubar.triggered.connect(self.open_and_load_dsp_file)
        self.view.exitAction_menubar.triggered.connect(self._quit)
        self.view.sel_com_combo_box.activated[str].connect(self.c_serial_select_com_port)
        self.view.sel_baudR_combo_box.activated[str].connect(self.c_serial_select_baud_rate)
        self.view.fill_up_baud_rate_list()

        self.view.connect_butt.clicked.connect(self.c_serial_open_close_connection)
        self.view.refresh_com_butt.clicked.connect(self.c_serial_get_host_com_ports)
        self.view.run_meas_butt.clicked.connect(self.c_serial_run_measurement)

    def run(self):
        self.serial.start()
        self.app.exec()



    '''
    Following methods command the 
    - measurement loading and prepare for plot
    - plot sinagls to graph
    - other settings for plotter
    '''
    def open_and_load_meas_file(self):
        file_name = self.view.open_file_dialog("*.mf4;*.csv")
        import_status = self.model.import_signals(file_name)

        if import_status == "empty_file":
            self.view.msg_box("Error", "The file is empty")
        elif import_status == "no_data":
            self.view.msg_box("Error", "The measurement has no data")
        else:
            self.view.fill_up_signal_list(self.model.signal_names)
            #self.aq_plot(self.model.signals)

    def open_and_load_dsp_file(self):
        file_name = self.view.open_file_dialog("*.txt")
        import_status = self.model.import_signal_info(file_name)

        if import_status == "empty_file":
            self.view.msg_box("Error", "The file is empty")
        elif import_status == "no_data":
            self.view.msg_box("Error", "The measurement has no data")
        else:
            pass

    def aq_plot(self, data):
        self.view.graphicsView.plot(data, pen='g')
        #self.view.plot.plot.add_new_channels(data)

    def add_signal_to_plot(self):
        selected_signal = self.view.signal_list_box.selectedItems()
        for signal in selected_signal:
            self.aq_plot(self.model.meas_data[signal.text()])
        #self.aq_plot(self.model.signals)


    def clear_graph(self):
        self.view.graphicsView.clear()

    '''
    This will handle the serial connection
    - configuration of port
    - controll the measurement start/stop
    '''

    def c_serial_get_host_com_ports(self):
            ports = self.serial.list_comports()
            if not ports:
                self.view.fill_up_COM_list(["No ports available"])
            else:
                port_list = []
                for port, desc, hwid in sorted(ports):
                    port_list.append(port)
                self.view.fill_up_COM_list(port_list)

    def c_serial_select_com_port(self, port):
        '''
        This method shall be used to send the selected port
        to the serial driver
        '''
        self.serial.set_port(port)

    def c_serial_select_baud_rate(self, baudrate):
        '''
        This method shall be used to send the selected port
        to the serial driver
        '''
        if baudrate != "Select Baude rate":
            self.serial.set_baud(baudrate)

    def c_serial_run_measurement(self):
        status = self.serial.serial_run_measurement()
        if status is "run":
            self.view.run_meas_butt.setText(self.view._translate("MainWindow", "Stop \n Measurement"))
        elif status is "stop":
            self.view.run_meas_butt.setText(self.view._translate("MainWindow", "Run \n Measurement"))
        else:
            self.view.msg_box("Error", "No connection established\nAbort")

    def c_serial_open_close_connection(self):
        serial_status = self.serial.serial_connection_control()
        if serial_status is "serial_open":
            self.view.connect_butt.setText(self.view._translate("MainWindow", "Disconnect"))
        elif serial_status is "serial_close":
            self.view.connect_butt.setText(self.view._translate("MainWindow", "Connect"))
        elif serial_status is "serial_error_access_denied":
            self.view.msg_box("Error", "Acces Denied To COM")
        elif serial_status is "error_unknown":
            self.view.msg_box("Error", "Could not connect\n\nHint:\n-check the COM\n-port in use")

    def c_serial_end_meas_clbk(self):

        """this will be called by the time the serial thread stopped the measurement
        Or, should it be more ok to have a clbk every time a pack has arrived?"""

        pass

    def _quit(self):
        get_user_ans = self.view.pop_up_on_exit()
        if get_user_ans == QtWidgets.QMessageBox.Yes:
            sys.exit()
        else :
            pass


class SerThread(threading.Thread):
    def __init__(self, thread_name, model):
        super(SerThread, self).__init__()
        self.name = thread_name
        self.model = model
        self.ser = serial.Serial()
        self.com_port_list = []

        """Das state machine bones"""
        self.DasState = 'StandBy'
        self.DASHandler = { 'StandBy'    : self.DAS_State_StandBy,
                            'StartOfMeas': self.DAS_State_StartOfMeas,
                            'ReceiveData': self.DAS_State_ReceiveData,
                            'StopMeas'   : self.DAS_State_StopMeas}

        self.commands = {'Cmd_StartMeas': chr(0x31).encode(),
                         'Cmd_StopMeas' : chr(0x30).encode()}

        self.input_pack_size = 16
    # gets called when thread is started with .start()
    def run(self):
        while True:
            self.com_port_list = serial.tools.list_ports.comports()
            if self.ser.is_open:
                '''DAS state machine handler '''
                self.DASHandler[self.DasState]()

    def serial_connection_control(self):
        if self.ser.is_open:
            self.ser.close()
            return "serial_close"
        else:
            try:
                self.ser.open()
                return "serial_open"
            except PermissionError:
                return "serial_error_access_denied"
            except:
                return "error_unknown"

    def serial_run_measurement(self):
        if self.ser.is_open:
            if self.DasState is 'StandBy':
                self.DasState = 'StartOfMeas'
                return "run"
            elif self.DasState is not 'StandBy':
                self.DasState = 'StopMeas'
                return "stop"
        else:
            return "not_connected"

    def serial_tx(self, ch):
        self.ser.write(ch)

    def serial_rx(self, nr_of_bytes):
        while self.ser.inWaiting() >= nr_of_bytes:
            ecu_pack = []
            line = self.ser.read(nr_of_bytes)
            for char in line:
                ecu_pack.append(char)
            ecu_pack[9] = self.ser.inWaiting()
            '''send data to model for processing'''
            self.model.get_pack_from_ecu(ecu_pack)

            #ecu_pack[4] = ecu_pack[0]
            #ecu_pack[0] = ecu_pack[11] | (ecu_pack[12] << 8) | (ecu_pack[13] << 16) | (ecu_pack[14] << 24)  # 200 us cnt
            #ecu_pack[1] = ecu_pack[1] | (ecu_pack[2] <<8) #dma isr cnt
            #ecu_pack[2] = self.ser.inWaiting()
            #ecu_pack[3] = ecu_pack[3] | (ecu_pack[4] <<8) #ring buff cnt
            #ecu_pack[5] = ecu_pack[5] | (ecu_pack[6] << 8)  # head real
            #ecu_pack[6] = ecu_pack[7] | (ecu_pack[8] << 8)  # tail real
            #ecu_pack[7] = self.loop_cnt
            #ecu_pack[8] = 0
            #ecu_pack[14] = 0
            #ecu_pack[11] = 0
            #ecu_pack[12] = 0
            #ecu_pack[13] = 0
            #self.csv_out.writerow(ecu_pack)


    def serial_reset_port_buffers(self):
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()

    def set_port(self, port):
        self.ser.setPort(port)

    def set_baud(self, baud):
        self.ser.baudrate = baud

    def list_comports(self):
        return self.com_port_list

    """State machine methods for states"""

    def DAS_State_StandBy(self):
        """
            This is a dummy state.
            Start will come from GUI
        """
        pass

    def DAS_State_StartOfMeas(self):
        print("start of meas")

        """ temporary data output too meas file
        Latter this will be send to controller and next to model"""
        #self.f = open('../TestManager/output_test.csv', 'w+')
        #self.name_list = ['Time',
        #                  'DmaLoopsCnt',
        #                  'Bytes InWaiting',
        #                  'ring buffer Cnt real',
        #                  'header',
        #                  'head real',
        #                  'tail real',
        #                  'ser rx loops',
        #                  'byte8',
        #                  'byte9',
        #                  'TessDasStates',
        #                  'byte11','byte12','byte13', 'byte14','footer']

        #self.csv_out = csv.writer(self.f, dialect='excel')
        #self.csv_out.writerow(self.name_list)

        self.serial_tx(self.commands['Cmd_StartMeas'])
        self.DasState = 'ReceiveData'

    def DAS_State_ReceiveData(self):
        self.serial_rx(self.input_pack_size)


    def DAS_State_StopMeas(self):
        self.serial_tx(self.commands['Cmd_StopMeas'])
        self.model.save_measurement()
        #self.f.close()


        # reconfigure port to flush all data from buffers
        # this way the next run data will be all new
        self.ser.close()
        self.ser.open()
        print("stop of meas")
        self.DasState = 'StandBy'


if __name__ == '__main__':
    C = Controller()
    C.run()
