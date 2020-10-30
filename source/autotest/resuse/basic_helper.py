# encoding:utf-8
import engine
from register import Register
from protocol.DataMetaType import *

class PublicCase(Register):
    def __init__(self, default_enable=True):
        self.units = []
        self.default_enable = default_enable

    def __call__(self, monitor):
        raise NotImplemented

    def append_unit(self,unit):
        self.units.append(unit)

    def get_para_widgets(self):
        ask_widgets = [meta.get_widgets() for meta in self.units]
        return ask_widgets

    def get_config_value(self):
        config = {}
        for unit in self.units:
            config[unit.name] = unit.value_str()
        return config

    def load_config_value(self, config):
        for unit in self.units:
            if unit.name in config:
                unit.value = config[unit.name]


class SoftwareCase(PublicCase):
    "基本报文测试.软件版本"
    def __init__(self):
        super(SoftwareCase, self).__init__()
        self.append_unit(DataCString("软件版本"))

    def __call__(self):
        engine.send_1_did("READ", "DIDSoftversion")
        engine.expect_1_did("READ", "DIDSoftversion", self.units[0].value)


class PlcVersionCase(PublicCase):
    "_.PLC版本信息"
    def __init__(self):
        super(PlcVersionCase, self).__init__()
        self.append_unit(DataCString("plcVersion"))

    def __call__(self, *args, **kwargs):
        engine.send_1_did("READ", "DIDPlcVersion")
        engine.expect_1_did("READ", "DIDPlcVersion", self.units[0].value)


class DeviceTypeCase(PublicCase):
    "_.设备类型"
    def __init__(self):
        super(DeviceTypeCase, self).__init__()
        self.append_unit(DataByteArray("deviceType"))

    def __call__(self, *args, **kwargs):
        engine.send_1_did("READ", "DIDDeviceType")
        engine.expect_1_did("READ", "DIDDeviceType", self.units[0].value)


class PrintTypeCase(PublicCase):
    "_.设备远程打印开关"
    def __init__(self):
        super(PrintTypeCase, self).__init__(False)
        self.append_unit(DataByteArray("value"))

    def __call__(self, *args, **kwargs):
        engine.send_1_did("READ", "DIDDeviceType")
        engine.expect_1_did("READ", "DIDDeviceType", self.units[0].value)