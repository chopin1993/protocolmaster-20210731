# encoding:utf-8
import engine
from public_case import PublicCase
from protocol.DataMetaType import *

测试组说明="本测试组内测试所有的设备均需支持"

def software_version_test(软件版本:DataCString):
    "软件版本测试"
    engine.send_did("READ", "设备描述信息设备制造商")
    engine.expect_did("READ", "设备描述信息设备制造商", 软件版本)

def  plc_version_test(应用层通讯协议及版本:DataCString):
    "PLC版本信息"
    engine.send_did("READ", r"应用层通讯协议及版本")
    engine.expect_did("READ", r"应用层通讯协议及版本", 应用层通讯协议及版本)

def device_type_test(设备类型:DataByteArray):
    "设备类型测试"
    engine.send_did("READ", "设备类型")
    engine.expect_did("READ", "设备类型", 设备类型)

def sn_info_test(sn通配符:DataCString):
    """
    SN查询
    SN中变化的部分可以使用*作为通配符
    """
    engine.send_did("READ", "SN")
    engine.expect_did("READ", "SN", sn通配符)


def dkey_test(dkey通配符:DataCString):
    """
    Dkey查询
    Dkey中变化的部分可以使用*作为通配符
    """
    engine.send_did("READ", "DKEY")
    engine.expect_did("READ", "DKEY", dkey通配符)
