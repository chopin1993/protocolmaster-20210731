# encoding:utf-8
import sys
from PyQt5.QtWidgets import *
from plug import plugs_get_all
from protocol_master_ui import Ui_MainWindow
import logging
import ui
import media
import protocol
import session

class ESMainWindow(QMainWindow, Ui_MainWindow):
    """
       管理插件、信道、和协议。
    """
    def __init__(self):
        super(ESMainWindow, self).__init__()
        self.setupUi(self)
        self.medias = media.get_media_instances()
        self.init_menu()
        self.protocols = protocol.get_all_protocol_instance()
        self.session = None
        self.session = session.SessionSuit.create_binary_suit(self.get_current_media(), self.get_current_protocol())
        self.plugs = plugs_get_all()
        self.plugIndexContainer = QStackedWidget()
        self.install_plugs()

    def update_session(self):
        self.session.media =  self.get_current_media()
        self.session.protocol = self.get_current_protocol()

    def install_plugs(self):
        self.plugIndexContainer.setMinimumHeight(375)
        for plug in self.plugs:
            widget = QTreeWidgetItem(self.treeWidget)
            widget.setText(0, plug.name)
            self.plugIndexContainer.addWidget(plug)
            plug.session = self.session
        self.splitter_v.insertWidget(0, self.plugIndexContainer)
        self.plugIndexContainer.setCurrentIndex(0)

    def init_menu(self):
        action = QAction(u"通信参数", self)
        action.setShortcut("Ctrl+R")
        action.triggered.connect(self.show_media_config)
        self.menuSet.addAction(action)
        action = QAction(u"协议", self)
        action.setShortcut("Ctrl+R")
        action.triggered.connect(self.show_protocol_config)
        self.menuSet.addAction(action)

    def plug_index_clicked(self, index):
        self.plugIndexContainer.setCurrentIndex(index.row())

    def show_media_config(self):
        if len(self.medias) > 0:
            ui.show_user_media_options(self.medias[0])
            self.update_session()
        else:
            QMessageBox.information(None, "错误", u"没有可以用使用的信道")

    def show_protocol_config(self):
        if len(self.protocols) > 0:
            def ok_func(options):
                pass
            options = list()
            for pros in self.protocols:
                 options.append(pros.name)
            ui.show_user_options([media.MediaOptions(u"协议",options)],ok_func)
            self.update_session()
        else:
            QMessageBox.information(None, "错误" , u"没有可以用使用的协议")

    def get_current_media(self):
        return self.medias[0]

    def get_current_protocol(self):
        return self.protocols[0]

def protocol_master_run():
    app = QApplication(sys.argv)
    ex = ESMainWindow()
    ex.show_media_config()
    ex.move((QApplication.desktop().width() - ex.width()) / 2, (QApplication.desktop().height() - ex.height()) / 2);
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    protocol_master_run()
