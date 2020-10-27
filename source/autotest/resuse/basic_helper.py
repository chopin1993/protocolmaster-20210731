# encoding:utf-8
import engine
from register import Register
from protocol.DataMetaType import *


class PublicCase(Register):
    def __init__(self):
        self.units = []

    def __call__(self, monitor):
        raise NotImplemented

    def append_unit(self,unit):
        self.units.append(unit)


class SoftwareCase(PublicCase):
    def __init__(self,software_version):
        "基本报文测试.软件版本"
        super(SoftwareCase, self).__init__()
        self.software_version = software_version
        self.append_unit(DataCString("softwareVersion"))

    def __call__(self, monitor):
        monitor.send_1_did("READ", "DIDSoftversion")
        monitor.expect_1_did("READ", "DIDSoftversion", self.software_version)


def plc_version_helper(monitor, plc_version):
    "_.PLC版本信息"
    monitor.send_1_did("READ", "DIDPlcVersion")
    monitor.expect_1_did("READ", "DIDPlcVersion", plc_version)


def device_type_helper(monitor, device_type):
    "_.设备类型"
    monitor.send_1_did("READ", "DIDDeviceType")
    monitor.expect_1_did("READ", "DIDDeviceType", device_type)