# encoding:utf-8
from PyQt5.QtWidgets import QHBoxLayout

from .application_plug import plug_register,ApplicationPlug
from .oip_ui import Ui_Form
from PyQt5.QtGui import QImage,QPixmap
from PyQt5 import QtCore
from protocol.codec import BinaryDecoder,BinaryEncoder
from protocol.smart7e_protocol import *
from ESSetting import ESSetting
from tools.converter import hexstr2bytes
from protocol.smart7e_DID import DIDRemote
import sip
from protocol.smart7e_DID import sync_json_dids

@plug_register
class OIPPlug(ApplicationPlug, Ui_Form):
    TAID_KEY= "TAID_KEY"
    def __init__(self):
        super(OIPPlug, self).__init__("智能视觉传感器")
        self.current_did_tmp = None
        self.current_cmd_tmp = None
        self.setupUi(self)
        self.setMyAddress.clicked.connect(self.set_my_address)
        self.setting = ESSetting.instance()
        self.devieAddrLineEdit.setText(self.setting.get_plug_data(self, self.TAID_KEY, default_value="2"))
        self.devieAddrLineEdit.textChanged.connect(self.save_plug_config)
        self.sendPushButton.clicked.connect(self.send_message)
        self.syncDIDPushButton.clicked.connect(self.sync_json_dids)
        self.sync_did_2_comboBox()
        self.didcomboBox.currentTextChanged.connect(self.did_changed)
        self.operation_widgets = []
        self.reply_widgets = []
        self.reply_layout = QHBoxLayout()
        self.dataGroup.setLayout(self.reply_layout)
        for cmd in CMD:
            self.cmdComboBox.addItem(cmd.name)
        self.cmdComboBox.currentTextChanged.connect(self.cmd_changed)
        self.cmd_changed(self.cmdComboBox.currentText())

    def send_message(self):
        cls = DIDRemote.find_class_by_name(self.didcomboBox.currentText())
        if cls is None:
            self.show_error_msg("", "不能正确的识别did")
            return
        try:
            data = cls.encode_widgets(self.operation_widgets, CMD[self.cmdComboBox.currentText()])
            fbd = RemoteFBD.create(CMD[self.cmdComboBox.currentText()], self.didcomboBox.currentText(), data)
        except Exception as e :
            self.show_error_msg("数据格式不合法", str(e), e)
            return
        if fbd is None:
            self.show_error_msg("", "did is not valid")
        else:
            self.send_remote_data(fbd)

    def sync_widget(self):
        did, cmd = self.didcomboBox.currentText(), self.cmdComboBox.currentText()
        if self.current_did_tmp == did and self.current_cmd_tmp==cmd:
            return
        else:
            self.current_did_tmp = did
            self.current_cmd_tmp = cmd
        for widget in self.operation_widgets:
            self.operationGroup.layout().removeWidget(widget)
            sip.delete(widget)
        for widget in self.reply_widgets:
            self.reply_layout.removeWidget(widget)
            sip.delete(widget)
        self.operation_widgets = []
        self.reply_widgets = []
        cls = DIDRemote.find_class_by_name(did)
        if cls is None:
            return
        self.operation_widgets, self.reply_widgets = cls.create_widgets(cmd)
        for i,widget in enumerate(self.operation_widgets):
            self.operationGroup.layout().insertWidget(3+i, widget)
        for widget in self.reply_widgets:
            self.reply_layout.addWidget(widget)

    def cmd_changed(self, txt):
        self.sync_widget()
        print("cmd change ",txt)

    def did_changed(self, txt):
        self.sync_widget()

    def sync_reply_widgets_value(self, data):
        cls = self.get_selected_did()
        if cls is not None:
            decoder = BinaryDecoder(data)
            cls.sync_reply_value(self.reply_widgets, decoder)

    def sync_did_2_comboBox(self):
        self.didcomboBox.clear()
        dids = DIDRemote.get_did_dict()
        for key,_ in dids.items():
            self.didcomboBox.addItem(key)

    def sync_json_dids(self):
        ret, msg = sync_json_dids()
        if ret < 0:
            self.show_error_msg("Smart7E文件格式有误", msg)
        else:
            self.sync_did_2_comboBox()

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
                        self.sync_reply_widgets_value(didunit.data)
        except Exception as e:
            self.show_error_msg("解析错误",str(e),e)

    def get_selected_did(self):
        cls = DIDRemote.find_class_by_name(self.didcomboBox.currentText())
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