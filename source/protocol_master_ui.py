# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'protocol_master_ui.ui'
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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(964, 645)
        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.centralWidget)
        self.horizontalLayout_2.setMargin(11)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.splitter_h = QtGui.QSplitter(self.centralWidget)
        self.splitter_h.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_h.setOpaqueResize(True)
        self.splitter_h.setHandleWidth(5)
        self.splitter_h.setChildrenCollapsible(False)
        self.splitter_h.setObjectName(_fromUtf8("splitter_h"))
        self.treeWidget = QtGui.QTreeWidget(self.splitter_h)
        self.treeWidget.setEnabled(True)
        self.treeWidget.setMaximumSize(QtCore.QSize(200, 16777215))
        self.treeWidget.setObjectName(_fromUtf8("treeWidget"))
        self.treeWidget.headerItem().setText(0, _fromUtf8("1"))
        self.splitter_v = QtGui.QSplitter(self.splitter_h)
        self.splitter_v.setFrameShape(QtGui.QFrame.NoFrame)
        self.splitter_v.setFrameShadow(QtGui.QFrame.Plain)
        self.splitter_v.setMidLineWidth(1)
        self.splitter_v.setOrientation(QtCore.Qt.Vertical)
        self.splitter_v.setObjectName(_fromUtf8("splitter_v"))
        self.appGroupBox = QtGui.QGroupBox(self.splitter_v)
        self.appGroupBox.setMinimumSize(QtCore.QSize(80, 350))
        self.appGroupBox.setObjectName(_fromUtf8("appGroupBox"))
        self.gridLayout_app = QtGui.QGridLayout(self.appGroupBox)
        self.gridLayout_app.setMargin(0)
        self.gridLayout_app.setSpacing(6)
        self.gridLayout_app.setObjectName(_fromUtf8("gridLayout_app"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setMargin(11)
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.convertAddressLineEdit = QtGui.QLineEdit(self.appGroupBox)
        self.convertAddressLineEdit.setObjectName(_fromUtf8("convertAddressLineEdit"))
        self.horizontalLayout_3.addWidget(self.convertAddressLineEdit)
        self.readConvertPushButton = QtGui.QPushButton(self.appGroupBox)
        self.readConvertPushButton.setObjectName(_fromUtf8("readConvertPushButton"))
        self.horizontalLayout_3.addWidget(self.readConvertPushButton)
        self.is645checkBox = QtGui.QCheckBox(self.appGroupBox)
        self.is645checkBox.setObjectName(_fromUtf8("is645checkBox"))
        self.horizontalLayout_3.addWidget(self.is645checkBox)
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
        self.verticalLayout.setMargin(11)
        self.verticalLayout.setSpacing(6)
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
        self.tabWidget = QtGui.QTabWidget(self.splitter_v)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tabFrame = QtGui.QWidget()
        self.tabFrame.setObjectName(_fromUtf8("tabFrame"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.tabFrame)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.tableWidgetFrame = QtGui.QTableWidget(self.tabFrame)
        self.tableWidgetFrame.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.tableWidgetFrame.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tableWidgetFrame.setAlternatingRowColors(True)
        self.tableWidgetFrame.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.tableWidgetFrame.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableWidgetFrame.setObjectName(_fromUtf8("tableWidgetFrame"))
        self.tableWidgetFrame.setColumnCount(3)
        self.tableWidgetFrame.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tableWidgetFrame.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidgetFrame.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidgetFrame.setHorizontalHeaderItem(2, item)
        self.tableWidgetFrame.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidgetFrame.horizontalHeader().setStretchLastSection(True)
        self.tableWidgetFrame.verticalHeader().setVisible(False)
        self.horizontalLayout.addWidget(self.tableWidgetFrame)
        self.textBrowserFrameInfo = QtGui.QTextBrowser(self.tabFrame)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Consolas"))
        font.setKerning(False)
        self.textBrowserFrameInfo.setFont(font)
        self.textBrowserFrameInfo.setObjectName(_fromUtf8("textBrowserFrameInfo"))
        self.horizontalLayout.addWidget(self.textBrowserFrameInfo)
        self.tabWidget.addTab(self.tabFrame, _fromUtf8(""))
        self.tabLog = QtGui.QWidget()
        self.tabLog.setObjectName(_fromUtf8("tabLog"))
        self.gridLayout = QtGui.QGridLayout(self.tabLog)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.textBrowser = QtGui.QTextBrowser(self.tabLog)
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.gridLayout.addWidget(self.textBrowser, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tabLog, _fromUtf8(""))
        self.horizontalLayout_2.addWidget(self.splitter_h)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtGui.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 964, 23))
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        self.menuSet = QtGui.QMenu(self.menuBar)
        self.menuSet.setObjectName(_fromUtf8("menuSet"))
        self.menuHelp = QtGui.QMenu(self.menuBar)
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        self.menuTools = QtGui.QMenu(self.menuBar)
        self.menuTools.setObjectName(_fromUtf8("menuTools"))
        MainWindow.setMenuBar(self.menuBar)
        self.toolbar = QtGui.QToolBar(MainWindow)
        self.toolbar.setObjectName(_fromUtf8("toolbar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolbar)
        self.statusBar = QtGui.QStatusBar(MainWindow)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        MainWindow.setStatusBar(self.statusBar)
        self.openDatabaseAction = QtGui.QAction(MainWindow)
        self.openDatabaseAction.setObjectName(_fromUtf8("openDatabaseAction"))
        self.exportDatabaseAction = QtGui.QAction(MainWindow)
        self.exportDatabaseAction.setObjectName(_fromUtf8("exportDatabaseAction"))
        self.action = QtGui.QAction(MainWindow)
        self.action.setObjectName(_fromUtf8("action"))
        self.menuSet.addAction(self.action)
        self.menuBar.addAction(self.menuSet.menuAction())
        self.menuBar.addAction(self.menuTools.menuAction())
        self.menuBar.addAction(self.menuHelp.menuAction())
        self.toolbar.addSeparator()

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.stopButton, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.start)
        QtCore.QObject.connect(self.startButton, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.stop)
        QtCore.QObject.connect(self.readConvertPushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.read_convert_address)
        QtCore.QObject.connect(self.is645checkBox, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), MainWindow.is645Taggle)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "智能硬件测试工具", None))
        self.appGroupBox.setTitle(_translate("MainWindow", "工作区", None))
        self.readConvertPushButton.setText(_translate("MainWindow", "抄读转换器地址", None))
        self.is645checkBox.setText(_translate("MainWindow", "645", None))
        self.label.setText(_translate("MainWindow", "抄读时间间隔", None))
        self.readMeterSpanLineEdit.setText(_translate("MainWindow", "7", None))
        self.stopButton.setText(_translate("MainWindow", "开始", None))
        self.startButton.setText(_translate("MainWindow", "暂停", None))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "表地址", None))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "状态", None))
        item = self.tableWidgetFrame.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "时间", None))
        item = self.tableWidgetFrame.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "标记", None))
        item = self.tableWidgetFrame.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "数据", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabFrame), _translate("MainWindow", "帧信息", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabLog), _translate("MainWindow", "日志", None))
        self.menuSet.setTitle(_translate("MainWindow", "设置", None))
        self.menuHelp.setTitle(_translate("MainWindow", "帮助", None))
        self.menuTools.setTitle(_translate("MainWindow", "工具", None))
        self.openDatabaseAction.setText(_translate("MainWindow", "open", None))
        self.exportDatabaseAction.setText(_translate("MainWindow", "export", None))
        self.action.setText(_translate("MainWindow", "串口", None))

