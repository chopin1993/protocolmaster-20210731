# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'image_label_ui.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(703, 466)
        self.rawDataLabel = QtWidgets.QLabel(Form)
        self.rawDataLabel.setGeometry(QtCore.QRect(30, 30, 320, 240))
        self.rawDataLabel.setMinimumSize(QtCore.QSize(171, 0))
        self.rawDataLabel.setBaseSize(QtCore.QSize(320, 240))
        self.rawDataLabel.setStyleSheet("background:rgb(255, 255, 255)")
        self.rawDataLabel.setObjectName("rawDataLabel")
        self.resultDataLabel = QtWidgets.QLabel(Form)
        self.resultDataLabel.setGeometry(QtCore.QRect(370, 30, 320, 240))
        self.resultDataLabel.setBaseSize(QtCore.QSize(320, 240))
        self.resultDataLabel.setStyleSheet("background:rgb(0, 255, 0)")
        self.resultDataLabel.setObjectName("resultDataLabel")
        self.playPushButton = QtWidgets.QPushButton(Form)
        self.playPushButton.setGeometry(QtCore.QRect(400, 300, 75, 23))
        self.playPushButton.setObjectName("playPushButton")
        self.infoLabel = QtWidgets.QLabel(Form)
        self.infoLabel.setGeometry(QtCore.QRect(120, 290, 131, 51))
        self.infoLabel.setObjectName("infoLabel")

        self.retranslateUi(Form)
        self.playPushButton.clicked.connect(Form.playbutton_clicked)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.rawDataLabel.setText(_translate("Form", "raw"))
        self.resultDataLabel.setText(_translate("Form", "result"))
        self.playPushButton.setText(_translate("Form", "play"))
        self.infoLabel.setText(_translate("Form", "TextLabel"))
