#!/usr/bin/evn python
# -*- coding: utf-8 -*-
"""
@Time: 2021/4/6 9:50
@Author: yang
@File: test04_载波通信功能测试.py
@Software: PyCharm
"""

from autotest.公共用例.public常用测试模块 import *
from .常用测试模块 import *
import time

测试组说明 = "载波通信功能测试"


def test_频繁通断电测试():
    """
    01_频繁通断电测试
    1、将小批测试的设备，全部通过自动化测试工装的继电器控制通断，达到通断电的目的；
    2、测试频繁通断电前后，均查询复位次数060D，然后做差，要求结果与频繁通断电次数一致；
    3、将通断电频率设置大约为5min一次，每次上电后，等待15s，设备上电初始化完成，然后查询与控制设备；
    4、等待2min，再次查询与控制设备；
    5、根据每轮测试用时，控制测试频率在5min通段一次；
    """
    counts = 2  # 频繁通断电测试次数
    devices = [860846]  # 测试设备清单

    def read_and_control():
        engine.send_did("READ", "设备描述信息设备制造商0003", "", taid=aid)
        engine.expect_did("READ", "设备描述信息设备制造商0003", config["设备描述信息设备制造商0003"], said=aid)
        engine.send_did("READ", "主动上报使能标志D005", taid=aid)
        engine.expect_did("READ", "主动上报使能标志D005", "03 03", said=aid)
        engine.wait(1)

    def power_control(init_time=config["被测设备上电后初始化时间"]):
        """
        测试工装控制通断电
        通过控制工装通断，实现给测试设备的通断电，实现断电测试场景
        passed_time 断电重启后设备用时
        """
        start_time = time.time()
        engine.add_doc_info("测试工装控制通断电")
        engine.wait(seconds=1, tips='保证和之前的测试存在1s间隔')
        engine.control_relay(0, 0)
        engine.wait(seconds=10, tips='保证被测设备充分断电')
        engine.control_relay(0, 1)
        engine.wait(seconds=init_time)  # 普通载波设备上电初始化，预留足够时间供载波初始化
        passed_time = time.time() - start_time

        return passed_time

    def read_060D():
        for aid in devices:
            engine.send_did("READ", "SSC1667和SSC1668复位信息060D", "", taid=aid)
            engine.expect_did("READ", "SSC1667和SSC1668复位信息060D", '** ' * 51 + '*', said=aid)

    # 设置抄控器本地密钥，默认为0，可根据实际网关PANID设置。
    engine.add_doc_info('设置抄控器本地密钥，默认为11176，可根据实际网关PANID设置。')
    engine.send_local_msg("设置PANID", 11176)
    engine.expect_local_msg("确认")

    engine.add_doc_info('1、测试频繁通断电前，查看各个被测设备的复位次数')
    read_060D()
    engine.add_doc_info('2、通过自动化测试工装的继电器控制通断 {} 次'.format(counts))

    for count in range(counts):

        engine.add_doc_info("*********第{}次通断电测试*********".format(count + 1))
        start_time = time.time()

        power_control()
        for aid in devices:
            engine.add_doc_info('测试设备AID为 {} '.format(aid))
            read_and_control()
        engine.wait(120, tips='等待2min，再次查询与控制设备')
        for aid in devices:
            engine.add_doc_info('测试设备AID为 {} '.format(aid))
            read_and_control()
        passed = time.time() - start_time

        if (300 - passed) > 0:
            engine.wait((300 - passed), tips='本轮测试用时为{:.3f}秒，为保证通断频率为5min，继续等待{:.3f}秒'.format(passed, (300 - passed)))

    engine.add_doc_info('3、测试频繁通断电后，查看各个被测设备的复位次数')
    read_060D()
