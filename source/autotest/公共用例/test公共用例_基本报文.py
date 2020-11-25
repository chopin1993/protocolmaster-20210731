# encoding:utf-8
import engine
from protocol.DataMetaType import *

测试组说明="本测试组内测试所有的设备均需支持。"

def test_software_version(软件版本:DataCString):
    "软件版本测试"
    engine.send_did("READ", "设备描述信息设备制造商0003")
    engine.expect_did("READ", "设备描述信息设备制造商0003", 软件版本)

def test_plc_version(应用层通讯协议及版本:DataCString):
    "PLC版本信息"
    engine.send_did("READ", r"应用层通讯协议及版本0002")
    engine.expect_did("READ", r"应用层通讯协议及版本0002", 应用层通讯协议及版本)

def test_device_type(设备类型:DataByteArray):
    "设备类型测试"
    engine.send_did("READ", "设备类型0001")
    engine.expect_did("READ", "设备类型0001", 设备类型)

def test_sn_info(sn通配符:DataCString):
    """
    SN查询
    SN中变化的部分可以使用*作为通配符
    """
    engine.send_did("READ", "SN0007")
    engine.expect_did("READ", "SN0007", sn通配符)

def test_dkey(dkey通配符:DataCString):
    """
    Dkey查询
    Dkey中变化的部分可以使用*作为通配符
    """
    engine.send_did("READ", "DKEY0005")
    engine.expect_did("READ", "DKEY0005", dkey通配符)


def test_multi_dids():
    "多DID测试"
    engine.send_multi_dids("READ", "DKEY", "", "SN", "", "设备类型", "")
    engine.expect_multi_dids("READ",
                             "DKEY", "** ** ** ** ** ** ** **",
                             "SN", "** ** ** ** ** ** ** ** ** ** ** **",
                             "设备类型","** ** ** ** ** ** ** **",
                             timeout=3)



