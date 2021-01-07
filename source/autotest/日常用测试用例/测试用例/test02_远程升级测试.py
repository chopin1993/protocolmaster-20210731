# encoding:utf-8
# 导入测试引擎
import engine
from autotest.公共用例.public常用测试模块 import *

测试组说明 = "远程升级测试"

config = engine.get_config()
config["应用程序上一版发布版本"] = "ESACT-CC1-AC-A-63(v1.4)-20200309"
config["应用程序同版本号测试版本"] = "ESACT-CC1-AC-A-63(v1.5)-20201207D1"
config["升级后等待重启时间"] = 50  # 默认30s，可根据具体设备升级后重启时间为例修改


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


config["检测版本号和参数保持不变"] = check_update_configure


def test_兼容性升级测试():
    """
    09_兼容性升级测试（已发布版本升级至提测版本）
    从之前的发布版本升级至本次测试版本，要求升级后正常运行，参数前后一致
    为满足自动化测试的一致性，采用先升级回上一版程序，再升级至本版测试程序的方式，验证升级的兼容性
    此处测试完毕，人工增加测试，采用烧写程序的方式，模拟上一版程序，且被配置使用，升级至本版测试程序
    """
    for i in range(10):
        engine.add_doc_info("测试第"+str(i)+"次升级任务：")

        engine.add_doc_info("升级前，查询版本及SN、DK、配置参数")
        check_update_configure(version=config["设备描述信息设备制造商0003"])
        engine.update(config["应用程序上一版发布版本"])
        engine.wait(config["升级后等待重启时间"], tips="设备升级完成，校验版本")
        check_update_configure(version=config["应用程序上一版发布版本"])

        # 从上一发布版本升级回当前测试版本
        engine.update(config["设备描述信息设备制造商0003"])
        engine.wait(config["升级后等待重启时间"], tips="设备升级完成，校验版本")
        # 升级后再次查看版本和配置信息
        check_update_configure(version=config["设备描述信息设备制造商0003"])
