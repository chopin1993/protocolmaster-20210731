# encoding:utf-8
import engine
from .public_case import PublicCase
from protocol.DataMetaType import *

class SoftwareCase(PublicCase):
    "基本报文测试.软件版本"
    def __init__(self):
        super(SoftwareCase, self).__init__()
        self.append_unit(DataCString("软件版本"))

    def __call__(self):
        engine.send_1_did("READ", "设备描述信息、设备制造商")
        engine.expect_1_did("READ", "设备描述信息、设备制造商", self.units[0].value)


class PlcVersionCase(PublicCase):
    "_.PLC版本信息"
    def __init__(self):
        super(PlcVersionCase, self).__init__()
        self.append_unit(DataCString("plcVersion"))

    def __call__(self, *args, **kwargs):
        engine.send_1_did("READ", r"应用层通讯协议及版本")
        engine.expect_1_did("READ", r"应用层通讯协议及版本", self.units[0].value)


class DeviceTypeCase(PublicCase):
    "_.设备类型"
    def __init__(self):
        super(DeviceTypeCase, self).__init__()
        self.append_unit(DataByteArray("deviceType"))

    def __call__(self, *args, **kwargs):
        engine.send_1_did("READ", "设备类型")
        engine.expect_1_did("READ", "设备类型", self.units[0].value)

