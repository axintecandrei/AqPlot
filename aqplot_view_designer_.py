# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\.github.com\AqPlot\aqplot_view_designer.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1148, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.central_gridLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.central_gridLayout.setObjectName("central_gridLayout")
        self.butt_frame = QtWidgets.QFrame(self.centralwidget)
        self.butt_frame.setMinimumSize(QtCore.QSize(231, 521))
        self.butt_frame.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.butt_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.butt_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.butt_frame.setObjectName("butt_frame")
        self.open_meas_butt = QtWidgets.QPushButton(self.butt_frame)
        self.open_meas_butt.setGeometry(QtCore.QRect(10, 10, 201, 31))
        self.open_meas_butt.setMinimumSize(QtCore.QSize(201, 31))
        self.open_meas_butt.setMaximumSize(QtCore.QSize(201, 31))
        self.open_meas_butt.setObjectName("open_meas_butt")
        self.clr_scr = QtWidgets.QPushButton(self.butt_frame)
        self.clr_scr.setGeometry(QtCore.QRect(10, 50, 201, 31))
        self.clr_scr.setMaximumSize(QtCore.QSize(201, 31))
        self.clr_scr.setObjectName("clr_scr")
        self.signals_box_label = QtWidgets.QLabel(self.butt_frame)
        self.signals_box_label.setGeometry(QtCore.QRect(11, 85, 60, 29))
        self.signals_box_label.setMinimumSize(QtCore.QSize(60, 29))
        self.signals_box_label.setMaximumSize(QtCore.QSize(60, 29))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.signals_box_label.setFont(font)
        self.signals_box_label.setTextFormat(QtCore.Qt.AutoText)
        self.signals_box_label.setScaledContents(True)
        self.signals_box_label.setWordWrap(False)
        self.signals_box_label.setObjectName("signals_box_label")
        self.signal_list_box = QtWidgets.QListWidget(self.butt_frame)
        self.signal_list_box.setGeometry(QtCore.QRect(10, 120, 201, 281))
        self.signal_list_box.setObjectName("signal_list_box")
        self.sel_com_combo_box = QtWidgets.QComboBox(self.butt_frame)
        self.sel_com_combo_box.setGeometry(QtCore.QRect(10, 450, 111, 21))
        self.sel_com_combo_box.setMinimumSize(QtCore.QSize(111, 21))
        self.sel_com_combo_box.setMaximumSize(QtCore.QSize(111, 21))
        self.sel_com_combo_box.setObjectName("sel_com_combo_box")
        self.sel_com_label = QtWidgets.QLabel(self.butt_frame)
        self.sel_com_label.setGeometry(QtCore.QRect(10, 420, 111, 29))
        self.sel_com_label.setMinimumSize(QtCore.QSize(91, 29))
        self.sel_com_label.setMaximumSize(QtCore.QSize(111, 29))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.sel_com_label.setFont(font)
        self.sel_com_label.setTextFormat(QtCore.Qt.AutoText)
        self.sel_com_label.setScaledContents(True)
        self.sel_com_label.setWordWrap(False)
        self.sel_com_label.setObjectName("sel_com_label")
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
        self.baudR_com_label = QtWidgets.QLabel(self.butt_frame)
        self.baudR_com_label.setGeometry(QtCore.QRect(10, 470, 111, 29))
        self.baudR_com_label.setMinimumSize(QtCore.QSize(91, 29))
        self.baudR_com_label.setMaximumSize(QtCore.QSize(111, 29))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.baudR_com_label.setFont(font)
        self.baudR_com_label.setTextFormat(QtCore.Qt.AutoText)
        self.baudR_com_label.setScaledContents(True)
        self.baudR_com_label.setWordWrap(False)
        self.baudR_com_label.setObjectName("baudR_com_label")
        self.sel_baudR_combo_box = QtWidgets.QComboBox(self.butt_frame)
        self.sel_baudR_combo_box.setGeometry(QtCore.QRect(10, 500, 111, 21))
        self.sel_baudR_combo_box.setMinimumSize(QtCore.QSize(111, 21))
        self.sel_baudR_combo_box.setMaximumSize(QtCore.QSize(111, 21))
        self.sel_baudR_combo_box.setObjectName("sel_baudR_combo_box")
        self.refresh_com_butt = QtWidgets.QPushButton(self.butt_frame)
        self.refresh_com_butt.setGeometry(QtCore.QRect(130, 450, 81, 21))
        self.refresh_com_butt.setMinimumSize(QtCore.QSize(81, 21))
        self.refresh_com_butt.setMaximumSize(QtCore.QSize(81, 21))
        self.refresh_com_butt.setObjectName("refresh_com_butt")
        self.signals_box_label.raise_()
        self.signal_list_box.raise_()
        self.open_meas_butt.raise_()
        self.clr_scr.raise_()
        self.sel_com_combo_box.raise_()
        self.sel_com_label.raise_()
        self.run_meas_butt.raise_()
        self.connect_butt.raise_()
        self.baudR_com_label.raise_()
        self.sel_baudR_combo_box.raise_()
        self.refresh_com_butt.raise_()
        self.central_gridLayout.addWidget(self.butt_frame)
        self.graphicsView = PlotWidget(self.centralwidget)
        self.graphicsView.setMinimumSize(QtCore.QSize(893, 582))
        self.graphicsView.setObjectName("graphicsView")
        self.central_gridLayout.addWidget(self.graphicsView)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.open_meas_butt.setText(_translate("MainWindow", "Open Measurement"))
        self.clr_scr.setText(_translate("MainWindow", "Clear Screen"))
        self.signals_box_label.setText(_translate("MainWindow", "Signals"))
        self.sel_com_label.setText(_translate("MainWindow", "Select COM"))
        self.run_meas_butt.setText(_translate("MainWindow", "Run \n"
" Measurement"))
        self.connect_butt.setText(_translate("MainWindow", "Connect"))
        self.baudR_com_label.setText(_translate("MainWindow", "Bauderate"))
        self.refresh_com_butt.setText(_translate("MainWindow", "Refresh COM"))

from pyqtgraph import PlotWidget

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

