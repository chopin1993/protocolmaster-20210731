# encoding:utf-8
import engine
from protocol.DataMetaType import *

测试组说明="本测试组内测试所有的设备均需支持。"

def test_software_version(软件版本:DataCString):
    "软件版本测试"
    engine.send_did("READ", "设备描述信息设备制造商")
    engine.expect_did("READ", "设备描述信息设备制造商", 软件版本)

def test_plc_version(应用层通讯协议及版本:DataCString):
    "PLC版本信息"
    engine.send_did("READ", r"应用层通讯协议及版本")
    engine.expect_did("READ", r"应用层通讯协议及版本", 应用层通讯协议及版本)

def test_device_type(设备类型:DataByteArray):
    "设备类型测试"
    engine.send_did("READ", "设备类型")
    engine.expect_did("READ", "设备类型", 设备类型)

def test_sn_info(sn通配符:DataCString):
    """
    SN查询
    SN中变化的部分可以使用*作为通配符
    """
    engine.send_did("READ", "SN")
    engine.expect_did("READ", "SN", sn通配符)


def test_dkey(dkey通配符:DataCString):
    """
    Dkey查询
    Dkey中变化的部分可以使用*作为通配符
    """
    engine.send_did("READ", "DKEY")
    engine.expect_did("READ", "DKEY", dkey通配符)


def test_multi_dids():
    "多DID测试"
    engine.send_multi_dids("READ", "DKEY", "", "SN", "", "设备类型", "")
    engine.expect_multi_dids("READ",
                             "DKEY", "** ** ** ** ** ** ** **",
                             "SN", "** ** ** ** ** ** ** ** ** ** ** **",
                             "设备类型","** ** ** ** ** ** ** **",
                             timeout=3)



