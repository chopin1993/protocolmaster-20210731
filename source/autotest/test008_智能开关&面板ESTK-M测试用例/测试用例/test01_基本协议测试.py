# encoding:utf-8
import engine
from autotest.公共用例.public01基本协议测试 import *

测试组说明 = "基本协议类报文测试"
"""
1、常用的基本协议类报文测试，已在公共用例中编写，直接导入即可；
2、针对各产品自身的基础协议，根据需要自定义补充；
"""


def test_应用层通讯协议及版本0002():
    """
    10_应用层通讯协议及版本0002
    """
    engine.send_did("READ", "应用层通讯协议及版本0002")
    engine.expect_did("READ", "应用层通讯协议及版本0002", config["应用层通讯协议及版本0002"])