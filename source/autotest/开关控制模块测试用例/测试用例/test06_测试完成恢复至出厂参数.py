# encoding:utf-8
# 导入测试引擎

import engine

from .常用测试模块 import *

测试组说明 = "测试完成恢复出厂参数"

config = engine.get_config()


def test_测试完成恢复出厂参数():
    """
    测试完成恢复出厂状态
    """
    # 清除前置测试工装和测试设备的PANID密钥
    engine.add_doc_info("清除前置测试工装和测试设备的PANID")
    # 清除前置测试工装的PANID
    engine.send_local_msg("设置PANID", 0)
    engine.expect_local_msg("确认")
    engine.send_did("WRITE", "载波芯片注册信息0603",
                    aid=778856,
                    panid=0,
                    pw=39751,
                    device_gid=config["抄控器默认源地址"],
                    sid=1,
                    taid=778856)

    engine.expect_did("WRITE", "载波芯片注册信息0603", "** ** ** ** ** **", said=778856, check_seq=False)
    engine.wait(20)
    # 清除测试设备的PANID
    clear_gw_info()
    engine.wait(20)

    # 所有的状态和配置参数恢复至出厂参数
    engine.add_doc_info("所有的状态和配置参数恢复至出厂参数")

    engine.send_did("WRITE", "通断操作C012", "01")
    engine.expect_did("WRITE", "通断操作C012", "00")
    engine.send_did("WRITE", "继电器上电状态C060", "02")
    engine.expect_did("WRITE", "继电器上电状态C060", "02")
    engine.send_did("WRITE", "继电器过零点动作延迟时间C020", "01 0A 1E")
    engine.expect_did("WRITE", "继电器过零点动作延迟时间C020", "01 0A 1E")
    engine.send_did("WRITE", "主动上报使能标志D005", 传感器类型="未知", 上报命令="同时上报设备和网关")
    engine.expect_did("WRITE", "主动上报使能标志D005", 传感器类型="未知", 上报命令="同时上报设备和网关")
    engine.send_did("WRITE", "设备运行状态信息统计E019", E019设备信息项="延时关闭时间毫秒", 时间=0)
    engine.expect_did("WRITE", "设备运行状态信息统计E019", E019设备信息项="延时关闭时间毫秒", 时间=0)
    # 前置工装通断电，然后进行测试参数验证
    power_off_test()
    engine.send_did("READ", "通断操作C012")
    engine.expect_did("READ", "通断操作C012", "00")
    engine.send_did("READ", "继电器上电状态C060")
    engine.expect_did("READ", "继电器上电状态C060", "02")
    engine.send_did("READ", "继电器过零点动作延迟时间C020", "01")
    engine.expect_did("READ", "继电器过零点动作延迟时间C020", "01 0A 1E")
    # xx(通道)xx（继电器断开延迟时间）xx（继电器闭合延迟时间） 默认断开延时1ms，默认闭合延时3ms
    engine.send_did("READ", "主动上报使能标志D005")
    engine.expect_did("READ", "主动上报使能标志D005", "00 03")
    engine.send_did("READ", "设备运行状态信息统计E019", "08")
    engine.expect_did("READ", "设备运行状态信息统计E019", "08 00 00 00 00")

#
# def test_test():
#     """
#     test
#     """
#     pass