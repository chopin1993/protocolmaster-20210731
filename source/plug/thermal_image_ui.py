# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'thermal_image_ui.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(676, 477)
        self.readImageButton = QtGui.QPushButton(Form)
        self.readImageButton.setGeometry(QtCore.QRect(350, 30, 121, 23))
        self.readImageButton.setObjectName(_fromUtf8("readImageButton"))
        self.image = QtGui.QLabel(Form)
        self.image.setGeometry(QtCore.QRect(30, 20, 281, 261))
        self.image.setStyleSheet(_fromUtf8("background:rgb(0, 255, 0)"))
        self.image.setText(_fromUtf8(""))
        self.image.setObjectName(_fromUtf8("image"))
        self.groupBox = QtGui.QGroupBox(Form)
        self.groupBox.setGeometry(QtCore.QRect(340, 120, 241, 101))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.startButton = QtGui.QPushButton(self.groupBox)
        self.startButton.setGeometry(QtCore.QRect(20, 50, 81, 23))
        self.startButton.setObjectName(_fromUtf8("startButton"))
        self.stopButton = QtGui.QPushButton(self.groupBox)
        self.stopButton.setGeometry(QtCore.QRect(120, 50, 81, 23))
        self.stopButton.setObjectName(_fromUtf8("stopButton"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(30, 20, 71, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.timespanLineeidt = QtGui.QLineEdit(self.groupBox)
        self.timespanLineeidt.setGeometry(QtCore.QRect(112, 20, 81, 20))
        self.timespanLineeidt.setObjectName(_fromUtf8("timespanLineeidt"))

        self.retranslateUi(Form)
        QtCore.QObject.connect(self.readImageButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Form.readImageOnce)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.readImageButton.setText(_translate("Form", "单次读取热度图", None))
        self.groupBox.setTitle(_translate("Form", "循环读取", None))
        self.startButton.setText(_translate("Form", "开始", None))
        self.stopButton.setText(_translate("Form", "停止", None))
        self.label.setText(_translate("Form", "时间间隔", None))

