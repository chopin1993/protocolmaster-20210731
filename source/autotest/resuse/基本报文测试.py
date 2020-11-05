# encoding:utf-8
import engine
from public_case import PublicCase
from protocol.DataMetaType import *

def software_version_test(软件版本:DataCString):
    "软件版本测试"
    engine.send_did("READ", "设备描述信息设备制造商")
    engine.expect_did("READ", "设备描述信息设备制造商", 软件版本)


class PlcVersionCase(PublicCase):
    "_.PLC版本信息"
    def __init__(self):
        super(PlcVersionCase, self).__init__()
        self.append_unit(DataCString("应用层通讯协议及版本"))

    def __call__(self, *args, **kwargs):
        engine.send_did("READ", r"应用层通讯协议及版本")
        engine.expect_did("READ", r"应用层通讯协议及版本", self.units[0].value)


class DeviceTypeCase(PublicCase):
    "_.设备类型"
    def __init__(self):
        super(DeviceTypeCase, self).__init__()
        self.append_unit(DataByteArray("设备类型"))

    def __call__(self, *args, **kwargs):
        engine.send_did("READ", "设备类型")
        engine.expect_did("READ", "设备类型", self.units[0].value)




