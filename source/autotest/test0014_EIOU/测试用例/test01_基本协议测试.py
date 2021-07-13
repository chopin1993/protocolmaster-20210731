# encoding:utf-8
import engine
from autotest.公共用例.public01基本协议测试 import *

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
    engine.send_did("READ", "设备类型0001")
    engine.expect_did("READ", "设备类型0001", config["设备类型0001"])


def test_设备描述信息设备制造商0003():
    """
    02_设备描述信息设备制造商0003
    """
    engine.send_did("READ", "设备描述信息设备制造商0003", "")
    engine.expect_did("READ", "设备描述信息设备制造商0003", config["设备描述信息设备制造商0003"])





def test_DKEY0005():
    """
    06_DKEY0005
    """
    engine.send_did("READ", "DKEY0005")
    engine.expect_did("READ", "DKEY0005", config["DKEY0005"])


def test_SN0007():
    """
    07_SN0007
    """
    engine.send_did("READ", "SN0007")
    engine.expect_did("READ", "SN0007", config["SN0007"])


def test_组合报文():
    """
    08_多DID组合报文测试
    1、组合报文查询：设备类型0001、设备描述信息设备制造商0003、DKEY0005、SN0007
    2、组合报文查询：适配层物料编码0602、适配层版本号0606、网络层物料编码0609、网络层版本号060A
    """
    engine.add_doc_info("1、组合报文查询：0001+0003+0005+0007")
    engine.send_multi_dids("READ", "设备类型0001", "",
                           "设备描述信息设备制造商0003", "",
                           "DKEY0005", "",
                           "SN0007", "")
    engine.expect_multi_dids("READ", "设备类型0001", config["设备类型0001"],
                             "设备描述信息设备制造商0003", config["设备描述信息设备制造商0003"],
                             "DKEY0005", config["DKEY0005"],
                             "SN0007", config["SN0007"])




def test_设备PWD000A():
    """
    09_设备PWD000A
    """
    engine.send_did("READ", "设备PWD000A")
    engine.expect_did("READ", "设备PWD000A", config["设备PWD000A"])

def test_应用层通讯协议及版本0002():
    """
    10_应用层通讯协议及版本0002
    """
    engine.send_did("READ", "应用层通讯协议及版本0002")
    engine.expect_did("READ", "应用层通讯协议及版本0002", config["应用层通讯协议及版本0002"])