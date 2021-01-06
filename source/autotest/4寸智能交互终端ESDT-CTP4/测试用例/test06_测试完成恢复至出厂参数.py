# encoding:utf-8
# 导入测试引擎

from autotest.公共用例.public常用测试模块 import *

测试组说明 = "测试完成恢复出厂参数"

config = engine.get_config()


def test_测试完成恢复出厂参数():
    """
    01_测试完成恢复出厂状态
    """
    # 清除前置测试工装和测试设备的PANID密钥
    engine.add_doc_info("清除前置测试工装和测试设备的PANID")
    engine.report_check_enable_all(True)

    # 清除前置测试工装的PANID
    clear_gw_info(aid=config["前置通断电工装AID"], pw=config["前置通断电工装PWD"])
    # 清除测试设备的PANID
    clear_gw_info()
    engine.wait(20)
    engine.report_check_enable_all(False)

    # 所有的状态和配置参数恢复至出厂参数
    engine.add_doc_info("所有的状态和配置参数恢复至出厂参数")
    engine.send_did("WRITE", "复位等待时间CD00", "00")
    engine.expect_did("WRITE", "复位等待时间CD00", "00")
    engine.send_did("WRITE", "通断操作C012", "01")
    engine.expect_did("WRITE", "通断操作C012", "00")

    # 前置工装通断电，然后进行测试参数验证
    power_control()
    engine.send_did("READ", "通断操作C012")
    engine.expect_did("READ", "通断操作C012", "00")
    engine.send_did("READ", "继电器上电状态C060")
    engine.expect_did("READ", "继电器上电状态C060", "02")
    engine.send_did("READ", "主动上报使能标志D005")
    engine.expect_did("READ", "主动上报使能标志D005", "0A 03")

