import sys
import threading
import serial
import serial.tools.list_ports
from aqplot_model import Model
from aqplot_view import *
import csv


class Controller:
    def __init__(self):
        self.app = QtWidgets.QApplication([])

        self.serial = SerThread("AqPlot")
        self.model = Model()
        self.view = View(QtWidgets.QMainWindow())

        self.view.open_meas_butt.clicked.connect(self.open_and_load_file)
        self.view.clr_scr.clicked.connect(self.clear_graph)
        self.view.signal_list_box.itemSelectionChanged.connect(self.add_signal_to_plot)
        self.view.openFileAction_menubar.triggered.connect(self.open_and_load_file)
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
    def open_and_load_file(self):
        file_name = self.view.open_file_dialog()
        if not file_name:
            pass
        else :
            self.model.import_signals(file_name)
            self.view.fill_up_signal_list(self.model.signal_names)

    def aq_plot(self, data):
        self.view.graphicsView.plot(data, pen='g')
        #self.view.graphicsView.setLabel('left', 'Voltage', units='V')

    def add_signal_to_plot(self):
        selected_signal = self.view.signal_list_box.selectedItems()
        for signal in selected_signal:
            self.aq_plot(self.model.meas_data[signal.text()])

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
            print("Connection not established or not configured")

    def c_serial_open_close_connection(self):
        serial_status = self.serial.serial_connection_control()
        if serial_status is "serial_open":
            self.view.connect_butt.setText(self.view._translate("MainWindow", "Disconnect"))
        elif serial_status is "serial_close":
            self.view.connect_butt.setText(self.view._translate("MainWindow", "Connect"))
        elif serial_status is "serial_error_access_denied":
            print("Acces Denied")
        elif serial_status is "error_unknown":
            print("Some error")

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
    def __init__(self, thread_name):
        super(SerThread, self).__init__()
        self.name = thread_name
        self.ser = serial.Serial()
        self.com_port_list = []

        """Das state machine bones"""
        self.DasState = 'StandBy'
        self.DASHandler = { 'StandBy'    : self.DAS_State_StandBy,
                            'StartOfMeas': self.DAS_State_StartOfMeas,
                            'ReceiveData': self.DAS_State_ReceiveData,
                            'SendAck'    : self.DAS_State_SendAck,
                            'StopMeas'   : self.DAS_State_StopMeas}

        self.commands = {'Cmd_StartMeas': chr(0x31).encode(),
                         'Cmd_ACK'      : chr(0x35).encode(),
                         'Cmd_StopMeas' : chr(0x30).encode()}

        self.input_pack_size = 26

    # gets called when thread is started with .start()
    def run(self):
        while True:
            self.com_port_list = serial.tools.list_ports.comports()
            if self.ser.is_open:
                '''state machine handler will be called here'''
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
            data = []
            line = self.ser.read(nr_of_bytes)
            for char in range(len(line)):
                data.append(line[char])
            self.csv_out.writerow(data)

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
        self.f = open('output_test.csv', 'w+')
        self.name_list = ["byte0,",
                          "byte1,",
                          "byte2,",
                          "byte3,",
                          "byte4,",
                          "byte5,",
                          "byte6,",
                          "byte7,",
                          "byte8,",
                          "byte9,",
                          "byte10,",
                          "byte11,","byte12,","byte13,","byte14,","byte15,","byte16,","byte17,","byte18,","byte19,",
                          "byte20,","byte21,","byte22,","byte23,","byte24,","byte25,","byte26,"]

        self.csv_out = csv.writer(self.f, dialect='excel-tab')
        self.csv_out.writerow("sep=,")
        self.csv_out.writerow(self.name_list)


        self.serial_tx(self.commands['Cmd_StartMeas'])
        self.DasState = 'ReceiveData'

    def DAS_State_ReceiveData(self):
        self.serial_rx(self.input_pack_size)
        self.DasState = 'SendAck'

    def DAS_State_SendAck(self):
        self.serial_tx(self.commands['Cmd_ACK'])
        self.DasState = 'ReceiveData'

    def DAS_State_StopMeas(self):
        print("stop of meas")

        self.f.close()
        self.DasState = 'StandBy'


if __name__ == '__main__':
    C = Controller()
    C.run()
