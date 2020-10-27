from case_editor_ui import Ui_MainWindow
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import re

class CaseEditor(QMainWindow, Ui_MainWindow):
    def __init__(self, engine):
        super(CaseEditor, self).__init__()
        self.tree_widgets = []
        self.engine = engine
        self.setupUi(self)
        self.test_infos = self.engine.all_infos
        self.init_tree()
        self.saveConfigButton.clicked.connect(self.save_config)
        self.runAllPushButton.clicked.connect(self.run_all_test)
        self.testCaseView.itemClicked.connect(self.item_clicked)
        self.applyPushButton.clicked.connect(self.filter)
        self.current_widget = None

    def filter(self):
        regs = self.filterLineEdit.text()
        if regs is "":
            regs = ".*"
        for widget in self.tree_widgets:
            case = widget.case
            if re.match(regs,case.name):
                widget.setHidden(False)
            else:
                widget.setHidden(True)

    def sync_status(self):
        for widget in self.tree_widgets:
            case = widget.case
            case.set_enable(widget.checkState(0) == Qt.Checked)

    def save_config(self):
        self.sync_status()
        if self.engine.is_exist_config():
            ret = QMessageBox.information(self,"配置保存", "已经存在配置文件，要覆盖吗？",QMessageBox.Yes|QMessageBox.No)
            if ret == QMessageBox.Yes:
                self.engine.save_config()
        else:
            self.engine.save_config()

    def run_all_test(self):
        self.sync_status()
        self.engine.run_all_test()
        QMessageBox.information(None, u"测试完成","请查看测试报告")

    def item_clicked(self, widget):
        self.current_widget = widget
        case = widget.case
        brief = case.brief if case.brief else "没有简介"
        self.briefTextBrowser.setText(brief)
        child_cnt = widget.childCount()
        status = widget.checkState(0)
        for idx in range(child_cnt):
            child = widget.child(idx)
            child.setCheckState(0, status)

    def init_tree(self):
        for group in self.test_infos:
           widget = QTreeWidgetItem(self.testCaseView)
           widget.setText(0, group.name)
           value = Qt.Checked if group.is_enable() else Qt.Unchecked
           widget.setCheckState(0, value)
           widget.case = group
           self.tree_widgets.append(widget)
           for case in group.subcases:
               case_wdiget = QTreeWidgetItem(widget)
               case_wdiget.setText(0, case.name)
               value = Qt.Checked if case.is_enable() else Qt.Unchecked
               case_wdiget.setCheckState(0, value)
               case_wdiget.case = case
               self.tree_widgets.append(case_wdiget)



