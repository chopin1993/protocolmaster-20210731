# encoding:utf-8
# 导入测试引擎
import engine
# from autotest.公共用例.public05远程升级测试 import *
from .常用测试模块 import *

测试组说明 = "通讯测试"



def test_错误类报文测试():
    """
    09_错误类报文测试
    1、数据格式错误，返回错误字00 03（C0 12的数据长度为2，而发送命令中的长度为3）
    2、数据域少一个字节，返回错误字00 01数据域长度错误
    3、发送不存在的数据项FB20，返回错误字00 04数据项不存在
    """

    engine.add_doc_info("1、数据格式错误，返回错误字00 03（C0 12的数据长度为1，而发送命令中的长度为3）")
    engine.send_did("WRITE", "设置密码C030", "01 02 03")
    engine.expect_did("WRITE", "设置密码C030", "03 00")

    engine.add_doc_info("2、数据域少一个字节，返回错误字00 01数据域长度错误")
    engine.add_doc_info('本种错误由载波适配层判断并直接回复，所以SWB总线是监控不到的')
    engine.send_raw("30 C0 02 49")
    engine.expect_did("WRITE", "设置密码C030", "01 00")

    engine.add_doc_info("3、发送不存在的数据项，返回错误字00 04数据项不存在")
    engine.send_did("READ", "适配层版本号0606", "")
    engine.expect_did("READ", "适配层版本号0606", "04 00")

    engine.add_doc_info("3、读取时0003后面多加12 34，还是能正常读取，读取无需含信息时无论是否携带内容均可正常读取")
    engine.send_did("READ", "设备描述信息设备制造商0003", "12 34")
    engine.expect_did("READ", "设备描述信息设备制造商0003", "")