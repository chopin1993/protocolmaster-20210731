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
    2、设置静默时间300s,测试静默时间内抄读版本及设置参数、查询参数均正常
    3、静默时间内多次进行设备搜索，均不回复
    4、控制前置工装断电重启，再次测试设备搜索正常，说明断电后设备静默时间失效
    """
    engine.add_doc_info("1、首先验证设备搜索功能正常")
    device_search0008(search_time=10, search_type=config["设备搜索类型"])

    engine.add_doc_info("2、设置静默时间300s,测试静默时间内抄读版本及设置参数、查询参数均正常")
    engine.send_did("WRITE", "静默时间000B", 静默时间=300)
    engine.expect_did("WRITE", "静默时间000B", 静默时间=300)
    read_write_test()

    engine.add_doc_info("3、静默时间内多次进行设备搜索，均不回复")
    for search_time in [10, 30, 60]:
        device_search0008(search_time=search_time, search_type=config["设备搜索类型"], search_reply=False)
    # 静默时间内的断电重启测试
    engine.add_doc_info("4、静默时间内进行断电重启测试")
    power_control()  # 工装断电重启用时约30s，仍在300s范围内
    device_search0008(search_time=10, search_type="FF FF FF FF")
    device_search0008(search_time=10, search_type=config["设备搜索类型"])


def test_APP设备指示0009():
    """
    10_APP设备指示0009
    1、发送指示命令，验证设备的响应动作是否与要求一致。
    设备指示具体指示动作为: 窗帘先下拉2s，停顿2s，然后上拉5s。
    """
    engine.add_doc_info('设备指示具体指示动作为: 窗帘先下拉2s，停顿2s，然后上拉5s。通过窗帘输出检测正常')
    engine.send_did("WRITE", "APP设备指示0009", "")
    engine.expect_did("WRITE", "APP设备指示0009", "")
    engine.wait(1, tips='当前处于下拉2s状态，进行输出验证')
    engine.expect_cross_zero_status(0, 0)
    engine.expect_cross_zero_status(1, 1)
    engine.wait(2, tips='当前处于暂停2s状态，进行输出验证')
    engine.expect_cross_zero_status(0, 0)
    engine.expect_cross_zero_status(1, 0)
    engine.wait(5, tips='当前处于上拉5s状态，进行输出验证')
    engine.expect_cross_zero_status(0, 1)
    engine.expect_cross_zero_status(1, 0)
    engine.wait(2, tips='设备指示结束，进行输出验证')
    engine.expect_cross_zero_status(0, 0)
    engine.expect_cross_zero_status(1, 0)

    engine.wait(10, allowed_message=False)
    #  设备指示过程中进行抄读测试,设备指示过程中不允许载波通信验证
    engine.add_doc_info("设备指示过程中进行抄读测试,窗帘控制模块与其他载波设备现象不一致")
    engine.send_did("WRITE", "APP设备指示0009", "")
    engine.expect_did("WRITE", "APP设备指示0009", "")
    engine.wait(1, tips='设备在进行指示时，当前动作正处于下拉状态，发送控制正转、反转的控制命令时，设备回复“设备忙”错误0005。')
    for value in ['正转', '反转']:
        engine.send_did("WRITE", "电机转动0A04", 电机状态=value)
        engine.expect_did("WRITE", "电机转动0A04", '05 00')
    engine.wait(2, tips='设备在进行指示时，此时处于暂停2s阶段')
    engine.wait(1, tips='设备在进行指示时，当前动作正处于上拉状态，发送控制正转、反转的控制命令时，设备回复“设备忙”错误0005。查询版本正常')
    for value in ['正转', '反转']:
        engine.send_did("WRITE", "电机转动0A04", 电机状态=value)
        engine.expect_did("WRITE", "电机转动0A04", '05 00')
    engine.send_did("READ", "设备描述信息设备制造商0003")
    engine.expect_did("READ", "设备描述信息设备制造商0003", config["设备描述信息设备制造商0003"])

    engine.add_doc_info("设备指示结束后，可以正常进行载波通信验证")
    read_write_test()


def test_APP设备指示中断电测试():
    """
    11_APP设备指示中断电测试
    1、设备指示验证正常
    2、设备指示过程中被断电重启，被测设备退出设备指示，设备载波通信恢复正常
    """
    engine.add_doc_info("设备指示过程中断电重启，退出设备指示，设备载波通信恢复正常")
    engine.send_did("WRITE", "APP设备指示0009", "")
    engine.expect_did("WRITE", "APP设备指示0009", "")
    engine.wait(1, tips='设备在进行指示时，当前动作正处于下拉状态，发送控制正转、反转的控制命令时，设备回复“设备忙”错误0005。')
    for value in ['正转', '反转']:
        engine.send_did("WRITE", "电机转动0A04", 电机状态=value)
        engine.expect_did("WRITE", "电机转动0A04", '05 00')
    engine.wait(3, allowed_message=False)

    engine.add_doc_info("控制前置工装通断电，测试设备指示的过程中断电，重启后被测设备仍可以正常运行")
    power_control()
    engine.add_doc_info("抄读版本及控制通断测试，用时约3s")
    read_write_test()

    engine.wait(120, tips='设备搜索全部功能测试结束')
