from case_editor_ui import Ui_MainWindow
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon

class CaseEditor(QMainWindow, Ui_MainWindow):
    def __init__(self, engine):
        super(CaseEditor, self).__init__()
        self.engine = engine
        self.setupUi(self)
        self.test_infos = self.engine.test_infos
        self.init_tree()

    def init_tree(self):
        self.testCaseView.setColumnWidth(0,150)
        self.testCaseView.setColumnWidth(2, 40)

        for group in self.test_infos:
           widget = QTreeWidgetItem(self.testCaseView)
           widget.setText(0, group.name)
           widget.setCheckState(0,Qt.Checked)
           button = QPushButton("运行")
           button.setMaximumWidth(40)
           self.testCaseView.setItemWidget(widget,2, button)
           for case in group.subcases:
               case_wdiget = QTreeWidgetItem(widget)
               case_wdiget.setText(0, case.name)
               case_wdiget.setCheckState(0,Qt.Checked)
               button = QPushButton("运行")
               # background-image
               #button.setStyleSheet("QPushButton{border-image: url(resource/run.png)}")
               button.setMaximumWidth(40)
               self.testCaseView.setItemWidget(case_wdiget, 2, button)


