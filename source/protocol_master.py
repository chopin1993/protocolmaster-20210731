# encoding:utf-8
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from plug import plugs_get_all
from protocol_master_ui import Ui_MainWindow
import ui
import media
import protocol
import session
import datetime
from ESSetting import ESSetting


class ESMainWindow(QMainWindow, Ui_MainWindow):
    """
       管理插件、信道、和协议。
    """
    def __init__(self):
        super(ESMainWindow, self).__init__()
        self.setupUi(self)
        self.setting = ESSetting.instance()
        self.medias_dict = media.get_media_instances()
        self.protocols_dict = protocol.get_all_protocol_instance()
        self.init_menu()
        self.plugIndexContainer = QStackedWidget()
        self.plugs = plugs_get_all()
        self.session = session.SessionSuit.create_binary_suit(self.get_current_media(), self.get_current_protocol())
        self.session.data_snd.connect(self.log_snd_frame)
        self.session.data_ready.connect(self.log_rcv_frame)
        self.session.data_clean.connect(self.log_rcv_frame)

        self.install_plugs()

        self.log_idx = 0
        self.tableWidgetFrame.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableWidgetFrame.setColumnWidth(0, 95)
        self.tableWidgetFrame.setColumnWidth(1, 35)
        self.tableWidgetFrame.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tableWidgetFrame.customContextMenuRequested.connect(self.log_tablewidgit_menu)
        self.status_bar_timer = QTimer(self)
        self.status_bar_timer.timeout.connect(self.update_status_bar)
        self.status_bar_timer.start(1000)
        self.sync_plug(-1)
        self.plugIndexContainer.setCurrentIndex(self.setting.get_plug_idx())
        self.sync_media(None)

    def sync_plug(self, idx):
        if idx >= 0:
            self.session.data_ready.disconnect()
            self.setting.set_plug_idx(idx)
        self.session.protocol = self.get_current_protocol()
        self.session.data_ready.connect(self.get_current_plug().handle_receive_data)

    def sync_media(self, key):
        if key is not None:
            self.get_current_media().error.disconnect()
            self.setting.set_media_key(key)
        self.session.media = self.get_current_media()
        self.session.media.error.connect(self.show_error)

    def update_status_bar(self):
        message = self.session.status_message()
        self.statusBar.showMessage(message)

    def log_tablewidgit_menu(self,pos):
        menu = QMenu()
        clear = menu.addAction("清空")
        action = menu.exec_(self.tableWidgetFrame.mapToGlobal(pos))
        if action == clear:
            self.clear_log_info()
            return
        else:
            return

    def install_plugs(self):
        self.plugIndexContainer.setMinimumHeight(475)
        for plug in self.plugs:
            widget = QTreeWidgetItem(self.treeWidget)
            widget.setText(0, plug.name)
            self.plugIndexContainer.addWidget(plug)
            plug.session = self.session
            protocols = plug.get_protocols()
            for pro in protocols:
                assert pro in self.protocols_dict
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
        idx = index
        if not isinstance(index, int):
            idx = index.row()
        if self.setting.get_plug_idx() != idx:
            self.plugIndexContainer.setCurrentIndex(idx)
            self.sync_plug(idx)

    def show_media_config(self):
        if len(self.medias_dict) > 0:
            self.session.media = self.get_current_media()
            def ok_func(media):
                if self.get_current_media() != media:
                    self.sync_media(media.name)
            ui.show_user_media_options(list(self.medias_dict.values()), ok_func)
        else:
            QMessageBox.information(None, "错误", u"没有可以用使用的信道")

    def show_protocol_config(self):
        if len(self.protocols_dict) > 0:
            def ok_func(protocol, options):
                pass
            options = list()
            for pros in self.protocols_dict:
                 options.append(pros.name)
            ui.show_user_options([media.MediaOptions(u"协议",options)],ok_func)
            self.update_session()
        else:
            QMessageBox.information(None, u"错误", u"没有可以用使用的协议")

    def show_error(self, msg):
        QMessageBox.information(None, u"错误", msg)
        self.get_current_plug().media_error_happen()

    def log_snd_frame(self, protocol):
        self._add_log_info("snd",str(protocol))

    def log_rcv_frame(self, protocol):
        self._add_log_info("rcv", str(protocol))

    def _add_log_info(self,tag, info):
        self.log_idx += 1
        self.tableWidgetFrame.setRowCount(self.log_idx)
        time_display = datetime.datetime.now().strftime('%m-%d %H:%M:%S.%f')
        widget = QTableWidgetItem(time_display)
        self.tableWidgetFrame.setItem(self.log_idx-1, 0, widget)
        widget = QTableWidgetItem(tag)
        self.tableWidgetFrame.setItem(self.log_idx-1, 1, widget)
        widget = QTableWidgetItem(info)
        self.tableWidgetFrame.setItem(self.log_idx-1, 2, widget)
        if self.log_idx > 50000:
            self.clear_log_info()

    def clear_log_info(self):
        self.tableWidgetFrame.setRowCount(0)
        self.log_idx = 0

    def get_current_media(self):
        key = list(self.medias_dict.keys())[0]
        return self.medias_dict[self.setting.get_media_key(key)]

    def get_current_protocol(self):
        keys = self.plugs[self.setting.get_plug_idx()].get_protocols()
        if len(keys) > 0:
            return self.protocols_dict[keys[0]]
        else:
            return list(self.protocols_dict.values())[0]

    def get_current_plug(self):
        return self.plugs[self.setting.get_plug_idx()]


def protocol_master_run():
    app = QApplication(sys.argv)
    ex = ESMainWindow()
    ex.show_media_config()
    ex.move((QApplication.desktop().width() - ex.width())/2, (QApplication.desktop().height() - ex.height()) / 2);
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    protocol_master_run()