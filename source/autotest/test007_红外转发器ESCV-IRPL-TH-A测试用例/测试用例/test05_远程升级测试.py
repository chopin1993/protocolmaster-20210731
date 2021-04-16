﻿# encoding:utf-8
# 导入测试引擎
from autotest.公共用例.public05远程升级测试 import *
from .常用测试模块 import *

测试组说明 = "远程升级测试"

config = engine.get_config()
config["应用程序上一版发布版本"] = "ESCV-IRPL-TH-A(v1.7)-20200729"
config["应用程序同版本号测试版本"] = "ESCV-IRPL-TH-A(v1.8)-20210122"
# 根据被测设备不同的载波版本，分别设置1663和1667参数
# config["载波适配层上一版本"] = "ESMD-AD63(v2.1)-20170210"
# config["载波网络层上一版本"] = "SSC1663-PLC(v1.0)-20170510"
config["载波适配层上一版本"] = "ESMD-AD6768(v1.1)-20180706"
config["载波网络层上一版本"] = "SSC1667-PLC(v5.0)-20180706"
config["升级后等待重启时间"] = 15  # 默认30s，可根据具体设备升级后重启时间为例修改


def check_update_configure(version=config["设备描述信息设备制造商0003"],
                           adaptor=config["适配层版本号0606"],
                           network=config["网络层版本号060A"]):
    """
    查询升级前后参数，验证版本号变更，验证升级前后，SN、DK、配置参数要求保持一致，前后不变
    """
    engine.send_did("READ", "设备描述信息设备制造商0003")
    engine.expect_did("READ", "设备描述信息设备制造商0003", version)

    engine.send_did("READ", "适配层版本号0606")
    engine.expect_did("READ", "适配层版本号0606", adaptor)
    engine.send_did("READ", "网络层版本号060A")
    engine.expect_did("READ", "网络层版本号060A", network)
    engine.send_multi_dids("READ",
                           "设备类型0001", "",
                           "设备描述信息设备制造商0003", "",
                           "DKEY0005", "",
                           "SN0007", "")
    engine.expect_multi_dids("READ",
                             "设备类型0001", config["设备类型0001"],
                             "设备描述信息设备制造商0003", version,
                             "DKEY0005", config["DKEY0005"],
                             "SN0007", config["SN0007"])

    modify_default_configuration(modify=False, verify=True)


config["检测版本号和参数保持不变"] = check_update_configure


def init_升级测试环境搭建():
    """
    00_测试环境搭建
    1、将测试工装和测试设备连接，上电搭建好测试环境，要求测试工装、测试设备均处于同一网关PANID内；
    2、查询当前设备的版本，确定为本次提交测试的版本；
    3、设置被测设备的参数，要求与默认参数不一致，验证升级前后，参数是否会变化；
    """
    engine.report_check_enable_all(True)
    # 设置被测设备密钥
    report_gateway_expect(wait_enable=False)

    engine.add_doc_info('通过抄控器设置被测设备的参数，使之与默认参数不一致，验证升级前后参数是否会发生变化')
    modify_default_configuration(modify=True, verify=True)

    engine.report_check_enable_all(False)


def test_升级过程中被控制():
    """
    08_升级过程中被控制
    升级过程中被单点控制、情景模式控制，均可以正常响应
    """

    def device_ctrl(second):
        if second == 15:
            engine.wait(3)
            for i in range(10):
                if i % 2 == 0:
                    engine.send_did("WRITE", "红外直接发送0902", "00 00 01 00")
                    engine.expect_did("WRITE", "红外直接发送0902", "00 00 01 00")
                    engine.wait(1)
                else:
                    engine.send_did("WRITE", "红外直接发送0902", "00 00 FE FF")
                    engine.expect_did("WRITE", "红外直接发送0902", "00 00 FE FF")
                    engine.wait(1)

    engine.add_doc_info("升级前，查询版本及SN、DK、配置参数")
    check_update_configure(version=config["设备描述信息设备制造商0003"])

    engine.update(config["应用程序同版本号测试版本"], None, device_ctrl)
    engine.wait(config["升级后等待重启时间"], tips="设备升级完成，校验版本")
    engine.add_doc_info("升级后，查询版本及SN、DK、配置参数，要求版本号变更，其余参数不变")
    check_update_configure(version=config["应用程序同版本号测试版本"])

    # 再升级回测试版本
    engine.update(config["设备描述信息设备制造商0003"], None, device_ctrl)
    engine.wait(config["升级后等待重启时间"], tips="设备升级完成，校验版本")
    engine.add_doc_info("升级后，查询版本及SN、DK、配置参数，要求版本号变更，其余参数不变")
    check_update_configure(version=config["设备描述信息设备制造商0003"])


def test_兼容性升级测试():
    """
    09_兼容性升级测试（已发布版本升级至提测版本）
    从之前的发布版本升级至本次测试版本，要求升级后正常运行，参数前后一致
    为满足自动化测试的一致性，采用先升级回上一版程序，再升级至本版测试程序的方式，验证升级的兼容性
    此处测试完毕，人工增加测试，采用烧写程序的方式，模拟上一版程序，且被配置使用，升级至本版测试程序
    1、首先进行应用程序版本验证和参数验证
    2、升级至上一发布版应用程序程序：
    3、升级成功后再次应用程序版本验证和参数验证，版本号变更，其余的参数不变
    4、再次升级回最新发布版本版应用程序：
    5、升级成功后再次应用程序版本验证和参数验证，版本号变更，其余的参数不变
    """

    engine.add_doc_info("升级前，查询版本及SN、DK、配置参数")
    check_update_configure(version=config["设备描述信息设备制造商0003"])

    engine.update(config["应用程序上一版发布版本"])
    engine.wait(config["升级后等待重启时间"], tips="设备升级完成，校验版本")
    engine.add_doc_info("升级后，查询版本及SN、DK、配置参数")
    check_update_configure(version=config["应用程序上一版发布版本"])

    engine.update(config["设备描述信息设备制造商0003"])
    engine.wait(config["升级后等待重启时间"], tips="设备升级完成，校验版本")
    # 升级后再次查看版本和配置信息
    check_update_configure(version=config["设备描述信息设备制造商0003"])
    # 断电重启后，再次查看版本和配置信息
    power_control()
    check_update_configure(version=config["设备描述信息设备制造商0003"])


def test_升级结束后恢复默认参数():
    """
    10_升级结束后恢复默认参数
    """
    return_to_factory()
