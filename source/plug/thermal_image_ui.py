# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'thermal_image_ui.ui'
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
        self.groupBox_2 = QtWidgets.QGroupBox(Form)
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(self.groupBox_2)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.tagLineEdit = QtWidgets.QLineEdit(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tagLineEdit.sizePolicy().hasHeightForWidth())
        self.tagLineEdit.setSizePolicy(sizePolicy)
        self.tagLineEdit.setObjectName("tagLineEdit")
        self.horizontalLayout.addWidget(self.tagLineEdit)
        self.gridLayout_2.addWidget(self.groupBox_2, 0, 1, 1, 1)
        self.image = QtWidgets.QWidget(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.image.sizePolicy().hasHeightForWidth())
        self.image.setSizePolicy(sizePolicy)
        self.image.setObjectName("image")
        self.gridLayout_2.addWidget(self.image, 0, 0, 10, 1)
        self.readImageButton = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.readImageButton.sizePolicy().hasHeightForWidth())
        self.readImageButton.setSizePolicy(sizePolicy)
        self.readImageButton.setObjectName("readImageButton")
        self.gridLayout_2.addWidget(self.readImageButton, 1, 1, 1, 1)
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
        self.gridLayout.addWidget(self.stopButton, 2, 0, 1, 1)
        self.startButton = QtWidgets.QPushButton(self.groupBox)
        self.startButton.setObjectName("startButton")
        self.gridLayout.addWidget(self.startButton, 2, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox, 2, 1, 1, 1)
        self.showdataGroup = QtWidgets.QGroupBox(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.showdataGroup.sizePolicy().hasHeightForWidth())
        self.showdataGroup.setSizePolicy(sizePolicy)
        self.showdataGroup.setObjectName("showdataGroup")
        self.formLayout = QtWidgets.QFormLayout(self.showdataGroup)
        self.formLayout.setObjectName("formLayout")
        self.label_3 = QtWidgets.QLabel(self.showdataGroup)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.rowidLineEdit = QtWidgets.QLineEdit(self.showdataGroup)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rowidLineEdit.sizePolicy().hasHeightForWidth())
        self.rowidLineEdit.setSizePolicy(sizePolicy)
        self.rowidLineEdit.setObjectName("rowidLineEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.rowidLineEdit)
        self.label_4 = QtWidgets.QLabel(self.showdataGroup)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.idxLineEdit = QtWidgets.QLineEdit(self.showdataGroup)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.idxLineEdit.sizePolicy().hasHeightForWidth())
        self.idxLineEdit.setSizePolicy(sizePolicy)
        self.idxLineEdit.setObjectName("idxLineEdit")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.idxLineEdit)
        self.searchPushButton = QtWidgets.QPushButton(self.showdataGroup)
        self.searchPushButton.setObjectName("searchPushButton")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.searchPushButton)
        self.playPushButton = QtWidgets.QPushButton(self.showdataGroup)
        self.playPushButton.setObjectName("playPushButton")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.playPushButton)
        self.gridLayout_2.addWidget(self.showdataGroup, 3, 1, 1, 1)

        self.retranslateUi(Form)
        self.readImageButton.clicked.connect(Form.readImageOnce)
        self.startButton.clicked.connect(Form.startRead)
        self.stopButton.clicked.connect(Form.stopRead)
        self.searchPushButton.clicked.connect(Form.searchImage)
        self.playPushButton.clicked.connect(Form.playImage)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupBox_2.setTitle(_translate("Form", "数据标签"))
        self.label_2.setText(_translate("Form", "tag"))
        self.tagLineEdit.setText(_translate("Form", "test"))
        self.readImageButton.setText(_translate("Form", "单次读取热度图"))
        self.groupBox.setTitle(_translate("Form", "读取"))
        self.timespanLineeidt.setText(_translate("Form", "700"))
        self.stopButton.setText(_translate("Form", "停止"))
        self.startButton.setText(_translate("Form", "开始"))
        self.label.setText(_translate("Form", "时间间隔"))
        self.showdataGroup.setTitle(_translate("Form", "数据查看"))
        self.label_3.setText(_translate("Form", "rowid"))
        self.label_4.setText(_translate("Form", "idx"))
        self.searchPushButton.setText(_translate("Form", "查找"))
        self.playPushButton.setText(_translate("Form", "play"))
