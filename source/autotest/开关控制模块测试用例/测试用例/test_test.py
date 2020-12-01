# encoding:utf-8
# 导入测试引擎
from autotest.公共用例.常用测试模块 import *

测试组说明 = "test"

config = engine.get_config()


def test_ceshi():
    """
    ceshi
    """
    engine.report_check_enable_all(True)
    engine.add_doc_info("3、测试上报重发机制，收不到网关应答，进行10s、100s重试，重试结束则本次添加上报结束")
    # 前端工装断电重启，模拟上电上报,并且重新上电后后续报文立即计时
    power_off_test(time=0)
    # sid = 8时，上电上报时间 = 60+sid% 100 =68s
    engine.wait(67, allowed_message=False)
    engine.expect_multi_dids("REPORT",
                             "通断操作C012", "**",
                             "导致状态改变的控制设备AIDC01A", config["测试设备地址"], timeout=2)  # 预留1s的误差
    engine.wait(9.5, allowed_message=False)
    engine.add_doc_info("ceshi")
    engine.expect_multi_dids("REPORT",
                             "通断操作C012", "**",
                             "导致状态改变的控制设备AIDC01A", config["测试设备地址"], timeout=1)
    engine.wait(99.5, allowed_message=False)
    engine.add_doc_info("ceshi")
    engine.expect_multi_dids("REPORT",
                             "通断操作C012", "**",
                             "导致状态改变的控制设备AIDC01A", config["测试设备地址"], timeout=1)
    engine.wait(20, allowed_message=False)

    engine.report_check_enable_all(False)


def test_time():
    """
    测试时间的准确性
    """
    import time
    for i in range(10):
        tick = time.time()
        engine.wait(19.5, allowed_message=False)
        passed = time.time() - tick
        print("time cost:", passed)