from PyQt5 import QtCore, QtGui, QtWidgets
from pyqtgraph import PlotWidget

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
        self.exitAction_menubar = QtWidgets.QAction("&Exit", self.main_window)
        self.exitAction_menubar.setShortcut("Ctrl+Q")
        self.exitAction_menubar.setStatusTip('Leave the app from menu bar')
        self.fileMenu.addAction(self.exitAction_menubar)

        self.helpMenu = self.mainMenu.addMenu('&Help')
        self.about = QtWidgets.QAction("&About", self.main_window)
        self.about.setShortcut("F1")
        self.about.setStatusTip('Help and about app')
        self.helpMenu.addAction(self.about)

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
        self.connect_butt.setGeometry(QtCore.QRect(130, 480, 81, 41))
        self.connect_butt.setMinimumSize(QtCore.QSize(81, 41))
        self.connect_butt.setMaximumSize(QtCore.QSize(81, 41))
        self.connect_butt.setObjectName("connect_butt")

        self.refresh_com_butt = QtWidgets.QPushButton(self.butt_frame)
        self.refresh_com_butt.setGeometry(QtCore.QRect(130, 450, 81, 21))
        self.refresh_com_butt.setMinimumSize(QtCore.QSize(81, 21))
        self.refresh_com_butt.setMaximumSize(QtCore.QSize(81, 21))
        self.refresh_com_butt.setObjectName("refresh_com_butt")

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
        self.refresh_com_butt.raise_()
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
        self.signal_list_box.clear()
        for signal in signal_name[1:]:
            self.signal_list_box.addItem(signal)

    def fill_up_COM_list(self, items):
        self.sel_com_combo_box.clear()
        self.sel_com_combo_box.addItems(items)

    def fill_up_baud_rate_list(self):
        baud_rates = ["Select Baude rate", "9600", "14400", "19200", "38400", "57600", "115200", "128000", "256000"]
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
        self.refresh_com_butt.setText(_translate("MainWindow", "Refresh COM"))
        self.baudR_com_label.setText(_translate("MainWindow", "Bauderate"))

