from PyQt5 import QtCore, QtGui, QtWidgets
#from pyqtgraph import PlotWidget
from asammdf.gui.widgets.plot import Plot, PlotSignal
from asammdf.gui.widgets.plot_standalone import PlotWindow
from asammdf.gui.widgets.list import ListWidget
from asammdf.gui.widgets.tree import TreeWidget
class View:
    def __init__(self, MainWindow):
        self.main_window = MainWindow
        self.main_frame_init()
        self.create_graph_view()
        self.create_signal_panel()
        self.create_menu_bar()
        self.create_serial_panel()
        self._translate = QtCore.QCoreApplication.translate
        '''
            The show() method shall be called ALWAYS after 
            the backyard is done and ready. 
        '''

        self.retranslateUi()
        self.main_window.showMaximized()

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


    def create_menu_bar(self):
        self.mainMenu = self.main_window.menuBar()

        self.fileMenu = self.mainMenu.addMenu('&File')


        self.openFileAction_menubar = QtWidgets.QAction("&Open Measurement", self.main_window)
        self.openFileAction_menubar.setShortcut("Ctrl+O")
        self.openFileAction_menubar.setStatusTip('Open a measurement file')
        self.fileMenu.addAction(self.openFileAction_menubar)

        self.opendspAction_menubar = QtWidgets.QAction("&Load signal info", self.main_window)
        self.opendspAction_menubar.setShortcut("Ctrl+Shift+O")
        self.opendspAction_menubar.setStatusTip('Load some sort of a2l file')
        self.fileMenu.addAction(self.opendspAction_menubar)

        self.save_measAction_menubar = QtWidgets.QAction("&Save Measurement", self.main_window)
        self.save_measAction_menubar.setShortcut("Ctrl+Alt+S")
        self.save_measAction_menubar.setStatusTip('Save the acquired data into a mdf file')
        self.fileMenu.addAction(self.save_measAction_menubar)

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
        self.sel_com_combo_box.setGeometry(QtCore.QRect(10, 460, 211, 21))
        self.sel_com_combo_box.setMinimumSize(QtCore.QSize(111, 21))
        self.sel_com_combo_box.setMaximumSize(QtCore.QSize(211, 21))
        self.sel_com_combo_box.setObjectName("sel_com_combo_box")

        self.sel_baudR_combo_box = QtWidgets.QComboBox(self.butt_frame)
        self.sel_baudR_combo_box.setGeometry(QtCore.QRect(10, 520, 111, 21))
        self.sel_baudR_combo_box.setMinimumSize(QtCore.QSize(111, 21))
        self.sel_baudR_combo_box.setMaximumSize(QtCore.QSize(211, 21))
        self.sel_baudR_combo_box.setObjectName("sel_baudR_combo_box")

        self.run_meas_butt = QtWidgets.QPushButton(self.butt_frame)
        self.run_meas_butt.setGeometry(QtCore.QRect(10, 550, 211, 41))
        self.run_meas_butt.setMinimumSize(QtCore.QSize(201, 41))
        self.run_meas_butt.setMaximumSize(QtCore.QSize(211, 41))
        self.run_meas_butt.setObjectName("run_meas_butt")

        self.connect_butt = QtWidgets.QPushButton(self.butt_frame)
        self.connect_butt.setGeometry(QtCore.QRect(140, 490, 81, 52))
        self.connect_butt.setMinimumSize(QtCore.QSize(81, 41))
        self.connect_butt.setMaximumSize(QtCore.QSize(81, 100))
        self.connect_butt.setObjectName("connect_butt")

        self.refresh_com_butt = QtWidgets.QPushButton(self.butt_frame)
        self.refresh_com_butt.setGeometry(QtCore.QRect(170, 420, 51, 31))
        self.refresh_com_butt.setMinimumSize(QtCore.QSize(21, 21))
        self.refresh_com_butt.setMaximumSize(QtCore.QSize(81, 81))
        self.refresh_com_butt.setIcon(QtGui.QIcon("d:\casdev\sbxs\github_com\AqPlot\Src\GUI\_refresh_icon.png"))
        self.refresh_com_butt.setIconSize(QtCore.QSize(31, 31))
        self.refresh_com_butt.setObjectName("refresh_com_butt")

        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)

        self.baudR_com_label = QtWidgets.QLabel(self.butt_frame)
        self.baudR_com_label.setGeometry(QtCore.QRect(10, 490, 111, 29))
        self.baudR_com_label.setMinimumSize(QtCore.QSize(91, 29))
        self.baudR_com_label.setMaximumSize(QtCore.QSize(111, 29))

        self.baudR_com_label.setFont(font)
        self.baudR_com_label.setTextFormat(QtCore.Qt.AutoText)
        self.baudR_com_label.setScaledContents(True)
        self.baudR_com_label.setWordWrap(False)
        self.baudR_com_label.setObjectName("baudR_com_label")

        self.sel_com_label = QtWidgets.QLabel(self.butt_frame)
        self.sel_com_label.setGeometry(QtCore.QRect(10, 430, 111, 29))
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


    def create_graph_view(self):
        #self.graphicsView = PlotWidget(self.centralwidget)
        self.graphicsView = PlotWindow([])
        #self.graphicsView.setMinimumSize(QtCore.QSize(893, 582))
        #self.graphicsView.setObjectName("graphicsView")
        self.central_gridLayout.addWidget(self.graphicsView)

    def create_signal_panel(self):
        self.signals_box_label = QtWidgets.QLabel(self.butt_frame)
        self.signals_box_label.setGeometry(QtCore.QRect(10, 60, 60, 29))
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
        self.signal_list_box.setGeometry(QtCore.QRect(10, 90, 211, 281))
        self.signal_list_box.setObjectName("listWidget")
        self.signal_list_box.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.signals_box_label.raise_()

        self.plot_butt = QtWidgets.QPushButton(self.butt_frame)
        self.plot_butt.setGeometry(QtCore.QRect(10, 380, 211, 35))
        self.plot_butt.setIcon(QtGui.QIcon("d:\casdev\sbxs\github_com\AqPlot\Src\GUI\plot_icon.png"))
        self.plot_butt.setIconSize(QtCore.QSize(33,33))
        self.plot_butt.setObjectName("plot_butt")
        self.plot_butt.raise_()

        self.open_meas_butt = QtWidgets.QPushButton(self.butt_frame)
        self.open_meas_butt.setGeometry(QtCore.QRect(10, 10, 201, 31))
        self.open_meas_butt.setMinimumSize(QtCore.QSize(201, 31))
        self.open_meas_butt.setMaximumSize(QtCore.QSize(201, 31))
        self.open_meas_butt.setObjectName("open_meas_butt")
        self.open_meas_butt.raise_()

    def fill_up_signal_list(self, signal_list):
        self.signal_list_box.clear()
        for signal in signal_list:
            item = QtWidgets.QListWidgetItem()
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            item.setCheckState(QtCore.Qt.Unchecked)
            item.setText(signal)
            self.signal_list_box.addItem(item)

    def fill_up_COM_list(self, items):
        self.sel_com_combo_box.clear()
        self.sel_com_combo_box.addItems(items)

    def fill_up_baud_rate_list(self):
        baud_rates = ["Select Baude rate", "9600", "14400", "19200", "38400", "57600", "115200", "128000", "256000", "750000", "1000000"]
        self.sel_baudR_combo_box.addItems(baud_rates)

    def open_file_dialog(self, filter_file_ext):
        file_name, value = QtWidgets.QFileDialog.getOpenFileName(self.main_window, 'Choose a file', filter=filter_file_ext)
        return file_name

    def get_dir_path(self, window_title):
        path = QtWidgets.QFileDialog.getExistingDirectory(self.main_window, window_title)
        return path

    def get_saved_file_name(self, window_title, filter=''):
        path_name, unused = QtWidgets.QFileDialog.getSaveFileName(self.main_window, window_title, filter=filter)
        return path_name

    def msg_box(self,p_str_title,p_str_msg):
        QtWidgets.QMessageBox.question(self.main_window,p_str_title,p_str_msg, QtWidgets.QMessageBox.Ok)

    def ask_user_binary_question(self, window_title, question):
        user_reply = QtWidgets.QMessageBox.question(self.main_window, window_title, question,
                                                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        return user_reply

    def get_string_from_user(self, window_title, suggestion):
        str, value = QtWidgets.QInputDialog.getText(self.main_window, window_title, suggestion)
        return str

    def retranslateUi(self):
        self.main_window.setWindowTitle(self._translate("MainWindow", "AqPlot"))
        self.open_meas_butt.setText(self._translate("MainWindow", "Open Measurement"))
        #self.clr_scr.setText(self._translate("MainWindow", "Clear Screen"))
        #self.plot_butt.setText(self._translate("MainWindow", "Plot"))
        self.signals_box_label.setText(self._translate("MainWindow", "Signals"))
        self.sel_com_label.setText(self._translate("MainWindow", "Select COM"))
        self.run_meas_butt.setText(self._translate("MainWindow", "Run \n"" Measurement"))
        self.connect_butt.setText(self._translate("MainWindow", "Connect"))
        #self.refresh_com_butt.setText(self._translate("MainWindow", "Refresh COM"))
        self.baudR_com_label.setText(self._translate("MainWindow", "Bauderate"))


