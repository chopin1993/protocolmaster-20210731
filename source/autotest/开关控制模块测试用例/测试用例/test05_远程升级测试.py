# encoding:utf-8
# 导入测试引擎

from autotest.公共用例.public常用测试模块 import *
from autotest.公共用例.public05远程升级测试 import *

测试组说明 = "远程升级测试"

config = engine.get_config()
config['应用程序上一版发布版本'] = "ESACT-1A(v1.4)-20171020"
config['应用程序同版本号测试版本'] = "ESACT-1A(v1.5)-20200808"
config['载波适配层上一版本'] = "ESMD-AD63(v2.1)-20170210"
config['载波网络层上一版本'] = "SSC1663-PLC(v1.0)-20170510"
config['升级后等待重启时间'] = 30

def check_update_configure(version=config["设备描述信息设备制造商0003"],
                           adaptor=config["适配层版本号0606"],
                           network=config["网络层版本号060A"]):
    """
    查询升级前后参数，验证升级前后，SN、DK、配置参数要求保持一致，前后不变
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
    engine.send_did("READ", "继电器过零点动作延迟时间C020", "01")
    engine.expect_did("READ", "继电器过零点动作延迟时间C020", "01 20 20")
    engine.send_did("READ", "主动上报使能标志D005")
    engine.expect_did("READ", "主动上报使能标志D005", 传感器类型="未知", 上报命令="上报网关")
    engine.send_did("READ", "设备运行状态信息统计E019", E019设备信息项="延时关闭时间毫秒")
    engine.expect_did("READ", "设备运行状态信息统计E019", E019设备信息项="延时关闭时间毫秒", 时间=600000)

config['检测版本号和参数保持不变'] = check_update_configure

def init_升级测试环境搭建():
    """
    00_测试环境搭建
    1、将测试工装和测试设备连接，上电搭建好测试环境，要求抄控器、测试工装、测试设备均处于同一网关PANID内；
    2、查询当前设备的版本，确定为本次提交测试的版本；
    3、设置开关控制模块的参数，要求与默认参数不一致，验证升级前后，参数是否会变化；
    """
    # 继电器上电状态C060为00上电状态为上电断开
    engine.send_did("WRITE", "继电器上电状态C060", "00")
    engine.expect_did("WRITE", "继电器上电状态C060", "00")
    # 继电器过零点动作延迟时间C020设置为01 20 20
    engine.send_did("WRITE", "继电器过零点动作延迟时间C020", "01 20 20")
    engine.expect_did("WRITE", "继电器过零点动作延迟时间C020", "01 20 20")
    # 主动上报使能标志D005设置为01 上报网关
    engine.send_did("WRITE", "主动上报使能标志D005", 传感器类型="未知", 上报命令="上报网关")
    engine.expect_did("WRITE", "主动上报使能标志D005", 传感器类型="未知", 上报命令="上报网关")
    # 设备运行状态信息统计E019设置延时闭合时间为6000ms
    engine.send_did("WRITE", "设备运行状态信息统计E019", E019设备信息项="延时关闭时间毫秒", 时间=600000)
    engine.expect_did("WRITE", "设备运行状态信息统计E019", E019设备信息项="延时关闭时间毫秒", 时间=600000)


def test_升级过程中被控制():
    """
    08_升级过程中被控制
    升级过程中被单点控制、情景模式控制，均可以正常响应
    """

    def device_ctrl(second):
        if second == 10:
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

    check_update_configure(version=config["设备描述信息设备制造商0003"])

    engine.update("ESACT-1S1A(v1.5)-20200808.bin", None, device_ctrl)
    engine.wait(30, tips="设备升级完成，校验版本")
    # 升级后
    check_update_configure(version=mcu_update_version)


def test_兼容性升级测试():
    """
    09_兼容性升级测试（已发布版本升级至提测版本）
    从之前的发布版本升级至本次测试版本，要求升级后正常运行，参数前后一致
    为满足自动化测试的一致性，采用先升级回上一版程序，再升级至本版测试程序的方式，验证升级的兼容性
    此处测试完毕，人工增加测试，采用烧写程序的方式，模拟上一版程序，且被配置使用，升级至本版测试程序
    1、首先进行应用程序版本验证和参数验证
    2、升级至上一发布版应用程序程序：ESACT-1A(v1.5)-20200805升级至ESACT-1A(v1.4)-20171020
    3、升级成功后再次应用程序版本验证和参数验证，版本号变更，其余的参数不变
    （因为v1.4版本不支持新增的数据标识C060和E019，所以会报错00 04，属于正常现象）
    4、再次升级回最新发布版本版应用程序：ESACT-1A(v1.4)-20171020升级至ESACT-1A(v1.5)-20200805
    5、升级成功后再次应用程序版本验证和参数验证，版本号变更，其余的参数不变
    """
    # 为满足自动化测试的一致性，采用先升级回上一版程序，再升级至本版测试程序的方式，验证升级的兼容性
    # 此处测试完毕，人工增加测试，采用烧写程序的方式，模拟上一版程序，且被配置使用，升级至本版测试程序
    # 升级前查看版本和配置信息
    check_update_configure(version=config["设备描述信息设备制造商0003"])
    engine.update("ESACT-1S1A(v1.4)-20171020.bin")
    engine.wait(30)
    # 升级后查看版本和配置信息
    # （因为v1.4版本不支持新增的数据标识C060和E019，所以会报错00 04，属于正常现象）
    engine.send_did("READ", "设备描述信息设备制造商0003")
    engine.expect_did("READ", "设备描述信息设备制造商0003", mcu_release_version)

    engine.send_did("READ", "适配层版本号0606")
    engine.expect_did("READ", "适配层版本号0606", config["适配层版本号0606"])
    engine.send_did("READ", "网络层版本号060A")
    engine.expect_did("READ", "网络层版本号060A", config["网络层版本号060A"])
    engine.send_multi_dids("READ",
                           "设备类型0001", "",
                           "设备描述信息设备制造商0003", "",
                           "DKEY0005", "",
                           "SN0007", "")
    engine.expect_multi_dids("READ",
                             "设备类型0001", config["设备类型0001"],
                             "设备描述信息设备制造商0003", mcu_release_version,
                             "DKEY0005", config["DKEY0005"],
                             "SN0007", config["SN0007"])
    engine.send_did("READ", "继电器上电状态C060")
    engine.expect_did("READ", "继电器上电状态C060", "04 00")
    engine.send_did("READ", "继电器过零点动作延迟时间C020", "01")
    engine.expect_did("READ", "继电器过零点动作延迟时间C020", "01 20 20")
    engine.send_did("READ", "主动上报使能标志D005")
    engine.expect_did("READ", "主动上报使能标志D005", 传感器类型="未知", 上报命令="上报网关")
    engine.send_did("READ", "设备运行状态信息统计E019", E019设备信息项="延时关闭时间毫秒")
    engine.expect_did("READ", "设备运行状态信息统计E019", "04 00")

    engine.update("ESACT-1S1A(v1.5)-20200805.bin")
    engine.wait(30)
    # 升级后再次查看版本和配置信息
    check_update_configure(version=config["设备描述信息设备制造商0003"])
