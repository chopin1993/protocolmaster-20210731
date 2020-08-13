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
from database import EsDatabase


class ESMainWindow(QMainWindow, Ui_MainWindow):
    PLUG_INDEX_KEY="plugIndexKey"
    """
       管理插件、信道、和协议。
    """
    def __init__(self):
        super(ESMainWindow, self).__init__()
        self.setupUi(self)
        self.medias = media.get_media_instances()
        self.current_media = self.medias[0]
        self.database = EsDatabase("image.db")
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
        self.tableWidgetFrame.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tableWidgetFrame.customContextMenuRequested.connect(self.log_tablewidgit_menu)
        self.current_index = 0
        self.setting = QSettings("eastsoft","ProtocolMaster")
        self.plug_index_clicked(self.setting.value(self.PLUG_INDEX_KEY, defaultValue=0))
        self.status_bar_timer = QTimer(self)
        self.status_bar_timer.timeout.connect(self.update_status_bar)
        self.status_bar_timer.start(1000)

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

    def update_session(self):
        self.session.media = self.get_current_media()
        self.session.protocol = self.get_current_protocol()

    def install_plugs(self):
        self.plugIndexContainer.setMinimumHeight(475)
        for plug in self.plugs:
            widget = QTreeWidgetItem(self.treeWidget)
            widget.setText(0, plug.name)
            self.plugIndexContainer.addWidget(plug)
            plug.session = self.session
            plug.database = self.database
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
        if self.current_index != idx:
            self.plugIndexContainer.setCurrentIndex(idx)
            self.current_index = idx
            self.setting.setValue(self.PLUG_INDEX_KEY,self.current_index)


    def show_media_config(self):
        if len(self.medias) > 0:
            def ok_func(meida):
                if self.current_media and self.current_media != media:
                    self.current_media = meida
                self.update_session()
            ui.show_user_media_options(self.medias, ok_func)
            self.update_session()
        else:
            QMessageBox.information(None, "错误", u"没有可以用使用的信道")

    def show_protocol_config(self):
        if len(self.protocols) > 0:
            def ok_func(protocol, options):
                pass
            options = list()
            for pros in self.protocols:
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