# encoding:utf-8

from .application_plug import plug_register,ApplicationPlug
from .oip_ui import Ui_Form
from PyQt5.QtGui import QImage,QPixmap
from PyQt5 import QtCore
from protocol.smart7e_protocol import *


@plug_register
class OIPPlug(ApplicationPlug, Ui_Form):

    def __init__(self):
        super(OIPPlug, self).__init__("智能视觉传感器")
        self.setupUi(self)
        self.setMyAddress.clicked.connect(self.set_my_address)

    def set_my_address(self):
        fbd = LocalFBD(LocalCmd.SET_APPLICATION_ADDR, int(self.myAddrLineEdit.text()))
        self.send_local_data(fbd)

    def handle_receive_data(self, msg):
        if msg.is_local():
            self.handle_local_msg(msg)
        else:
            self.handl_remote_msg(msg)

    def handle_local_msg(self, msg):
        pass

    def handle_remote_msg(self, msg):
        try:
            src, dst = int(self.myAddrLineEdit.text()), int(self.devieAddrLineEdit.text())
            data = Smart7EData(src, dst, msg)
            self.send_data(data)
        except ValueError:
            self.show_error_msg("","地址格式不对")

    def send_local_data(self, fbd):
        data = Smart7EData(0, 0, fbd)
        self.send_data(data)

    def send_remote_data(self, data):
        pass

    def get_protocols(self):
        return ["Smart7eProtocol",]