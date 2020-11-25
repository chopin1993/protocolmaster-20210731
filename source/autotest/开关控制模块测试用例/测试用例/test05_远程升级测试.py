# encoding:utf-8
# 导入测试引擎

import engine

from .常用测试模块 import *

测试组说明 = "远程升级测试"

config = engine.get_config()
mcu_update_version = "ESACT-1A(v1.5)-20200808"


def check_update_configure():
    """
    查询升级前后参数，验证升级前后，SN、DK、配置参数要求保持一致，前后不变
    """
    engine.send_multi_dids("READ", "设备类型0001", "",
                           "DKEY0005", "",
                           "SN0007", "")
    engine.expect_multi_dids("READ", "设备类型0001", config["设备类型0001"],
                             "DKEY0005", config["DKEY0005"],
                             "SN0007", config["SN0007"])
    engine.send_did("READ", "继电器上电状态C060")
    engine.expect_did("READ", "继电器上电状态C060", "00")
    engine.send_did("READ", "继电器过零点动作延迟时间C020", "01")
    engine.expect_did("READ", "继电器过零点动作延迟时间C020", "01 20 20")
    engine.send_did("READ", "主动上报使能标志D005")
    engine.expect_did("READ", "主动上报使能标志D005", 传感器类型="未知", 上报命令="上报网关")
    engine.send_did("READ", "设备运行状态信息统计E019", E019设备信息项="延时关闭时间毫秒")
    engine.expect_did("READ", "设备运行状态信息统计E019", E019设备信息项="延时关闭时间毫秒", 时间=6000)


def test_升级测试环境搭建():
    """
    01_测试环境搭建
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
    engine.send_did("WRITE", "设备运行状态信息统计E019", E019设备信息项="延时关闭时间毫秒", 时间=6000)
    engine.expect_did("WRITE", "设备运行状态信息统计E019", E019设备信息项="延时关闭时间毫秒", 时间=6000)


def test_应用层远程升级():
    """
    02_应用层远程升级（提测版本升级至其他版本）
    1、查询当前版本及SN、DK、配置参数
    2、进行远程升级
    3、升级成功后，再次查询版本及SN、DK、配置参数，要求版本号变更，其余参数不变
    4、断电重启，再次查询版本及SN、DK、配置参数不变
    5、升级回提测版本，再次查询版本及SN、DK、配置参数，要求版本号变更，其余参数不变
    ESACT-1A(v1.5)-20200805升级至ESACT-1A(v1.5)-20200808
    ESACT-1A(v1.5)-20200808升级回ESACT-1A(v1.5)-20200805
    """
    # 升级前，查询版本为ESACT-1S1A(v1.5)-20200805
    engine.send_did("READ", "设备描述信息设备制造商0003")
    engine.expect_did("READ", "设备描述信息设备制造商0003", config["设备描述信息设备制造商0003"])
    check_update_configure()
    engine.update("ESACT-1S1A(v1.5)-20200808.bin")
    engine.wait(30)

    # 升级后，查询版本为ESACT-1S1A(v1.5)-20200808
    engine.send_did("READ", "设备描述信息设备制造商0003")
    engine.expect_did("READ", "设备描述信息设备制造商0003", mcu_update_version)
    check_update_configure()
    # 断电重启，再次查询前版本及SN、DK、配置参数
    power_off_test()
    engine.send_did("READ", "设备描述信息设备制造商0003")
    engine.expect_did("READ", "设备描述信息设备制造商0003", mcu_update_version)
    check_update_configure()

    # 再升级回提测版本
    engine.update("ESACT-1S1A(v1.5)-20200805.bin")
    engine.wait(30)
    # 升级后，查询版本为ESACT-1S1A(v1.5)-20200805
    engine.send_did("READ", "设备描述信息设备制造商0003")
    engine.expect_did("READ", "设备描述信息设备制造商0003", config["设备描述信息设备制造商0003"])
    check_update_configure()


def test_兼容性升级测试():
    """
    03_兼容性升级测试
    从之前的发布版本升级至本次测试版本，要求升级后正常运行，参数前后一致
    1、首先烧写之前的发布版本，然后查询版本号及SN、DK、配置参数
    2、进行远程升级
    3、升级成功后，再次查询版本及SN、DK、配置参数，要求版本号变更，其余参数不变
    4、本项测试需要手动进行验证，期间需要人工参与
    """
    pass


def test_断点续传():
    """
    04_断点续传
    1、查询版本及SN、DK、配置参数
    2、远程升级发送到9包之后，停止发送，模拟环境异常，升级失败，要求设备此时仍能正常工作；
    3、等待3min后，再次触发远程升级，再启动发送，设备会继续请求10包；
    4、升级成功后，再次查询版本及SN、DK、配置参数
    """
    # 读版本号及参数
    engine.send_did("READ", "设备描述信息设备制造商0003")
    engine.expect_did("READ", "设备描述信息设备制造商0003", config["设备描述信息设备制造商0003"])
    check_update_configure()

    reqs = engine.update("ESACT-1S1A(v1.5)-20200808.bin")
    if reqs[0] != 10:
        engine.add_fail_test("断点续传失败")
    engine.wait(30, tips="设备升级完成，校验版本")

    # 读版本号及参数
    engine.send_did("READ", "设备描述信息设备制造商0003")
    engine.expect_did("READ", "设备描述信息设备制造商0003", config["设备描述信息设备制造商0003"])
    check_update_configure()
    engine.wait(180)

    def controller_fun2(seq):
        if seq < 10:
            engine.add_fail_test("断点续传功能失败")
        else:
            return seq

    engine.update("ESACT-1S1A(v1.5)-20200808.bin", controller_fun2)
    engine.wait(30)
    #  读版本号及参数
    engine.send_did("READ", "设备描述信息设备制造商0003")
    engine.expect_did("READ", "设备描述信息设备制造商0003", mcu_update_version)
    check_update_configure()


def test_断电重传():
    """
    05_断电重传
    1、紧接断点续传测试，升级前读取设备的版本信息
    2、升级至9包，控制前置工装进行断电重启，测试重启后要求设备此时仍能正常工作；
    3、重新触发升级，要求从第1包重新开始升级；
    4、升级成功后，读取设备版本号，确保升级成功
    """
    # 读版本号及参数
    engine.send_did("READ", "设备描述信息设备制造商0003")
    engine.expect_did("READ", "设备描述信息设备制造商0003", mcu_update_version)
    check_update_configure()

    def controller_fun(seq):
        if seq < 10:
            return seq
        else:
            return None

    engine.update("ESACT-1S1A(v1.5)-20200805.bin", controller_fun)
    engine.wait(20, tips="请给设备断电")
    #  断电再次验证版本及参数
    power_off_test()
    engine.send_did("READ", "设备描述信息设备制造商0003")
    engine.expect_did("READ", "设备描述信息设备制造商0003", mcu_update_version)
    check_update_configure()
    # 再次触发升级，并获取所有的升级包帧号
    reqs = engine.update("ESACT-1S1A(v1.5)-20200805.bin")

    if reqs[0] != 1:
        engine.add_fail_test("断电重传失败")

    engine.wait(30, tips="设备升级完成，校验版本")

    engine.send_did("READ", "设备描述信息设备制造商0003")
    engine.expect_did("READ", "设备描述信息设备制造商0003", config["设备描述信息设备制造商0003"])
    check_update_configure()


def test_升级过程中被控制():
    """
    06_升级过程中被控制
    升级过程中被单点控制、情景模式控制，均可以正常响应
    """

    def controller_fun(seq):
        import time
        if seq % 40 == 0:
            engine.send_did("WRITE", "通断操作C012", "81")
            engine.expect_did("WRITE", "通断操作C012", "01")
        elif seq % 40 == 2:
            engine.send_did("WRITE", "通断操作C012", "01")
            engine.expect_did("WRITE", "通断操作C012", "00")
        return seq

    engine.send_did("READ", "设备描述信息设备制造商0003")
    engine.expect_did("READ", "设备描述信息设备制造商0003", config["设备描述信息设备制造商0003"])
    check_update_configure()

    engine.update("ESACT-1S1A(v1.5)-20200808.bin", controller_fun)
    engine.wait(30, tips="设备升级完成，校验版本")

    engine.send_did("READ", "设备描述信息设备制造商0003")
    engine.expect_did("READ", "设备描述信息设备制造商0003", config["设备描述信息设备制造商0003"])
    check_update_configure()


def test_升级成功瞬间断电():
    """
    07_升级成功瞬间断电
    1、升级成功瞬间断电，然后再次查询版本及SN、DK、配置参数
    """

    # 升级前

    def controller_fun(seq):
        if seq == 65535:
            import time
            time.sleep(1)  # 保证和之前的测试存在1s间隔
            engine.send_did("WRITE", "通断操作C012", "01", taid=778856)
            engine.expect_did("WRITE", "通断操作C012", "00", said=778856)
            time.sleep(5) # 充分断电
            engine.send_did("WRITE", "通断操作C012", "81", taid=778856)
            engine.expect_did("WRITE", "通断操作C012", "01", said=778856)
            time.sleep(15)  # 普通载波设备上电初始化时间约10s，预留足够时间供载波初始化
            return None
        else:
            return seq

    engine.update("ESACT-1S1A(v1.5)-20200805.bin", controller_fun)

    engine.wait(30)
    # 升级后，查询版本为ESACT-1S1A(v1.5)-20200805
    engine.send_did("READ", "设备描述信息设备制造商0003")
    engine.expect_did("READ", "设备描述信息设备制造商0003", config["设备描述信息设备制造商0003"])
    check_update_configure()
