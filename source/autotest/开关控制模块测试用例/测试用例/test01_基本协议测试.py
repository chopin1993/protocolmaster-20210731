# encoding:utf-8
import engine
from autotest.公共用例.public01基本协议测试 import *

测试组说明 = "基本协议类报文测试"

def test_应用层通讯协议及版本0002():
    """
    02_应用层通讯协议及版本0002
    """
    engine.send_did("READ", "应用层通讯协议及版本0002")
    engine.expect_did("READ", "应用层通讯协议及版本0002", config["应用层通讯协议及版本0002"])

