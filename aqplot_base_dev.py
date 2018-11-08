import sys
import serial.tools.list_ports


from PyQt5 import QtCore, QtGui, QtWidgets
from pyqtgraph import PlotWidget, AxisItem
import pandas as pd
'''
    Using this comand a .ui file shall be converted to .py file
    path_of_pyuic tool : "C:\_Users\axint\AppData\Local\Programs\Python\Python36\Scripts>pyuic5.exe" 
                          C:\_Users\axint\AppData\Roaming\Python\Python36\Scripts
                          
    
    command = pyuic5.exe -x file_to_Be_converted.ui -o result_of_convertion.py
'''

class Model:
    def __init__(self):
        self.number_of_signals = int()
        self.signal_names = []



    def import_signals(self, file_name):

        with open(file_name, newline='') as f:
            if f != "":
                self.meas_data = pd.read_csv(f, low_memory=False)

        self.signal_names = self.meas_data.keys()
        self.number_of_signals = len(self.signal_names)



'''
    This class shall represent the View:
        - all gui related objects
        - 
'''
class TimeAxisItem(AxisItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def tickStrings(self, values, scale, spacing):
        # PySide's QTime() initialiser fails miserably and dismisses args/kwargs
        #return [QTime().addMSecs(value).toString('mm:ss') for value in values]
        return [int2dt(value).strftime("%H:%M:%S.%f") for value in values]

class View:

    def __init__(self, MainWindow):
        self.main_window = MainWindow
        self.main_frame_init()
        self.create_graph_view()
        self.create_open_meas_butt()
        self.create_clr_scr_butt()
        self.create_signal_list()
        self.create_menu_bar()
        self.create_serial_panel()

        '''
            The show() method shall be called ALWAYS after 
            the backyard is done and ready. 
        '''
        self.retranslateUi()
        self.main_window.show()

    def main_frame_init(self):
        self.main_window.setObjectName("MainWindow")
        self.main_window.resize(1150, 600)

        self.centralwidget = QtWidgets.QWidget(self.main_window)
        self.centralwidget.setObjectName("centralwidget")

        self.central_gridLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.central_gridLayout.setObjectName("central_gridLayout")

        '''buttons frame'''
        self.butt_frame = QtWidgets.QFrame(self.centralwidget)
        self.butt_frame.setMinimumSize(QtCore.QSize(231, 521))
        self.butt_frame.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.butt_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.butt_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.butt_frame.setObjectName("butt_frame")

        self.central_gridLayout.addWidget(self.butt_frame)
        self.main_window.setCentralWidget(self.centralwidget)

        QtCore.QMetaObject.connectSlotsByName(self.main_window)

    def create_open_meas_butt(self):
        self.open_meas_butt = QtWidgets.QPushButton(self.butt_frame)
        self.open_meas_butt.setGeometry(QtCore.QRect(10, 10, 201, 31))
        self.open_meas_butt.setMinimumSize(QtCore.QSize(201, 31))
        self.open_meas_butt.setMaximumSize(QtCore.QSize(201, 31))
        self.open_meas_butt.setObjectName("open_meas_butt")
        self.open_meas_butt.raise_()

    def create_clr_scr_butt(self):
        self.clr_scr = QtWidgets.QPushButton(self.butt_frame)
        self.clr_scr.setGeometry(QtCore.QRect(10, 50, 201, 31))
        self.clr_scr.setMinimumSize(QtCore.QSize(201, 31))
        self.clr_scr.setMaximumSize(QtCore.QSize(201, 31))
        self.clr_scr.setObjectName("clr_scr")
        self.clr_scr.raise_()

    def create_menu_bar(self):
        self.mainMenu = self.main_window.menuBar()

        self.fileMenu = self.mainMenu.addMenu('&File')


        self.openFileAction_menubar = QtWidgets.QAction("&Open...", self.main_window)
        self.openFileAction_menubar.setShortcut("Ctrl+O")
        self.openFileAction_menubar.setStatusTip('Open a txt file')
        self.fileMenu.addAction(self.openFileAction_menubar)

        self.fileMenu = self.mainMenu.addMenu('&File')
        self.exitAction_menubar = QtWidgets.QAction("&Exit", self.main_window)
        self.exitAction_menubar.setShortcut("Ctrl+Q")
        self.exitAction_menubar.setStatusTip('Leave the app from menu bar')
        self.fileMenu.addAction(self.exitAction_menubar)

    def create_tool_bar(self):
        self.toolBar = self.addToolBar("Another Exit")
        self.extractAction_toolbar = QtWidgets.QAction(QtGui.QIcon("exit.png"),"&Another Exit point", self)
        self.toolBar.addAction(self.extractAction_toolbar)
        self.extractAction_toolbar.setStatusTip('Leave the app toolbar')

    def create_check_box(self):
        self.check_box = QtWidgets.QCheckBox("Check this to enlarge window",self)
        self.check_box.setGeometry(100,25,250,40)
        #self.check_box.move(100,25)
        #self.check_box.toggle()
        self.check_box.stateChanged.connect(self.enlarge_window)

    def create_progres_bar(self):
        self.progress = QtWidgets.QProgressBar(self)
        self.progress.setGeometry(250,55,250,20)

    def create_serial_panel(self):
        self.sel_com_combo_box = QtWidgets.QComboBox(self.butt_frame)
        self.sel_com_combo_box.setGeometry(QtCore.QRect(10, 450, 111, 21))
        self.sel_com_combo_box.setMinimumSize(QtCore.QSize(111, 21))
        self.sel_com_combo_box.setMaximumSize(QtCore.QSize(111, 21))
        self.sel_com_combo_box.setObjectName("sel_com_combo_box")

        self.sel_baudR_combo_box = QtWidgets.QComboBox(self.butt_frame)
        self.sel_baudR_combo_box.setGeometry(QtCore.QRect(10, 500, 111, 21))
        self.sel_baudR_combo_box.setMinimumSize(QtCore.QSize(111, 21))
        self.sel_baudR_combo_box.setMaximumSize(QtCore.QSize(111, 21))
        self.sel_baudR_combo_box.setObjectName("sel_baudR_combo_box")

        self.run_meas_butt = QtWidgets.QPushButton(self.butt_frame)
        self.run_meas_butt.setGeometry(QtCore.QRect(10, 530, 201, 41))
        self.run_meas_butt.setMinimumSize(QtCore.QSize(201, 41))
        self.run_meas_butt.setMaximumSize(QtCore.QSize(211, 41))
        self.run_meas_butt.setObjectName("run_meas_butt")

        self.connect_butt = QtWidgets.QPushButton(self.butt_frame)
        self.connect_butt.setGeometry(QtCore.QRect(140, 450, 71, 71))
        self.connect_butt.setMinimumSize(QtCore.QSize(71, 71))
        self.connect_butt.setMaximumSize(QtCore.QSize(71, 71))
        self.connect_butt.setObjectName("connect_butt")

        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)

        self.baudR_com_label = QtWidgets.QLabel(self.butt_frame)
        self.baudR_com_label.setGeometry(QtCore.QRect(10, 470, 111, 29))
        self.baudR_com_label.setMinimumSize(QtCore.QSize(91, 29))
        self.baudR_com_label.setMaximumSize(QtCore.QSize(111, 29))

        self.baudR_com_label.setFont(font)
        self.baudR_com_label.setTextFormat(QtCore.Qt.AutoText)
        self.baudR_com_label.setScaledContents(True)
        self.baudR_com_label.setWordWrap(False)
        self.baudR_com_label.setObjectName("baudR_com_label")

        self.sel_com_label = QtWidgets.QLabel(self.butt_frame)
        self.sel_com_label.setGeometry(QtCore.QRect(10, 420, 111, 29))
        self.sel_com_label.setMinimumSize(QtCore.QSize(91, 29))
        self.sel_com_label.setMaximumSize(QtCore.QSize(111, 29))

        self.sel_com_label.setFont(font)
        self.sel_com_label.setTextFormat(QtCore.Qt.AutoText)
        self.sel_com_label.setScaledContents(True)
        self.sel_com_label.setWordWrap(False)
        self.sel_com_label.setObjectName("sel_com_label")

        self.sel_com_combo_box.raise_()
        self.sel_com_label.raise_()
        self.run_meas_butt.raise_()
        self.connect_butt.raise_()
        self.baudR_com_label.raise_()
        self.sel_baudR_combo_box.raise_()



    def open_file_dialog(self):
        file_name, value = QtWidgets.QFileDialog.getOpenFileName(self.main_window, 'Choise a file')
        return file_name

    def create_graph_view(self):
        self.graphicsView = PlotWidget(self.centralwidget)#axisItems={'bottom': TimeAxisItem(orientation='bottom')})
        self.graphicsView.setMinimumSize(QtCore.QSize(893, 582))
        self.graphicsView.setObjectName("graphicsView")
        self.central_gridLayout.addWidget(self.graphicsView)

    def create_signal_list(self):
        self.signals_box_label = QtWidgets.QLabel(self.butt_frame)
        self.signals_box_label.setGeometry(QtCore.QRect(11, 85, 60, 29))
        self.signals_box_label.setMinimumSize(QtCore.QSize(60, 29))
        self.signals_box_label.setMaximumSize(QtCore.QSize(60, 29))

        font = QtGui.QFont()
        font.setPointSize(12)
        font.setWeight(50)
        self.signals_box_label.setFont(font)
        self.signals_box_label.setTextFormat(QtCore.Qt.AutoText)
        self.signals_box_label.setScaledContents(True)
        self.signals_box_label.setWordWrap(False)
        self.signals_box_label.setObjectName("signals_box_label")

        self.signal_list_box = QtWidgets.QListWidget(self.butt_frame)
        self.signal_list_box.setGeometry(QtCore.QRect(10, 120, 201, 281))
        self.signal_list_box.setObjectName("listWidget")
        self.signal_list_box.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.signals_box_label.raise_()

    def fill_up_signal_list(self, signal_name):
        for signal in signal_name[1:]:
            self.signal_list_box.addItem(signal)

    def fill_up_COM_list(self, items):
        self.sel_com_combo_box.addItems(items)

    def fill_up_baud_rate_list(self):
        baud_rates = ["9600", "14400", "19200", "38400", "57600", "115200", "128000", "256000"]
        self.sel_baudR_combo_box.addItems(baud_rates)

    def pop_up_on_exit(self):
        areYouSure = QtWidgets.QMessageBox.question(self, 'Exit', "Get Out?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        return areYouSure

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.main_window.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.open_meas_butt.setText(_translate("MainWindow", "Open Measurement"))
        self.clr_scr.setText(_translate("MainWindow", "Clear Screen"))
        self.signals_box_label.setText(_translate("MainWindow", "Signals"))
        self.sel_com_label.setText(_translate("MainWindow", "Select COM"))
        self.run_meas_butt.setText(_translate("MainWindow", "Run \n"" Measurement"))
        self.connect_butt.setText(_translate("MainWindow", "Connect"))
        self.baudR_com_label.setText(_translate("MainWindow", "Bauderate"))


class Controller:
    def __init__(self):
        self.app = QtWidgets.QApplication([])

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
        self.get_host_com_ports()


    def run(self):
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
            ports = serial.tools.list_ports.comports()
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
        pass

    def select_baud_rate(self, baudrate):
        '''
        This method shall be used to send the selected port
        to the serial driver
        '''
        pass

    def _quit(self):
        get_user_ans = self.view.pop_up_on_exit()
        if get_user_ans == QtWidgets.QMessageBox.Yes:
            sys.exit()
        else :
            pass


if __name__ == '__main__':
    C = Controller()
    C.run()

