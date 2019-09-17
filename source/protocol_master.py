# encoding:utf-8
import sys
from PyQt5.QtWidgets import *
from plug import plugs_get_all
from protocol_master_ui import Ui_MainWindow
import logging
import ui
import media


class ESMainWindow(QMainWindow, Ui_MainWindow):
    """
       管理插件、信道、和协议。
    """
    def __init__(self):
        super(ESMainWindow, self).__init__()
        self.setupUi(self)
        self.plugs = plugs_get_all()
        self.plugIndexContainer = QStackedWidget()
        self.install_plugs()
        self.medias = media.get_media_instances()
        self.init_menu()

    def install_plugs(self):
        self.plugIndexContainer.setMinimumHeight(375)
        for plug in self.plugs:
            widget = QTreeWidgetItem(self.treeWidget)
            widget.setText(0, plug.name)
            self.plugIndexContainer.addWidget(plug)
        self.splitter_v.insertWidget(0, self.plugIndexContainer)
        self.plugIndexContainer.setCurrentIndex(0)

    def init_menu(self):
        action = QAction(u"通信参数", self)
        action.setShortcut("Ctrl+R")
        action.triggered.connect(self.show_media_config)
        self.menuSet.addAction(action)
        self.toolbar.addAction(action)

    def plug_index_clicked(self, index):
        self.plugIndexContainer.setCurrentIndex(index.row())

    def show_media_error(self, msg):
        QMessageBox.information(self, u"串口错误", msg)

    def show_media_config(self):
        if len(self.medias) > 0:
            ui.get_user_options(self.medias[0])
        else:
            QMessageBox.information(u"没有可以用使用的通信设施")


def protocol_master_run():
    app = QApplication(sys.argv)
    ex = ESMainWindow()
    ex.move((QApplication.desktop().width() - ex.width()) / 2, (QApplication.desktop().height() - ex.height()) / 2);
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    protocol_master_run()
