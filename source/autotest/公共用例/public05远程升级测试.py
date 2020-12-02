# encoding:utf-8
# 导入测试引擎

from autotest.公共用例.public常用测试模块 import *

config = engine.get_config()

def test_应用层远程升级():
    """
    01_应用层远程升级（提测版本升级至其他版本）
    1、查询当前版本及SN、DK、配置参数
    2、进行远程升级
    3、升级成功后，再次查询版本及SN、DK、配置参数，要求版本号变更，其余参数不变
    4、断电重启，再次查询版本及SN、DK、配置参数不变
    5、升级回提测版本，再次查询版本及SN、DK、配置参数，要求版本号变更，其余参数不变
    ESACT-1A(v1.5)-20200805升级至ESACT-1A(v1.5)-20200808
    ESACT-1A(v1.5)-20200808升级回ESACT-1A(v1.5)-20200805
    """
    # 升级前，查询版本为ESACT-1S1A(v1.5)-20200805
    config['检测版本号和参数保持不变'](version=config["设备描述信息设备制造商0003"])
    engine.update(config['应用程序同版本号测试版本'])
    engine.wait(30)

    # 升级后，查询版本为ESACT-1S1A(v1.5)-20200808
    config['检测版本号和参数保持不变'](version=config['应用程序同版本号测试版本'])
    # 断电重启，再次查询前版本及SN、DK、配置参数
    power_off_test()
    config['检测版本号和参数保持不变'](version=config['应用程序同版本号测试版本'])

    # 再升级回提测版本
    engine.update(config["设备描述信息设备制造商0003"])
    engine.wait(30)
    # 升级后，查询版本为ESACT-1S1A(v1.5)-20200805
    config['检测版本号和参数保持不变'](version=config["设备描述信息设备制造商0003"])

def test_断点续传():
    """
    02_断点续传
    1、查询版本及SN、DK、配置参数
    2、远程升级发送到9包之后，停止发送，模拟环境异常，升级失败，要求设备此时仍能正常工作；
    3、等待3min后，再次触发远程升级，再启动发送，设备会继续请求10包；
    4、升级成功后，再次查询版本及SN、DK、配置参数
    """
    # 读版本号及参数
    config['检测版本号和参数保持不变'](version=config["设备描述信息设备制造商0003"])

    def update_func(seq):
        if seq < 30:
            return seq
        else:
            return None

    engine.update(config['应用程序同版本号测试版本'], update_func)
    engine.wait(2)
    # 读版本号及参数
    config['检测版本号和参数保持不变'](version=config["设备描述信息设备制造商0003"])
    engine.wait(180)

    reqs = engine.update(config['应用程序同版本号测试版本'])
    if reqs[0] != 30:
        engine.add_fail_test("断点续传失败")
    engine.wait(30, tips="设备升级完成，校验版本")

    #  读版本号及参数
    config['检测版本号和参数保持不变'](version=config['应用程序同版本号测试版本'])


def test_断电重传():
    """
    03_断电重传
    1、紧接断点续传测试，升级前读取设备的版本信息
    2、升级至9包，控制前置工装进行断电重启，测试重启后要求设备此时仍能正常工作；
    3、重新触发升级，要求从第1包重新开始升级；
    4、升级成功后，读取设备版本号，确保升级成功
    """
    # 读版本号及参数
    config['检测版本号和参数保持不变'](version=config['应用程序同版本号测试版本'])

    def update_func(seq):
        if seq < 10:
            return seq
        else:
            return None

    engine.update(config["设备描述信息设备制造商0003"], update_func)
    engine.wait(20, tips="请给设备断电")
    #  断电再次验证版本及参数
    power_off_test()
    config['检测版本号和参数保持不变'](version=config['应用程序同版本号测试版本'])

    # 再次触发升级，并获取所有的升级包帧号
    reqs = engine.update(config["设备描述信息设备制造商0003"])

    if reqs[0] != 1:
        engine.add_fail_test("断电重传失败")

    engine.wait(30, tips="设备升级完成，校验版本")

    config['检测版本号和参数保持不变'](version=config["设备描述信息设备制造商0003"])


def test_升级成功瞬间断电():
    """
    04_升级成功瞬间断电
    1、升级成功瞬间断电，然后再次查询版本及SN、DK、配置参数
    """

    # 升级前，查询版本为
    config['检测版本号和参数保持不变'](version=config['应用程序同版本号测试版本'])

    engine.update(config["设备描述信息设备制造商0003"])
    power_off_test()
    engine.wait(30)
    # 升级后，查询版本为ESACT-1S1A(v1.5)-20200805
    config['检测版本号和参数保持不变'](version=config["设备描述信息设备制造商0003"])


def test_相同版本重复升级测试():
    """
    05_相同版本重复升级测试
    1、查询版本及SN、DK、配置参数
    2、触发相同版本升级，升级设备回复0xFFFF立即升级成功
    3、升级成功后，再次查询版本及SN、DK、配置参数
    """
    # 升级前，查询版本为ESACT-1S1A(v1.5)-20200805
    config['检测版本号和参数保持不变'](version=config["设备描述信息设备制造商0003"])
    # 触发相同版本号升级任务
    reqs = engine.update(config["设备描述信息设备制造商0003"])

    if reqs[0] != 65535:
        engine.add_fail_test("相同版本号重复升级，升级功能异常")

    engine.wait(30, tips="设备升级完成，校验版本")

    config['检测版本号和参数保持不变'](version=config["设备描述信息设备制造商0003"])


def test_载波适配层升级测试():
    """
    06_载波适配层升级测试
    1、首先进行载波适配层版本验证和参数验证
    2、升级至上一发布版载波适配层程序：ESMD-AD63(v2.2)-20170826升级至ESMD-AD63(v2.1)-20170210
    3、升级成功后再次载波适配层版本验证和参数验证，版本号变更，其余的参数不变
    4、再次升级回最新发布版本版载波适配层：ESMD-AD63(v2.1)-20170210升级至ESMD-AD63(v2.2)-20170826
    5、升级成功后再次载波适配层版本验证和参数验证，版本号变更，其余的参数不变
    """
    # 升级前查看版本和配置信息
    config['检测版本号和参数保持不变'](adaptor=config["适配层版本号0606"])
    engine.update(config['载波适配层上一版本'])
    engine.wait(30)
    # 升级后查看版本和配置信息
    config['检测版本号和参数保持不变'](adaptor=config['载波适配层上一版本'])
    engine.update(config["适配层版本号0606"])
    engine.wait(30)
    # 升级后再次查看版本和配置信息
    config['检测版本号和参数保持不变'](adaptor=config["适配层版本号0606"])


def test_载波网络层升级测试():
    """
    07_载波网络层升级测试
    1、首先进行载波网络层版本验证和参数验证
    2、升级至上一发布版载波网络层程序：SSC1663-PLC(v1.0)-20171011升级至SSC1663-PLC(v1.0)-20170510
    3、升级成功后再次载波网络层版本验证和参数验证，版本号变更，其余的参数不变
    4、再次升级回最新发布版本版载波网络层：SSC1663-PLC(v1.0)-20170510升级至SSC1663-PLC(v1.0)-20171011
    5、升级成功后再次载波网络层版本验证和参数验证，版本号变更，其余的参数不变
    """
    # 升级前查看版本和配置信息
    config['检测版本号和参数保持不变'](network=config["网络层版本号060A"])
    engine.update(config['载波网络层上一版本'])
    engine.wait(30)
    # 升级后查看版本和配置信息
    config['检测版本号和参数保持不变'](network=config['载波网络层上一版本'])
    engine.update(config["网络层版本号060A"])
    engine.wait(30)
    # 升级后再次查看版本和配置信息
    config['检测版本号和参数保持不变'](network=config["网络层版本号060A"])
