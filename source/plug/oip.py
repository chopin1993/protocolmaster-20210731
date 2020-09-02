# encoding:utf-8

from .application_plug import plug_register,ApplicationPlug
from .oip_ui import Ui_Form
from PyQt5.QtGui import QImage,QPixmap
from PyQt5 import QtCore
from protocol.smart7e_protocol import *
from ESSetting import ESSetting
from tools.converter import hexstr2bytes

@plug_register
class OIPPlug(ApplicationPlug, Ui_Form):
    TAID_KEY= "TAID_KEY"
    def __init__(self):
        super(OIPPlug, self).__init__("智能视觉传感器")
        self.setupUi(self)
        self.setMyAddress.clicked.connect(self.set_my_address)
        self.setting = ESSetting.instance()
        self.devieAddrLineEdit.setText(self.setting.get_plug_data(self, self.TAID_KEY, default_value="2"))
        self.devieAddrLineEdit.textChanged.connect(self.save_plug_config)
        self.readPushButton.clicked.connect(self.readDID)
        self.setPushButton.clicked.connect(self.setDID)
        self.syncDIDPushButton.clicked.connect(self.sync_json_dids)
        self.refresh_didcomboBox()

    def refresh_didcomboBox(self):
        self.didcomboBox.clear()
        dids = get_all_DID()
        for key in dids:
            self.didcomboBox.addItem(key)

    def sync_json_dids(self):
        ret, msg = sync_json_dids()
        if ret < 0:
            self.show_error_msg("Smart7E文件格式有误", msg)
        else:
            self.refresh_didcomboBox()

    def readDID(self):
        data = hexstr2bytes(self.didLineEdit.text())
        fbd = RemoteFBD.create(CMD.READ, self.didcomboBox.currentText(), data)
        self.send_remote_data(fbd)

    def setDID(self):
        data = hexstr2bytes(self.didLineEdit.text())
        fbd = RemoteFBD.create(CMD.WRTIE, self.didcomboBox.currentText(), data)
        self.send_remote_data(fbd)

    def save_plug_config(self):
        self.setting.save_plug_data(self, self.TAID_KEY, self.devieAddrLineEdit.text())

    def set_my_address(self):
        fbd = LocalFBD(DIDLocal.SET_APPLICATION_ADDR, int(self.myAddrLineEdit.text()))
        self.send_local_data(fbd)

    def handle_receive_data(self, msg):
        if msg.is_local():
            self.handle_local_msg(msg)
        else:
            self.handle_remote_msg(msg)

    def handle_local_msg(self, msg):
        pass

    def handle_remote_msg(self, msg):
        pass

    def send_local_data(self, fbd):
        data = Smart7EData(0, 0, fbd)
        self.send_data(data)

    def send_remote_data(self, fbd):
        try:
            src, dst = int(self.myAddrLineEdit.text()), int(self.devieAddrLineEdit.text())
            data = Smart7EData(src, dst, fbd)
            self.send_data(data)
        except ValueError:
            self.show_error_msg("","地址格式不对")

    def get_protocols(self):
        return ["Smart7eProtocol",]