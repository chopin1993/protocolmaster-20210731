# encoding:utf-8
# 导入测试引擎
import engine
from autotest.公共用例.public常用测试模块 import *
from autotest.公共用例.public05远程升级测试 import *

测试组说明 = "远程升级测试"
"""
1、智能交互终端的程序，只支持向更高版本升级，不支持降级升级；
2、为满足测试，需要有过渡用的升级测试程序，config["应用程序同版本号测试版本"] 需要升级包外壳版本号高于当前测试版本，
内部程序版本号低于当前测试版本，使智能交互终端可以重复升级测试；联系研发人员提供；
"""
config = engine.get_config()
config["应用程序上一版发布版本"] = "ESDT-CTP4(v1.4)-20200518"
config["应用程序同版本号测试版本"] = "ESDT-CTP4(v2.4)-20220513"
config["载波适配层上一版本"] = "ESMD-AD6768(v1.1)-20180706"
config["载波网络层上一版本"] = "SSC1667-PLC(v5.0)-20180706"
config["升级后等待重启时间"] = 250  # 默认30s，可根据具体设备升级后重启时间为例修改


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
    engine.send_did("READ", "继电器上电状态C060")
    engine.expect_did("READ", "继电器上电状态C060", "00")
    engine.send_did("READ", "主动上报使能标志D005")
    engine.expect_did("READ", "主动上报使能标志D005", 传感器类型="通断", 上报命令="上报网关")



config["检测版本号和参数保持不变"] = check_update_configure


def init_升级测试环境搭建():
    """
    00_测试环境搭建
    1、将测试工装和测试设备连接，上电搭建好测试环境，要求抄控器、测试工装、测试设备均处于同一网关PANID内；
    2、查询当前设备的版本，确定为本次提交测试的版本；
    3、设置被测设备的参数，要求与默认参数不一致，验证升级前后，参数是否会变化；
    """
    engine.report_check_enable_all(True)
    # 设置前置测试工装密钥
    set_gw_info(aid=config["前置通断电工装AID"],pw=config["前置通断电工装PWD"])
    # 设置被测设备密钥
    set_gw_info()
    engine.wait(seconds=1)
    # 继电器上电状态C060为00上电状态为上电断开
    engine.send_did("WRITE", "继电器上电状态C060", "00")
    engine.expect_did("WRITE", "继电器上电状态C060", "00")

    # 主动上报使能标志D005设置为01 上报网关
    engine.send_did("WRITE", "主动上报使能标志D005", 传感器类型="未知", 上报命令="上报网关")
    engine.expect_did("WRITE", "主动上报使能标志D005", 传感器类型="未知", 上报命令="上报网关")


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
                    engine.send_did("WRITE", "通断操作C012", "81")
                    engine.expect_did("WRITE", "通断操作C012", "01")
                    engine.wait(1)
                else:
                    engine.send_did("WRITE", "通断操作C012", "01")
                    engine.expect_did("WRITE", "通断操作C012", "00")
                    engine.wait(1)
    engine.add_doc_info("升级前，查询版本及SN、DK、配置参数")
    check_update_configure(version=config["设备描述信息设备制造商0003"])

    engine.update(config["应用程序同版本号测试版本"], None, device_ctrl)
    engine.wait(config["升级后等待重启时间"], tips="设备升级完成，校验版本")
    engine.add_doc_info("升级后，查询版本及SN、DK、配置参数，要求版本号变更，其余参数不变")
    check_update_configure(version=config["应用程序同版本号测试版本"] )

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

    engine.add_doc_info("升级至上一测试版本，查询版本及SN、DK、配置参数")
    check_update_configure(version=config["应用程序上一版发布版本"])

    # 从上一发布版本升级回当前测试版本
    engine.add_doc_info("兼容性升级测试")
    engine.update(config["设备描述信息设备制造商0003"])
    engine.wait(config["升级后等待重启时间"], tips="设备升级完成，校验版本")

    engine.add_doc_info("升级后，查询版本及SN、DK、配置参数")
    check_update_configure(version=config["设备描述信息设备制造商0003"])
    # 断电重启后，再次查看版本和配置信息
    power_control()
    check_update_configure(version=config["设备描述信息设备制造商0003"])
