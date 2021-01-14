#!/usr/bin/evn python
# -*- coding: utf-8 -*-
"""
@Time: 2021/1/13 9:03
@Author: SUN
@File: test_单独用例验证测试.py
@Software: PyCharm
"""
import engine
from .常用测试模块 import *

测试组说明 = "状态同步测试"
def test_ceshi():
    """
    test_单独测试验证
    """
    from .test04_状态同步测试 import test_订阅者上报顺序测试

    def test():
        report_power_on_expect(wait_times=[68], ack=True, wait_enable=False)
        engine.add_doc_info("配置3个订阅者时：")
        panel01 = set_subscriber("订阅者1", 21)
        panel02 = set_subscriber("订阅者2", 22)
        panel03 = set_subscriber("订阅者3", 23)

        report_subscribe_expect([panel01, panel02, panel03], write_value="81", expect_value="01")
        report_subscribe_expect([panel01, panel02, panel03], write_value="01", expect_value="00")

        engine.add_doc_info("2、订阅者4控制一次，发现上报的顺序变成订阅者4、订阅者2、订阅者3")
        panel04 = set_subscriber("订阅者4", 24)
        report_subscribe_expect([panel04, panel02, panel03], write_value="81", expect_value="01")
        report_subscribe_expect([panel04, panel02, panel03], write_value="01", expect_value="00")

        engine.add_doc_info("3、订阅者1控制一次，发现上报的顺序变成订阅者4、订阅者1、订阅者3")
        panel01 = set_subscriber("订阅者1", 21)
        report_subscribe_expect([panel04, panel01, panel03], write_value="81", expect_value="01")
        report_subscribe_expect([panel04, panel01, panel03], write_value="01", expect_value="00")

        engine.add_doc_info("4、订阅者2控制一次，发现上报的顺序变成订阅者4、订阅者1、订阅者2")
        panel02 = set_subscriber("订阅者2", 22)
        report_subscribe_expect([panel04, panel01, panel02], write_value="81", expect_value="01")
        report_subscribe_expect([panel04, panel01, panel02], write_value="01", expect_value="00")

        engine.add_doc_info("5、订阅者3控制一次，发现上报的顺序变成订阅者3、订阅者1、订阅者2")
        panel03 = set_subscriber("订阅者3", 23)
        report_subscribe_expect([panel03, panel01, panel02], write_value="81", expect_value="01")
        report_subscribe_expect([panel03, panel01, panel02], write_value="01", expect_value="00")

    engine.report_check_enable_all(True)

    for i in range(5):
        engine.add_doc_info('*'*20+'第{}次测试'.format(i+1)+'*'*20)
        test()
    engine.report_check_enable_all(False)

def test_ceshi2():
    """
    test_设备添加入网测试
    """
    engine.report_check_enable_all(True)

    report_gateway_expect(wait_times=[15], ack=True, quit_net=True)

    engine.report_check_enable_all(False)


def test_ceshi3():
    """
     断电重启测试
    """
    ceshi_time = power_control()
    engine.add_doc_info('正常断电重启用时测试{}'.format(ceshi_time))

    ceshi_time = power_control(init_time=0)
    engine.add_doc_info('正常断电重启用时测试{}'.format(ceshi_time))