# encoding:utf-8
import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from config import ESConfig
from session import SessionSuit
from tools.converter import str2hexstr, hexstr2str
from ui.media_option_ui import get_user_options
from plug import plugs_get_all
from protocol_master_ui import Ui_MainWindow

reload(sys)
sys.setdefaultencoding('utf8')


class EarthMother(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(EarthMother, self).__init__()
        self.setupUi(self)
        self.stackedWidget = QStackedWidget(self.appGroupBox)
        self.widgets = list()
        self.plugs = plugs_get_all()

        for plug in self.plugs:
            self.install_plugs(plug)

    def install_plugs(self, a_plug):
        widget = QTreeWidgetItem(self.treeWidget)
        widget.setText(0,a_plug.name)
        self.stackedWidget.addWidget(a_plug)


    def item_changed(item , index):
        print index,"clicked"

    def clicked(self, index):
        self.stackedWidget.setCurrentIndex(index.row())

        # self.session.data_ready.connect(self.protocol_handle)
        # self.session.media.error.connect(self.show_media_error)
        # self.show_media_config()
        #
        # action = QAction(u"通信参数", self)
        # action.setShortcut("Ctrl+R")
        # action.triggered.connect(self.show_media_config)
        # self.menuSet.addAction(action)
        # self.toolbar.addAction(action)
        #
        # action = QAction(u"导入设备", self)
        # action.triggered.connect(self.import_device_list)
        # self.menuDevice.addAction(action)
        # self.toolbar.addAction(action)

    # def get_select_media(self):
    #     reply = QMessageBox.information(self, u"通信方式", u"请选择通信方式", "TCP","UART")
    #     return reply
    #
    # def show_media_error(self, msg):
    #     QMessageBox.information(self, u"串口错误", msg)
    #
    # def show_media_config(self):
    #     get_user_options(self.session.media)
    #
    # def import_device_list(self):
    #     file_name = QFileDialog.getOpenFileName(directory=ESConfig.get_instance().get_device_file())
    #     file_name = unicode(file_name.toUtf8(), 'utf-8', 'ignore')
    #     ESConfig.get_instance().set_device_file(file_name)
    #     self.devices = get_all_device(file_name)
    #     self.sync_device_to_ui()
    #
    # def sync_device_to_ui(self):
    #     devices = self.devices
    #     self.tableWidget.setRowCount(len(devices))
    #     for i, device in enumerate(devices):
    #         widget = QTableWidgetItem(device.get_hex_string_address())
    #         self.tableWidget.setItem(i, 0, widget)
    #         device.device_update.connect(self.sync_status_to_ui)
    #     self.send_idx = 0
    #
    # def sync_status_to_ui(self):
    #     for i, device in enumerate(self.devices):
    #         widget = QTableWidgetItem(device.get_summary())
    #         self.tableWidget.setItem(i, 1, widget)
    #
    # def read_next_device(self):
    #     device = self.devices[self.send_idx]
    #     device.add_send_count()
    #     self.send_idx += 1
    #     self.send_idx %= len(self.devices)
    #     self.sync_status_to_ui()
    #     if self.protocol_idx == PROTOL_645_07:
    #         self.session.send_data(hexstr2str(str(self.convertAddressLineEdit.text())), DIDRealTimeMeterData(device.address))
    #     elif self.protocol_idx == PROTOL_188:
    #         self.session.send_data(device.address, DIDReadMeter())
    #     elif self.protocol_idx == PROTOL_645_97:
    #         protocol = CJT188Protocol.create_frame(device.address,DIDReadMeter())
    #         data = BinaryEncoder.object2data(protocol)
    #         self.session.send_data(hexstr2str(str(self.convertAddressLineEdit.text())), DIDESTunnelData(data))
    #
    # def eventFilter(self, source, event):
    #     if source == self.video_label and event.type() == QEvent.MouseButtonPress:
    #         return True
    #     else:
    #         return QMainWindow.eventFilter(self, source, event)
    #
    # def start(self):
    #     if len(self.devices) == 0:
    #         QMessageBox.information(self, u"导入设备", u"轮抄需要首先导入设备列表")
    #         return
    #     self.read_next_device()
    #     self.timer.start(int(str(self.readMeterSpanLineEdit.text()))*1000)
    #
    # def stop(self):
    #     self.timer.stop()
    #
    # def read_convert_address(self):
    #     if self.protocol_idx != PROTOL_188:
    #         self.session.send_data(chr(0xaa)*6, None, cmd=0x13)
    #
    # def protocol_change(self, idx):
    #     self.protocol_idx = idx
    #     if idx == PROTOL_188:
    #         self.session.protocol_cls = CJT188Protocol
    #     elif idx == PROTOL_645_07:
    #         self.protocol_idx = True
    #         self.session.protocol_cls = DL645_07_Protocol
    #     elif  idx == PROTOL_645_97:
    #         self.session.protocol_cls =  DL645_97_Protocol


def protocol_master_run():
    app = QApplication(sys.argv)
    ex = EarthMother()
    ex.move((QApplication.desktop().width() - ex.width()) / 2, (QApplication.desktop().height() - ex.height()) / 2);
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    protocol_master_run()
