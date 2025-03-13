# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\Imixadmin\Documents\POC_Zommerango\GoPro_Server\Running_Setup_Zoomeango\camera_v2.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(592, 763)
        MainWindow.setMaximumSize(QtCore.QSize(592, 763))
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 100, 571, 111))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.camera_label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(28)
        self.camera_label.setFont(font)
        self.camera_label.setAlignment(QtCore.Qt.AlignCenter)
        self.camera_label.setObjectName("camera_label")
        self.horizontalLayout.addWidget(self.camera_label)
        self.Battery = QtWidgets.QLCDNumber(self.horizontalLayoutWidget)
        self.Battery.setObjectName("Battery")
        self.horizontalLayout.addWidget(self.Battery)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 220, 571, 291))
        self.groupBox.setMaximumSize(QtCore.QSize(571, 291))
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.groupBox)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(10, 20, 551, 51))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.auto_radiobutton = QtWidgets.QRadioButton(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(21)
        self.auto_radiobutton.setFont(font)
        self.auto_radiobutton.setObjectName("auto_radiobutton")
        self.horizontalLayout_2.addWidget(self.auto_radiobutton)
        self.manual_radiobutton = QtWidgets.QRadioButton(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(21)
        self.manual_radiobutton.setFont(font)
        self.manual_radiobutton.setObjectName("manual_radiobutton")
        self.horizontalLayout_2.addWidget(self.manual_radiobutton)
        self.horizontalLayoutWidget_3 = QtWidgets.QWidget(self.groupBox)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(60, 80, 461, 41))
        self.horizontalLayoutWidget_3.setObjectName("horizontalLayoutWidget_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.download_radioButton = QtWidgets.QRadioButton(self.horizontalLayoutWidget_3)
        self.download_radioButton.setObjectName("download_radioButton")
        self.horizontalLayout_3.addWidget(self.download_radioButton)
        self.photo_radioButton = QtWidgets.QRadioButton(self.horizontalLayoutWidget_3)
        self.photo_radioButton.setObjectName("photo_radioButton")
        self.horizontalLayout_3.addWidget(self.photo_radioButton)
        self.video_radioButton = QtWidgets.QRadioButton(self.horizontalLayoutWidget_3)
        self.video_radioButton.setObjectName("video_radioButton")
        self.horizontalLayout_3.addWidget(self.video_radioButton)
        self.tableWidget = QtWidgets.QTableWidget(self.groupBox)
        self.tableWidget.setGeometry(QtCore.QRect(10, 140, 561, 141))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(410, 580, 171, 121))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.start_pushbutton = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(22)
        self.start_pushbutton.setFont(font)
        self.start_pushbutton.setObjectName("start_pushbutton")
        self.verticalLayout_2.addWidget(self.start_pushbutton)
        self.start_pushbutton_2 = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(22)
        self.start_pushbutton_2.setFont(font)
        self.start_pushbutton_2.setObjectName("start_pushbutton_2")
        self.verticalLayout_2.addWidget(self.start_pushbutton_2)
        self.log_textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.log_textEdit.setGeometry(QtCore.QRect(10, 520, 391, 181))
        self.log_textEdit.setObjectName("log_textEdit")
        self.horizontalLayoutWidget_4 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_4.setGeometry(QtCore.QRect(20, 10, 531, 81))
        self.horizontalLayoutWidget_4.setObjectName("horizontalLayoutWidget_4")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_4)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.tag_label = QtWidgets.QLabel(self.horizontalLayoutWidget_4)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.tag_label.setFont(font)
        self.tag_label.setObjectName("tag_label")
        self.horizontalLayout_4.addWidget(self.tag_label)
        self.tag_lineEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget_4)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.tag_lineEdit.setFont(font)
        self.tag_lineEdit.setObjectName("tag_lineEdit")
        self.horizontalLayout_4.addWidget(self.tag_lineEdit)
        self.tag_button = QtWidgets.QPushButton(self.horizontalLayoutWidget_4)
        self.tag_button.setObjectName("tag_button")
        self.horizontalLayout_4.addWidget(self.tag_button)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 592, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "GoPro Controller"))
        self.camera_label.setText(_translate("MainWindow", "Camera model"))
        self.groupBox.setTitle(_translate("MainWindow", "Operation"))
        self.auto_radiobutton.setText(_translate("MainWindow", "Auto"))
        self.manual_radiobutton.setText(_translate("MainWindow", "Manual"))
        self.download_radioButton.setText(_translate("MainWindow", "Download"))
        self.photo_radioButton.setText(_translate("MainWindow", "Photo"))
        self.video_radioButton.setText(_translate("MainWindow", "Video"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "ID"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Code"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Time Stamp"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Original file"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Associated file"))
        self.start_pushbutton.setText(_translate("MainWindow", "Start"))
        self.start_pushbutton_2.setText(_translate("MainWindow", "Stop"))
        self.tag_label.setText(_translate("MainWindow", "Tag Folder :"))
        self.tag_button.setText(_translate("MainWindow", "Browse"))
