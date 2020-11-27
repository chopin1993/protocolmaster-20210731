# encoding:utf-8
# 导入测试引擎
import engine


# from .常用测试模块 import *

def power_off_test(time=15):
    """
    前置工装通断电
    抄控器通过报文控制大功率计量遥控开关通断，实现给测试设备的通断电
    """
    engine.wait(seconds=1)  # 保证和之前的测试存在1s间隔
    engine.send_did("WRITE", "通断操作C012", "01", taid=778856)
    engine.expect_did("WRITE", "通断操作C012", "00", said=778856)
    engine.wait(seconds=5)  # 充分断电
    engine.send_did("WRITE", "通断操作C012", "81", taid=778856)
    engine.expect_did("WRITE", "通断操作C012", "01", said=778856)
    if time != 0:
         engine.wait(seconds=time)  # 普通载波设备上电初始化时间约10s，预留足够时间供载波初始化


def clear_gw_info():
    """
    清除网关PANID信息，模拟出厂设备
    r"4aid+2panid+2pw+4gid+2sid"
    """
    config = engine.get_config()

    engine.send_local_msg("设置PANID", 0)
    engine.expect_local_msg("确认")
    engine.wait(1)
    engine.send_did("WRITE", "载波芯片注册信息0603",
                    aid=config["测试设备地址"],
                    panid=0,
                    pw=config["设备PWD000A"],
                    device_gid=config["抄控器默认源地址"],
                    sid=1)
    engine.expect_did("WRITE", "载波芯片注册信息0603", "** ** ** ** ** **", check_seq=False)


def set_gw_info():
    """
    设置网关PANID信息，模拟设备入网
    r"4aid+2panid+2pw+4gid+2sid"
    """
    config = engine.get_config()
    engine.send_local_msg("设置PANID", config["panid"])
    engine.expect_local_msg("确认")
    engine.wait(1)
    engine.send_did("WRITE", "载波芯片注册信息0603",
                    aid=config["测试设备地址"],
                    panid=config["panid"],
                    pw=config["设备PWD000A"],
                    device_gid=config["抄控器默认源地址"],
                    sid=8)
    engine.expect_did("WRITE", "载波芯片注册信息0603", "** ** ** ** ** **", check_seq=False)


def set_subscriber(name, aid):
    """
    配置订阅者信息
    按照不同的数量配置订阅者，
    开关控制模块最多支持3个订阅，
    超过3个时自动将最早的订阅者替换
    """
    panel = engine.create_role(name, aid)
    panel.send_did("WRITE", "通断操作C012", "81")
    panel.expect_did("WRITE", "通断操作C012", "01")
    engine.wait(0.5)
    panel.send_did("WRITE", "通断操作C012", "01")
    panel.expect_did("WRITE", "通断操作C012", "00")
    engine.wait(0.5)
    return panel

