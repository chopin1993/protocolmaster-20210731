# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'camera_ui.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(748, 526)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(13, 10, 640, 480))
        self.label.setStyleSheet("background:rgb(170, 255, 0)")
        self.label.setObjectName("label")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "TextLabel"))
