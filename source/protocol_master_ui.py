# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'G:\ProtocolMaster\source\protocol_master_ui.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(964, 645)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.splitter_h = QtWidgets.QSplitter(self.centralWidget)
        self.splitter_h.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_h.setOpaqueResize(True)
        self.splitter_h.setHandleWidth(5)
        self.splitter_h.setChildrenCollapsible(False)
        self.splitter_h.setObjectName("splitter_h")
        self.treeWidget = QtWidgets.QTreeWidget(self.splitter_h)
        self.treeWidget.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.treeWidget.sizePolicy().hasHeightForWidth())
        self.treeWidget.setSizePolicy(sizePolicy)
        self.treeWidget.setMaximumSize(QtCore.QSize(200, 16777215))
        self.treeWidget.setObjectName("treeWidget")
        self.splitter_v = QtWidgets.QSplitter(self.splitter_h)
        self.splitter_v.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.splitter_v.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.splitter_v.setFrameShadow(QtWidgets.QFrame.Plain)
        self.splitter_v.setMidLineWidth(1)
        self.splitter_v.setOrientation(QtCore.Qt.Vertical)
        self.splitter_v.setObjectName("splitter_v")
        self.tabWidget = QtWidgets.QTabWidget(self.splitter_v)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setObjectName("tabWidget")
        self.tabFrame = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabFrame.sizePolicy().hasHeightForWidth())
        self.tabFrame.setSizePolicy(sizePolicy)
        self.tabFrame.setObjectName("tabFrame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.tabFrame)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tableWidgetFrame = QtWidgets.QTableWidget(self.tabFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidgetFrame.sizePolicy().hasHeightForWidth())
        self.tableWidgetFrame.setSizePolicy(sizePolicy)
        self.tableWidgetFrame.setMaximumSize(QtCore.QSize(16777215, 545))
        self.tableWidgetFrame.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.tableWidgetFrame.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidgetFrame.setAlternatingRowColors(True)
        self.tableWidgetFrame.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.tableWidgetFrame.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidgetFrame.setObjectName("tableWidgetFrame")
        self.tableWidgetFrame.setColumnCount(3)
        self.tableWidgetFrame.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidgetFrame.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidgetFrame.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidgetFrame.setHorizontalHeaderItem(2, item)
        self.tableWidgetFrame.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidgetFrame.horizontalHeader().setStretchLastSection(True)
        self.tableWidgetFrame.verticalHeader().setVisible(False)
        self.horizontalLayout.addWidget(self.tableWidgetFrame)
        self.textBrowserFrameInfo = QtWidgets.QTextBrowser(self.tabFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textBrowserFrameInfo.sizePolicy().hasHeightForWidth())
        self.textBrowserFrameInfo.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setKerning(False)
        self.textBrowserFrameInfo.setFont(font)
        self.textBrowserFrameInfo.setObjectName("textBrowserFrameInfo")
        self.horizontalLayout.addWidget(self.textBrowserFrameInfo)
        self.tabWidget.addTab(self.tabFrame, "")
        self.tabLog = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabLog.sizePolicy().hasHeightForWidth())
        self.tabLog.setSizePolicy(sizePolicy)
        self.tabLog.setObjectName("tabLog")
        self.gridLayout = QtWidgets.QGridLayout(self.tabLog)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.textBrowser = QtWidgets.QTextBrowser(self.tabLog)
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout.addWidget(self.textBrowser, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tabLog, "")
        self.verticalLayout.addWidget(self.splitter_h)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 964, 23))
        self.menuBar.setObjectName("menuBar")
        self.menuSet = QtWidgets.QMenu(self.menuBar)
        self.menuSet.setObjectName("menuSet")
        self.menuHelp = QtWidgets.QMenu(self.menuBar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuDevice = QtWidgets.QMenu(self.menuBar)
        self.menuDevice.setObjectName("menuDevice")
        MainWindow.setMenuBar(self.menuBar)
        self.toolbar = QtWidgets.QToolBar(MainWindow)
        self.toolbar.setObjectName("toolbar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolbar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.menuBar.addAction(self.menuSet.menuAction())
        self.menuBar.addAction(self.menuDevice.menuAction())
        self.menuBar.addAction(self.menuHelp.menuAction())
        self.toolbar.addSeparator()

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        self.treeWidget.clicked['QModelIndex'].connect(MainWindow.plug_index_clicked)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "智能硬件测试工具"))
        self.treeWidget.headerItem().setText(0, _translate("MainWindow", "APP名称"))
        item = self.tableWidgetFrame.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "时间"))
        item = self.tableWidgetFrame.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "标记"))
        item = self.tableWidgetFrame.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "数据"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabFrame), _translate("MainWindow", "帧信息"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabLog), _translate("MainWindow", "日志"))
        self.menuSet.setTitle(_translate("MainWindow", "设置"))
        self.menuHelp.setTitle(_translate("MainWindow", "帮助"))
        self.menuDevice.setTitle(_translate("MainWindow", "设备"))
