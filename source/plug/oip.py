# encoding:utf-8

from .application_plug import plug_register,ApplicationPlug
from .oip_ui import Ui_Form
from PyQt5.QtGui import QImage,QPixmap
from PyQt5 import QtCore
from protocol.smart7e_protocol import *
from ESSetting import ESSetting
from tools.converter import hexstr2bytes
from protocol.smart7e_DID import find_class_by_name
import sip

@plug_register
class OIPPlug(ApplicationPlug, Ui_Form):
    TAID_KEY= "TAID_KEY"
    def __init__(self):
        super(OIPPlug, self).__init__("智能视觉传感器")
        self.current_txt = None
        self.setupUi(self)
        self.setMyAddress.clicked.connect(self.set_my_address)
        self.setting = ESSetting.instance()
        self.devieAddrLineEdit.setText(self.setting.get_plug_data(self, self.TAID_KEY, default_value="2"))
        self.devieAddrLineEdit.textChanged.connect(self.save_plug_config)
        self.readPushButton.clicked.connect(self.readDID)
        self.setPushButton.clicked.connect(self.setDID)
        self.syncDIDPushButton.clicked.connect(self.sync_json_dids)
        self.refresh_didcomboBox()
        self.didcomboBox.currentTextChanged.connect(self.sync_did_widgets)
        self.did_widgets = []
        self.groupdata_layout = QHBoxLayout()
        self.sync_did_widgets(self.didcomboBox.currentText())
        self.dataGroup.setLayout(self.groupdata_layout)

    def widgets_value_change(self):
        selecteddid = self.get_selected_did()
        if selecteddid is not None:
            encoder = BinaryEncoder()
            for widget, meta in zip(self.did_widgets, selecteddid.MEMBERS):
                meta.encode_widget_value(widget, encoder)

    def sync_did_widgets(self, txt):
        if self.current_txt == txt:
            return
        else:
            self.current_txt = txt
        for widget in self.did_widgets:
            self.groupdata_layout.removeWidget(widget)
            sip.delete(widget)
        self.did_widgets = []
        cls = find_class_by_name(txt)
        if cls is None:
            return
        self.did_widgets = [meta.create_widgets(self.widgets_value_change) for meta in cls.MEMBERS]
        for widget in self.did_widgets:
            self.groupdata_layout.addWidget(widget)

    def sync_widgets_value(self, data):
        selecteddid = self.get_selected_did()
        if selecteddid is not None:
            decoder = BinaryDecoder(data)
            for widget,meta in zip(self.did_widgets, selecteddid.MEMBERS):
                meta.set_widget_value(widget, decoder)

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
        data = hexstr2bytes(self.rawLineEdit.text())
        fbd = RemoteFBD.create(CMD.READ, self.didcomboBox.currentText(), data)
        if fbd is None:
            self.show_error_msg("", "did is not valid")
        else:
            self.send_remote_data(fbd)

    def setDID(self):
        data = hexstr2bytes(self.rawLineEdit.text())
        fbd = RemoteFBD.create(CMD.WRTIE, self.didcomboBox.currentText(), data)
        if fbd is None:
            self.show_error_msg("", "did is not valid")
        else:
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
        try:
            selecteddid = self.get_selected_did()
            if selecteddid is not None:
                for didunit in msg.fbd.didunits:
                    if didunit.is_error:
                        self.show_error_msg("错误",str(didunit))
                        continue
                    if didunit.DID == self.get_selected_did().DID:
                        self.sync_widgets_value(didunit.data)
                        self.rawLineEdit.setText(str2hexstr(didunit.data))
        except Exception as e:
            self.show_error_msg("解析错误",str(e))

    def get_selected_did(self):
        cls = find_class_by_name(self.didcomboBox.currentText())
        return cls

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