# encoding:utf-8
# 导入测试引擎
from autotest.公共用例.public03设备搜索测试 import *
from .常用测试模块 import *

测试组说明 = "设备搜索测试"

config = engine.get_config()

# 设备搜索类型即被测设备自身的设备类型
config["设备搜索类型"] = config["SN0007"][0:11]
# 设备不支持的搜索类型，可以自定义多个类型进行验证
config["设备不支持的搜索类型"] = ["31 71 10 10", "31 71 20 01"]


def test_静默时间000B断电测试():
    """
    09_静默时间000B断电测试
    验证在静默时间内，是否可以不响应搜索报文
    1、首先验证设备搜索功能正常
    2、设置静默时间300s,测试静默时间内抄读版本及控制通断均正常
    3、静默时间内多次进行设备搜索，均不回复
    4、控制前置工装断电重启，再次测试设备搜索正常，说明断电后设备静默时间失效
    """
    engine.add_doc_info("1、首先验证设备搜索功能正常")
    device_search0008(search_time=10, search_type=config["设备搜索类型"])

    engine.add_doc_info("2、设置静默时间300s,测试静默时间内抄读版本及控制通断均正常")
    engine.send_did("WRITE", "静默时间000B", 静默时间=300)
    engine.expect_did("WRITE", "静默时间000B", 静默时间=300)
    read_write_test()

    engine.add_doc_info("3、静默时间内多次进行设备搜索，均不回复")
    device_search0008(search_time=10, search_type=config["设备搜索类型"], search_reply=False)
    device_search0008(search_time=30, search_type=config["设备搜索类型"], search_reply=False)
    device_search0008(search_time=60, search_type=config["设备搜索类型"], search_reply=False)
    # 静默时间内的断电重启测试
    engine.add_doc_info("4、静默时间内进行断电重启测试")
    power_control()  # 工装断电重启用时约30s，仍在300s范围内
    device_search0008(search_time=10, search_type="FF FF FF FF")
    device_search0008(search_time=10, search_type=config["设备搜索类型"])


def test_APP设备指示0009():
    """
    10_APP设备指示0009
    1、发送指示命令，验证设备的响应动作与要求一致；
    设备指示具体指示动作为红外指示灯闪烁，持续6s，设备指示过程中不允许载波通信；
    2、发送指示命令，验证设备指示过程中不允许载波通信；
    """
    engine.add_doc_info("1、发送指示命令，验证设备的响应动作与要求一致；")
    engine.send_did("WRITE", "APP设备指示0009", "")
    engine.expect_did("WRITE", "APP设备指示0009", "")
    engine.wait((6 + 1), allowed_message=False)

    #  设备指示过程中进行抄读测试,设备指示过程中不允许载波通信验证
    engine.add_doc_info("2、设备指示过程中进行抄读测试,设备指示过程中不允许载波通信验证")
    engine.send_did("WRITE", "APP设备指示0009", "")
    engine.expect_did("WRITE", "APP设备指示0009", "")
    engine.send_did("READ", "设备描述信息设备制造商0003")
    engine.wait(2, allowed_message=False)
    engine.send_did('WRITE', '心跳时间D101', 心跳时间=30)
    engine.wait(2, allowed_message=False)
    engine.send_did("READ", "主动上报使能标志D005", "")
    engine.wait(2, allowed_message=False)
    engine.add_doc_info("设备指示结束后，可以正常进行载波通信验证")
    read_write_test()


def test_APP设备指示中断电测试():
    """
    11_APP设备指示中断电测试
    1、设备指示验证正常
    2、设备指示过程中被断电重启，被测设备退出设备指示，设备载波通信恢复正常
    """
    engine.add_doc_info("1、设备指示验证正常")
    engine.send_did("WRITE", "APP设备指示0009", "")
    engine.expect_did("WRITE", "APP设备指示0009", "")
    engine.add_doc_info("设备指示过程中进行抄读测试,设备指示过程中不允许载波通信验证")
    engine.send_did("READ", "设备描述信息设备制造商0003")
    engine.wait(3, allowed_message=False)
    engine.send_did("READ", "设备描述信息设备制造商0003")
    engine.wait(4, allowed_message=False)

    engine.add_doc_info("2、设备指示过程中被断电重启，被测设备退出设备指示，设备载波通信恢复正常")
    engine.send_did("WRITE", "APP设备指示0009", "")
    engine.expect_did("WRITE", "APP设备指示0009", "")
    engine.wait(2, allowed_message=False)
    power_control()
    engine.add_doc_info("抄读版本及控制测试，均正常")
    read_write_test()
