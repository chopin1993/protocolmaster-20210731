# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'success_radio_plug_ui.ui'
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
        Form.resize(767, 528)
        self.appGroupBox = QtGui.QGroupBox(Form)
        self.appGroupBox.setGeometry(QtCore.QRect(30, 10, 541, 461))
        self.appGroupBox.setMinimumSize(QtCore.QSize(80, 350))
        self.appGroupBox.setObjectName(_fromUtf8("appGroupBox"))
        self.gridLayout_app = QtGui.QGridLayout(self.appGroupBox)
        self.gridLayout_app.setMargin(0)
        self.gridLayout_app.setObjectName(_fromUtf8("gridLayout_app"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.convertAddressLineEdit = QtGui.QLineEdit(self.appGroupBox)
        self.convertAddressLineEdit.setObjectName(_fromUtf8("convertAddressLineEdit"))
        self.horizontalLayout_3.addWidget(self.convertAddressLineEdit)
        self.readConvertPushButton = QtGui.QPushButton(self.appGroupBox)
        self.readConvertPushButton.setObjectName(_fromUtf8("readConvertPushButton"))
        self.horizontalLayout_3.addWidget(self.readConvertPushButton)
        self.protocol_comboBox = QtGui.QComboBox(self.appGroupBox)
        self.protocol_comboBox.setObjectName(_fromUtf8("protocol_comboBox"))
        self.protocol_comboBox.addItem(_fromUtf8(""))
        self.protocol_comboBox.addItem(_fromUtf8(""))
        self.protocol_comboBox.addItem(_fromUtf8(""))
        self.horizontalLayout_3.addWidget(self.protocol_comboBox)
        self.label = QtGui.QLabel(self.appGroupBox)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_3.addWidget(self.label)
        self.readMeterSpanLineEdit = QtGui.QLineEdit(self.appGroupBox)
        self.readMeterSpanLineEdit.setObjectName(_fromUtf8("readMeterSpanLineEdit"))
        self.horizontalLayout_3.addWidget(self.readMeterSpanLineEdit)
        spacerItem = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.stopButton = QtGui.QPushButton(self.appGroupBox)
        self.stopButton.setObjectName(_fromUtf8("stopButton"))
        self.horizontalLayout_3.addWidget(self.stopButton)
        self.startButton = QtGui.QPushButton(self.appGroupBox)
        self.startButton.setObjectName(_fromUtf8("startButton"))
        self.horizontalLayout_3.addWidget(self.startButton)
        self.gridLayout_app.addLayout(self.horizontalLayout_3, 1, 0, 1, 1)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tableWidget = QtGui.QTableWidget(self.appGroupBox)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        self.verticalLayout.addWidget(self.tableWidget)
        self.gridLayout_app.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.appGroupBox.setTitle(_translate("Form", "工作区", None))
        self.readConvertPushButton.setText(_translate("Form", "抄读转换器地址", None))
        self.protocol_comboBox.setItemText(0, _translate("Form", "188", None))
        self.protocol_comboBox.setItemText(1, _translate("Form", "645_07", None))
        self.protocol_comboBox.setItemText(2, _translate("Form", "645_97", None))
        self.label.setText(_translate("Form", "抄读时间间隔", None))
        self.readMeterSpanLineEdit.setText(_translate("Form", "7", None))
        self.stopButton.setText(_translate("Form", "开始", None))
        self.startButton.setText(_translate("Form", "暂停", None))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", "表地址", None))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Form", "状态", None))

