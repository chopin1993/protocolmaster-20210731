# encoding:utf-8
# 导入测试引擎

from autotest.公共用例.public常用测试模块 import *

测试组说明 = "测试完成恢复出厂参数"

config = engine.get_config()
channel_dict = {1: '01', 2: '02', 3: '04'}  # 设备通道及对应值

def test_测试完成恢复出厂参数():
    """
    测试完成恢复出厂状态
    1、发送调试指令FF00，使设备恢复出厂设置
    此操作恢复出厂设置功能与设备本地按键恢复出厂设置功能相同，清除网关信息，继电器恢复默认状态，其他功能参数恢复至默认，
    硬件相关的参数或特殊应用参数不清除，如继电器校准参数、继电器动作次数、继电器默认上电状态、背光灯参数；
    2、对所有的参数进行验证，保障调试指令正常
    """
    from .test02_功能类协议测试 import test_出厂默认参数

    engine.report_check_enable_all(True)
    clear_gw_info()
    engine.wait(14, allowed_message=False)
    engine.expect_multi_dids("REPORT",
                             "通断操作C012", '00',
                             "导致状态改变的控制设备AIDC01A", config["测试设备地址"], ack=True)
    engine.report_check_enable_all(False)

    engine.add_doc_info("发送调试指令，所有的状态和配置参数恢复至出厂参数")
    engine.send_did("WRITE", "自动测试FC00", 密码=config["设备PWD000A"], 自动测试命令="清除系统所有信息")
    engine.expect_did("WRITE", "自动测试FC00", 密码=config["设备PWD000A"], 自动测试命令="清除系统所有信息")
    engine.wait(10, tips='预留10s时间供设备清除系统所有信息')

    engine.add_doc_info('将自动测试FC00不能清除的关键参数，恢复至出厂默认参数')
    engine.send_did("WRITE", "继电器上电状态C060", "02")
    engine.expect_did("WRITE", "继电器上电状态C060", "02")
    if config["被测设备硬件版本"] == "继电器版本":
        engine.send_did("WRITE", "继电器过零点动作延迟时间C020", "07 33 39 33 39 33 39")
        engine.expect_did("WRITE", "继电器过零点动作延迟时间C020", "07 33 39 33 39 33 39")
    engine.send_did("WRITE", "读写面板默认背光亮度百分比C135", '07 01 01 01')
    engine.expect_did("WRITE", "读写面板默认背光亮度百分比C135", '07 01 01 01')

    engine.add_doc_info("前置工装断电前，进行测试默认参数验证")
    test_出厂默认参数()

    engine.add_doc_info("前置工装通断电后，进行测试默认参数验证")
    power_control()
    test_出厂默认参数()
