# encoding:utf-8
import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from plug import plugs_get_all
from protocol_master_ui import Ui_MainWindow
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
        self.current_media = self.medias[0]
        self.get_current_media().error.connect(self.show_error)
        self.init_menu()
        self.protocols = protocol.get_all_protocol_instance()
        self.session = None
        self.session = session.SessionSuit.create_binary_suit(self.get_current_media(), self.get_current_protocol())
        self.plugs = plugs_get_all()
        self.plugIndexContainer = QStackedWidget()
        self.install_plugs()
        self.session.data_ready.connect(self.get_current_plug().handle_receive_data)
        self.session.data_snd.connect(self.log_snd_frame)
        self.session.data_ready.connect(self.log_rcv_frame)
        self.session.data_clean.connect(self.log_rcv_frame)
        self.log_idx = 0
        self.tableWidgetFrame.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableWidgetFrame.setColumnWidth(0, 95)
        self.tableWidgetFrame.setColumnWidth(1, 35)

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

    def init_menu(self):
        action = QAction(u"通信参数", self)
        action.setShortcut("Ctrl+R")
        action.triggered.connect(self.show_media_config)
        self.menuSet.addAction(action)
        self.toolbar.addAction(action)
        action = QAction(u"协议", self)
        action.setShortcut("Ctrl+R")
        action.triggered.connect(self.show_protocol_config)
        self.menuSet.addAction(action)
        self.toolbar.addAction(action)

    def plug_index_clicked(self, index):
        self.plugIndexContainer.setCurrentIndex(index.row())

    def show_media_config(self):
        if len(self.medias) > 0:
            def ok_func(meida):
                self.current_media = meida
                self.update_session()
            ui.show_user_media_options(self.medias, ok_func)
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
            QMessageBox.information(None, u"错误", u"没有可以用使用的协议")

    @staticmethod
    def show_error(msg):
        QMessageBox.information(None, u"错误", msg)

    def log_snd_frame(self, protocol):
        self._add_log_info("snd",str(protocol))

    def log_rcv_frame(self, protocol):
        self._add_log_info("rcv", str(protocol))

    def _add_log_info(self,tag, info):
        self.log_idx += 1
        self.tableWidgetFrame.setRowCount(self.log_idx)
        time = QtCore.QDateTime.currentDateTime()
        time_display = time.toString("MM-dd hh:mm:ss")
        widget = QTableWidgetItem(time_display)
        self.tableWidgetFrame.setItem(self.log_idx-1, 0, widget)
        widget = QTableWidgetItem(tag)
        self.tableWidgetFrame.setItem(self.log_idx-1, 1, widget)
        widget = QTableWidgetItem(info)
        self.tableWidgetFrame.setItem(self.log_idx-1, 2, widget)

    def get_current_media(self):
        return self.current_media

    def get_current_protocol(self):
        return self.protocols[0]

    def get_current_plug(self):
        return self.plugs[0]


def protocol_master_run():
    app = QApplication(sys.argv)
    ex = ESMainWindow()
    ex.show_media_config()
    ex.move((QApplication.desktop().width() - ex.width())/2, (QApplication.desktop().height() - ex.height()) / 2);
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    protocol_master_run()
