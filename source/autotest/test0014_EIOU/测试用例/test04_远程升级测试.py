# encoding:utf-8
# 导入测试引擎
from autotest.公共用例.public05远程升级测试 import *
from .常用测试模块 import *

测试组说明 = "远程升级测试"

config = engine.get_config()
config["应用程序上一版发布版本"] = "ES-EIOU-9(v1.0)-20210712"  # 如果此处为空字符串时，表示不支持兼容性升级或手动测试。
config["应用程序同版本号测试版本"] = "ES-EIOU-9(v1.0)-20210715"
# 根据被测设备不同的载波版本，分别设置1663和1667参数
# config["载波适配层上一版本"] = "ESMD-AD63(v2.1)-20170210"
# config["载波网络层上一版本"] = "SSC1663-PLC(v1.0)-20170510"
# config["载波适配层上一版本"] = "ESMD-AD6768(v1.1)-20180706"
# config["载波网络层上一版本"] = "SSC1667-PLC(v5.0)-20180706"
config["升级后等待重启时间"] = 15  # 默认30s，可根据具体设备升级后重启时间为例修改


def check_update_configure(version=config["设备描述信息设备制造商0003"],
                           ):
    """
    查询升级前后参数，验证版本号变更，验证升级前后，SN、DK、配置参数要求保持一致，前后不变
    """
    engine.send_did("READ", "设备描述信息设备制造商0003")
    engine.expect_did("READ", "设备描述信息设备制造商0003", version)


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


config["检测版本号和参数保持不变"] = check_update_configure





def test_升级过程中被控制():
    """
    08_升级过程中被控制
    升级过程中配置UI05、UI08，均可以正常响应
    """



    engine.add_doc_info("升级前，查询版本及SN、DK、配置参数")
    engine.send_did("WRITE", "IO配置D201", "05 20")
    engine.expect_did("WRITE", "IO配置D201", "05 20")
    engine.send_did("WRITE", "IO配置D201", "08 00")
    engine.expect_did("WRITE", "IO配置D201", "08 00")
    check_update_configure(version=config["设备描述信息设备制造商0003"])

    engine.update(config["应用程序同版本号测试版本"], None,)
    engine.wait(config["升级后等待重启时间"], tips="设备升级完成，校验版本")
    engine.add_doc_info("升级后，查询版本及SN、DK、配置参数，要求版本号变更，其余参数不变")
    engine.send_did("READ", "IO配置D201", "05")
    engine.expect_did("READ", "IO配置D201", "05 20")
    engine.send_did("READ", "IO配置D201", "08")
    engine.expect_did("READ", "IO配置D201", "08 00")
    check_update_configure(version=config["应用程序同版本号测试版本"])

    # 再升级回测试版本
    engine.update(config["设备描述信息设备制造商0003"], None, )
    engine.wait(config["升级后等待重启时间"], tips="设备升级完成，校验版本")
    engine.add_doc_info("升级后，查询版本及SN、DK、配置参数，要求版本号变更，其余参数不变")
    engine.send_did("READ", "IO配置D201", "05")
    engine.expect_did("READ", "IO配置D201", "05 20")
    engine.send_did("READ", "IO配置D201", "08")
    engine.expect_did("READ", "IO配置D201", "08 00")
    check_update_configure(version=config["设备描述信息设备制造商0003"])


def test_兼容性升级测试():
    """
    09_兼容性升级测试（已发布版本升级至提测版本）
    从之前的发布版本升级至本次测试版本，要求升级后正常运行，参数前后一致
    为满足自动化测试的一致性，采用先升级回上一版程序，再升级至本版测试程序的方式，验证升级的兼容性
    此处测试完毕，人工增加测试，采用烧写程序的方式，模拟上一版程序，且被配置使用，升级至本版测试程序
    1、首先进行应用程序版本验证和参数验证
    2、升级至上一发布版应用程序程序：
    3、升级成功后再次应用程序版本验证和参数验证，版本号变更，
    4、再次升级回最新发布版本版应用程序：
    5、升级成功后再次应用程序版本验证和参数验证，版本号变更，其余的参数不变
    """

    engine.add_doc_info("升级前，查询版本及SN、DK、配置参数")
    check_update_configure(version=config["设备描述信息设备制造商0003"])

    engine.update(config["应用程序上一版发布版本"])
    engine.wait(config["升级后等待重启时间"], tips="设备升级完成，校验版本")
    engine.add_doc_info("升级后，查询版本及SN、DK、配置参数")


    engine.send_did("READ", "设备描述信息设备制造商0003")
    engine.expect_did("READ", "设备描述信息设备制造商0003", config["应用程序上一版发布版本"])

    engine.send_multi_dids("READ",
                           "设备类型0001", "",
                           "设备描述信息设备制造商0003", "",
                           "DKEY0005", "",
                           "SN0007", "")
    engine.expect_multi_dids("READ",
                             "设备类型0001", config["设备类型0001"],
                             "设备描述信息设备制造商0003", config["应用程序上一版发布版本"],
                             "DKEY0005", config["DKEY0005"],
                             "SN0007", config["SN0007"])

    engine.send_did("WRITE", "IO配置D201", "01 20")
    engine.expect_did("WRITE", "IO配置D201", "01 20")
    engine.send_did("WRITE", "IO配置D201", "09 FF")
    engine.expect_did("WRITE", "IO配置D201", "09 FF")

    engine.update(config["设备描述信息设备制造商0003"])
    engine.wait(config["升级后等待重启时间"], tips="设备升级完成，校验版本")
    # 升级后再次查看版本和配置信息
    check_update_configure(version=config["设备描述信息设备制造商0003"])
    # 断电重启后，再次查看版本和配置信息
    power_control()
    check_update_configure(version=config["设备描述信息设备制造商0003"])
    engine.send_did("READ", "IO配置D201", "01")
    engine.expect_did("READ", "IO配置D201", "01 20")
    engine.send_did("READ", "IO配置D201", "09")
    engine.expect_did("READ", "IO配置D201", "09 FF")



