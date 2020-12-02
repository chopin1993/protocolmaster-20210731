# encoding:utf-8
# 导入测试引擎
import engine
from autotest.公共用例.public常用测试模块 import *


def power_off_test(time=15):
    """
    前置工装通断电
    抄控器通过报文控制大功率计量遥控开关通断，实现给测试设备的通断电
    """
    engine.add_doc_info("前置工装通断电")
    engine.wait(seconds=1)  # 保证和之前的测试存在1s间隔
    engine.send_did("WRITE", "通断操作C012", "01", taid=778856)
    engine.expect_did("WRITE", "通断操作C012", "00", said=778856)
    engine.wait(seconds=5)  # 充分断电
    engine.send_did("WRITE", "通断操作C012", "81", taid=778856)
    engine.expect_did("WRITE", "通断操作C012", "01", said=778856)
    if time != 0:
        engine.wait(seconds=time)  # 普通载波设备上电初始化时间约10s，预留足够时间供载波初始化


def set_subscriber(name, aid):
    """
    配置订阅者信息
    配置订阅者成功后，需要订阅者实际控制被测设备，
    便于被测设备记住订阅者
    """
    panel = engine.create_role(name, aid)
    panel.send_did("WRITE", "通断操作C012", "81")
    panel.expect_did("WRITE", "通断操作C012", "01")
    engine.wait(0.5)
    panel.send_did("WRITE", "通断操作C012", "01")
    panel.expect_did("WRITE", "通断操作C012", "00")
    engine.wait(0.5)
    return panel

def report_expect(devices, write_value="01", expect_value="00", first_timeout=2, gateway=False, ack=True):
    '''
    :param devices:订阅者列表
    :param write_value:写入的值
    :param expect_value:期望上报的值
    '''
    config = engine.get_config()
    engine.send_did("WRITE", "通断操作C012", write_value)
    engine.expect_did("WRITE", "通断操作C012", expect_value)
    for i,panel in enumerate(devices):
        if i == 0:
            panel.expect_did("NOTIFY", "通断操作C012", expect_value, timeout=first_timeout)
        else:
            panel.expect_did("NOTIFY", "通断操作C012", expect_value, timeout=2)

    if gateway:
        engine.expect_multi_dids("REPORT",
                             "通断操作C012", "01",
                             "导致状态改变的控制设备AIDC01A", config["抄控器默认源地址"], timeout=2, ack=ack)
    else:
        engine.wait(10, allowed_message=False)



