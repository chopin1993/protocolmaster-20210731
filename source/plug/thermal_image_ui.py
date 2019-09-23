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
        Form.resize(728, 550)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.gridLayout_2 = QtWidgets.QGridLayout(Form)
        self.gridLayout_2.setContentsMargins(-1, 15, 15, 25)
        self.gridLayout_2.setSpacing(15)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.groupBox = QtWidgets.QGroupBox(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setVerticalSpacing(12)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.timespanLineeidt = QtWidgets.QLineEdit(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.timespanLineeidt.sizePolicy().hasHeightForWidth())
        self.timespanLineeidt.setSizePolicy(sizePolicy)
        self.timespanLineeidt.setObjectName("timespanLineeidt")
        self.gridLayout.addWidget(self.timespanLineeidt, 0, 1, 1, 1)
        self.stopButton = QtWidgets.QPushButton(self.groupBox)
        self.stopButton.setObjectName("stopButton")
        self.gridLayout.addWidget(self.stopButton, 1, 0, 1, 1)
        self.startButton = QtWidgets.QPushButton(self.groupBox)
        self.startButton.setObjectName("startButton")
        self.gridLayout.addWidget(self.startButton, 1, 1, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox, 2, 1, 1, 1, QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        self.gridLayout_2.addItem(spacerItem, 3, 1, 1, 1)
        self.image = QtWidgets.QWidget(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.image.sizePolicy().hasHeightForWidth())
        self.image.setSizePolicy(sizePolicy)
        self.image.setObjectName("image")
        self.gridLayout_2.addWidget(self.image, 0, 0, 4, 1)
        self.readImageButton = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.readImageButton.sizePolicy().hasHeightForWidth())
        self.readImageButton.setSizePolicy(sizePolicy)
        self.readImageButton.setObjectName("readImageButton")
        self.gridLayout_2.addWidget(self.readImageButton, 1, 1, 1, 1, QtCore.Qt.AlignLeft)

        self.retranslateUi(Form)
        self.readImageButton.clicked.connect(Form.readImageOnce)
        self.startButton.clicked.connect(Form.startRead)
        self.stopButton.clicked.connect(Form.stopRead)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupBox.setTitle(_translate("Form", "循环读取"))
        self.label.setText(_translate("Form", "时间间隔"))
        self.timespanLineeidt.setText(_translate("Form", "500"))
        self.stopButton.setText(_translate("Form", "停止"))
        self.startButton.setText(_translate("Form", "开始"))
        self.readImageButton.setText(_translate("Form", "单次读取热度图"))
