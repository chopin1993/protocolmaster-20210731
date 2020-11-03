# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'case_editor_ui.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(729, 556)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.header = QtWidgets.QWidget(self.centralwidget)
        self.header.setObjectName("header")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.header)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.header)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.filterLineEdit = QtWidgets.QLineEdit(self.header)
        self.filterLineEdit.setMaximumSize(QtCore.QSize(200, 16777215))
        self.filterLineEdit.setObjectName("filterLineEdit")
        self.horizontalLayout.addWidget(self.filterLineEdit)
        self.applyPushButton = QtWidgets.QPushButton(self.header)
        self.applyPushButton.setObjectName("applyPushButton")
        self.horizontalLayout.addWidget(self.applyPushButton)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.runAllPushButton = QtWidgets.QPushButton(self.header)
        self.runAllPushButton.setObjectName("runAllPushButton")
        self.horizontalLayout.addWidget(self.runAllPushButton)
        self.saveConfigButton = QtWidgets.QPushButton(self.header)
        self.saveConfigButton.setObjectName("saveConfigButton")
        self.horizontalLayout.addWidget(self.saveConfigButton)
        self.verticalLayout.addWidget(self.header)
        self.lowWidget = QtWidgets.QWidget(self.centralwidget)
        self.lowWidget.setObjectName("lowWidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.lowWidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.testCaseView = QtWidgets.QTreeWidget(self.lowWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(5)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.testCaseView.sizePolicy().hasHeightForWidth())
        self.testCaseView.setSizePolicy(sizePolicy)
        self.testCaseView.setColumnCount(1)
        self.testCaseView.setObjectName("testCaseView")
        self.testCaseView.header().setMinimumSectionSize(60)
        self.horizontalLayout_2.addWidget(self.testCaseView)
        self.caseContainer = QtWidgets.QWidget(self.lowWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(8)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.caseContainer.sizePolicy().hasHeightForWidth())
        self.caseContainer.setSizePolicy(sizePolicy)
        self.caseContainer.setMinimumSize(QtCore.QSize(200, 0))
        self.caseContainer.setObjectName("caseContainer")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.caseContainer)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.paraContainerWidget = QtWidgets.QWidget(self.caseContainer)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(4)
        sizePolicy.setHeightForWidth(self.paraContainerWidget.sizePolicy().hasHeightForWidth())
        self.paraContainerWidget.setSizePolicy(sizePolicy)
        self.paraContainerWidget.setObjectName("paraContainerWidget")
        self.verticalLayout_2.addWidget(self.paraContainerWidget)
        self.briefTextBrowser = QtWidgets.QTextBrowser(self.caseContainer)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(4)
        sizePolicy.setHeightForWidth(self.briefTextBrowser.sizePolicy().hasHeightForWidth())
        self.briefTextBrowser.setSizePolicy(sizePolicy)
        self.briefTextBrowser.setObjectName("briefTextBrowser")
        self.verticalLayout_2.addWidget(self.briefTextBrowser)
        self.horizontalLayout_2.addWidget(self.caseContainer)
        self.verticalLayout.addWidget(self.lowWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 729, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "过滤器"))
        self.applyPushButton.setText(_translate("MainWindow", "应用"))
        self.runAllPushButton.setText(_translate("MainWindow", "运行选中测试"))
        self.saveConfigButton.setText(_translate("MainWindow", "保存配置"))
        self.testCaseView.headerItem().setText(0, _translate("MainWindow", "测试项"))
