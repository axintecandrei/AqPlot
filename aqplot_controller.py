from aqplot_model import Model
from aqplot_view import *
import sys
from aqplot_serial import *



class Controller:
    def __init__(self):
        self.app = QtWidgets.QApplication([])

        self.serial = ser_thread("AqPlot")

        self.model = Model()
        self.view = View(QtWidgets.QMainWindow())

        self.view.open_meas_butt.clicked.connect(self.open_and_load_file)
        self.view.clr_scr.clicked.connect(self.clear_graph)
        self.view.signal_list_box.itemSelectionChanged.connect(self.add_signal_to_plot)
        self.view.openFileAction_menubar.triggered.connect(self.open_and_load_file)
        self.view.exitAction_menubar.triggered.connect(self._quit)
        self.view.sel_com_combo_box.activated[str].connect(self.select_com_port)
        self.view.sel_baudR_combo_box.activated[str].connect(self.select_baud_rate)
        self.view.fill_up_baud_rate_list()
        self.view.connect_butt.clicked.connect(self.serial.open_close)
        self.view.refresh_com_butt.clicked.connect(self.get_host_com_ports)

    def run(self):
        self.serial.start()
        self.app.exec()

    def open_and_load_file(self):
        file_name = self.view.open_file_dialog()
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

    def get_host_com_ports(self):
            ports = self.serial.list_comports()
            if not ports:
                self.view.fill_up_COM_list(["No ports available"])
            else:
                port_list = []
                for port, desc, hwid in sorted(ports):
                    port_list.append(port)
                self.view.fill_up_COM_list(port_list)

    def select_com_port(self, port):
        '''
        This method shall be used to send the selected port
        to the serial driver
        '''
        self.serial.set_port(port)


    def select_baud_rate(self, baudrate):
        '''
        This method shall be used to send the selected port
        to the serial driver
        '''
        if baudrate != "Select Baude rate":
            self.serial.set_baud(baudrate)


    def _quit(self):
        get_user_ans = self.view.pop_up_on_exit()
        if get_user_ans == QtWidgets.QMessageBox.Yes:
            sys.exit()
        else :
            pass

if __name__ == '__main__':
    C = Controller()
    C.run()
