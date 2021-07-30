# encoding:utf-8
import engine
from .常用测试模块 import *

测试组说明 = "基本协议类报文测试"
"""
1、常用的基本协议类报文测试，已在公共用例中编写，直接导入即可；
2、针对各产品自身的基础协议，根据需要自定义补充；
"""
config = engine.get_config()


def test_设备类型0001():
    """
    01_设备类型0001
    """
    engine.add_doc_info('设备上电')
    ctrl_relay_close(20)
    engine.wait(3)
    ctrl_relay_open(20)

    engine.wait(5)  # 等待设备完全上电
    engine.send_FE02_did("READ", "设备类型0001")
    engine.expect_FE02_did("READ", "设备类型0001", config["设备类型0001"])


def test_设备描述信息设备制造商0003():
    """
    03_设备描述信息设备制造商0003
    """
    engine.send_FE02_did('READ', '设备描述信息设备制造商0003')
    engine.expect_FE02_did('READ', '设备描述信息设备制造商0003', config["设备描述信息设备制造商0003"])


def test_DKEY0005():
    """
    04_DKEY0005
    """
    engine.send_FE02_did("READ", "DKEY0005")
    engine.expect_FE02_did("READ", "DKEY0005", config["DKEY0005"])


def test_SN0007():
    """
    07_SN0007
    """
    engine.send_FE02_did("READ", "SN0007")
    engine.expect_FE02_did("READ", "SN0007", config["SN0007"])


def test_组合报文():  # 本自动测试框架在7e包7e中，目前未对组合报文的发送和接收做处理。20210727-fanxg
    """
    08_多DID组合报文测试
    1、组合报文查询：设备类型0001、设备描述信息设备制造商0003、DKEY0005、SN0007
    2、组合报文查询：适配层物料编码0602、适配层版本号0606、网络层物料编码0609、网络层版本号060A
    """
    engine.add_doc_info('08-组合报文查询：0001+0003+0005+0007')
    engine.send_FE02_multi_dids("READ", "设备类型0001", "",
                                "设备描述信息设备制造商0003", "",
                                "DKEY0005", "",
                                "SN0007", "")
    engine.expect_FE02_multi_dids("READ", "设备类型0001", config["设备类型0001"],
                                  "设备描述信息设备制造商0003", config["设备描述信息设备制造商0003"],
                                  "DKEY0005", config["DKEY0005"],
                                  "SN0007", config["SN0007"])


def test_设备PWD000A():
    """
    09_设备PWD000A
    """
    engine.send_FE02_did("READ", "设备PWD000A")
    engine.expect_FE02_did("READ", "设备PWD000A", config["设备PWD000A"])
