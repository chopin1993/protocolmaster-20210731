# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'G:\ProtocolMaster\source\plug\thermal_image_ui.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(751, 482)
        self.readImageButton = QtWidgets.QPushButton(Form)
        self.readImageButton.setGeometry(QtCore.QRect(630, 60, 121, 23))
        self.readImageButton.setObjectName("readImageButton")
        self.image = QtWidgets.QLabel(Form)
        self.image.setGeometry(QtCore.QRect(10, 20, 591, 371))
        self.image.setStyleSheet("background:rgb(0, 255, 0)")
        self.image.setText("")
        self.image.setObjectName("image")
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setGeometry(QtCore.QRect(150, 400, 211, 71))
        self.groupBox.setObjectName("groupBox")
        self.startButton = QtWidgets.QPushButton(self.groupBox)
        self.startButton.setGeometry(QtCore.QRect(20, 50, 81, 23))
        self.startButton.setObjectName("startButton")
        self.stopButton = QtWidgets.QPushButton(self.groupBox)
        self.stopButton.setGeometry(QtCore.QRect(120, 50, 81, 23))
        self.stopButton.setObjectName("stopButton")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(30, 20, 71, 16))
        self.label.setObjectName("label")
        self.timespanLineeidt = QtWidgets.QLineEdit(self.groupBox)
        self.timespanLineeidt.setGeometry(QtCore.QRect(112, 20, 81, 20))
        self.timespanLineeidt.setObjectName("timespanLineeidt")

        self.retranslateUi(Form)
        self.readImageButton.clicked.connect(Form.readImageOnce)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.readImageButton.setText(_translate("Form", "单次读取热度图"))
        self.groupBox.setTitle(_translate("Form", "循环读取"))
        self.startButton.setText(_translate("Form", "开始"))
        self.stopButton.setText(_translate("Form", "停止"))
        self.label.setText(_translate("Form", "时间间隔"))
