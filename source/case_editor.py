from case_editor_ui import Ui_MainWindow
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import re
import sip

class CaseEditor(QMainWindow, Ui_MainWindow):
    def __init__(self, engine):
        super(CaseEditor, self).__init__()
        self.all_tree_widgets = []
        self.top_tree_widgets = []
        self.engine = engine
        self.setupUi(self)
        self.test_infos = self.engine.all_infos
        self.init_tree()
        self.saveConfigButton.clicked.connect(self.save_config)
        self.runAllPushButton.clicked.connect(self.run_all_test)
        self.testCaseView.itemClicked.connect(self.item_clicked)
        self.applyPushButton.clicked.connect(self.filter)
        self.current_widget = None
        self.para_widgets = []
        layout = QVBoxLayout()
        self.paraContainerWidget.setLayout(layout)

    def filter(self):
        regs = self.filterLineEdit.text()
        if regs is "":
            regs = ".*"
        for top_widget in self.all_tree_widgets:
            top_status = False
            case = top_widget.case
            child_cnt = top_widget.childCount()
            if re.match(regs, case.name):
                top_status = True
            for idx in range(child_cnt):
                child = top_widget.child(idx)
                case = child.case
                if re.match(regs, case.name):
                    child.setHidden(False)
                    top_status = True
                else:
                    child.setHidden(True)

            top_widget.setHidden(not top_status)

    def sync_status(self):
        for widget in self.all_tree_widgets:
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

    def item_clicked(self, tree_widget_item):
        self.current_widget = tree_widget_item
        case = tree_widget_item.case
        brief = case.brief if case.brief else "没有简介"
        self.briefTextBrowser.setText(brief)

        for para_widget in self.para_widgets:
            self.paraContainerWidget.layout().removeWidget(para_widget)
            para_widget.hide()

        self.para_widgets = case.get_para_widgets()

        for para_widget in self.para_widgets:
            self.paraContainerWidget.layout().addWidget(para_widget)
            para_widget.show()


        child_cnt = tree_widget_item.childCount()
        status = tree_widget_item.checkState(0)
        for idx in range(child_cnt):
            child = tree_widget_item.child(idx)
            child.setCheckState(0, status)

    def init_tree(self):
        for group in self.test_infos:
           widget = QTreeWidgetItem(self.testCaseView)
           widget.setText(0, group.name)
           value = Qt.Checked if group.is_enable() else Qt.Unchecked
           widget.setCheckState(0, value)
           widget.case = group
           self.all_tree_widgets.append(widget)
           self.top_tree_widgets.append(widget)
           for case in group.subcases:
               case_wdiget = QTreeWidgetItem(widget)
               case_wdiget.setText(0, case.name)
               value = Qt.Checked if case.is_enable() else Qt.Unchecked
               case_wdiget.setCheckState(0, value)
               case_wdiget.case = case
               self.all_tree_widgets.append(case_wdiget)



