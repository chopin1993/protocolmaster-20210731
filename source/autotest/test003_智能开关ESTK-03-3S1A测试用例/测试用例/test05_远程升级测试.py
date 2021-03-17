# encoding:utf-8
# 导入测试引擎
from autotest.公共用例.public05远程升级测试 import *
from .常用测试模块 import *

测试组说明 = "远程升级测试"

config = engine.get_config()
config["应用程序上一版发布版本"] = "ESTK-03-3S1A(v1.3)-20191205"  # 如果此处为空字符串时，表示不支持兼容性升级或手动测试。
config["应用程序同版本号测试版本"] = "ESTK-03-R-3S1A(v2.0)-20210310"
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

    engine.send_did("READ", "继电器上电状态C060")
    engine.expect_did("READ", "继电器上电状态C060", "00")
    engine.send_did("READ", "继电器过零点动作延迟时间C020", "07")
    engine.expect_did("READ", "继电器过零点动作延迟时间C020", "07 20 20 20 21 20 22")
    engine.send_did("READ", "读写面板默认背光亮度百分比C135", "07")
    engine.expect_did("READ", "读写面板默认背光亮度百分比C135", '07 32 32 32')

    engine.send_did("READ", "主动上报使能标志D005")
    engine.expect_did("READ", "主动上报使能标志D005", "00 01")
    engine.send_did("READ", "读取或设置被控设备端的控制地址FB20", 设备通道=1)
    engine.expect_did("READ", "读取或设置被控设备端的控制地址FB20",
                      设备通道=1, 被控设备AID=config["测试设备地址"], 被控设备通道='01')
    engine.add_doc_info('因为通道2配置了情景模式，FC29查询，所以采用模拟点击的方式，测试通道2的配置信息正常')
    engine.set_device_sensor_status("按键输入", "短按", 1)
    engine.broadcast_expect_multi_dids('WRITE',
                                       [73], 'U8', '单轨窗帘目标开度0A03', '64',
                                       [2, 5, 6, 12], 'BIT1', '开关机E013', '01',
                                       [75], 'U8', '通断操作C012', '02')
    engine.send_did("READ", "读取或设置被控设备端的控制地址FB20", 设备通道=3)
    engine.expect_did("READ", "读取或设置被控设备端的控制地址FB20",
                      设备通道=3, 被控设备AID=0, 被控设备通道='01')


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
    report_gateway_expect(wait_times=[15], ack=True, wait_enable=False)

    engine.add_doc_info('通过抄控器设置被测设备的参数，使之与默认参数不一致，验证升级前后参数是否会发生变化')
    engine.send_did("WRITE", "继电器上电状态C060", "00")
    engine.expect_did("WRITE", "继电器上电状态C060", "00")
    engine.send_did("WRITE", "继电器过零点动作延迟时间C020", "07 20 20 20 21 20 22")
    engine.expect_did("WRITE", "继电器过零点动作延迟时间C020", "07 20 20 20 21 20 22")
    engine.send_did("WRITE", "读写面板默认背光亮度百分比C135", '07 32 32 32')
    engine.expect_did("WRITE", "读写面板默认背光亮度百分比C135", '07 32 32 32')

    engine.send_did("WRITE", "主动上报使能标志D005", 传感器类型="未知", 上报命令="上报网关")
    engine.expect_did("WRITE", "主动上报使能标志D005", 传感器类型="未知", 上报命令="上报网关")
    engine.add_doc_info('触摸开关的3个按键，分别配置为1按键保持不变、2按键配置为情景模式报文、3按键配置为上报模式')

    engine.send_did("WRITE", "情景模式帧体FC29",
                    '01 02 13 41 49 03 0A 01 64 02 32 08 13 E0 01 01 41 4B 12 C0 01 02')
    engine.expect_did("WRITE", "情景模式帧体FC29",
                      '01 02 13 41 49 03 0A 01 64 02 32 08 13 E0 01 01 41 4B 12 C0 01 02')
    engine.send_did("WRITE", "读取或设置被控设备端的控制地址FB20",
                    设备通道=3, 被控设备AID=0, 被控设备通道='01')
    engine.expect_did("WRITE", "读取或设置被控设备端的控制地址FB20",
                      设备通道=3, 被控设备AID=0, 被控设备通道='01')

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
    3、升级成功后再次应用程序版本验证和参数验证，版本号变更，不再支持过零检测参数C020
    4、再次升级回最新发布版本版应用程序：
    5、升级成功后再次应用程序版本验证和参数验证，版本号变更，其余的参数不变
    """

    engine.add_doc_info("升级前，查询版本及SN、DK、配置参数")
    check_update_configure(version=config["设备描述信息设备制造商0003"])

    engine.update(config["应用程序上一版发布版本"])
    engine.wait(config["升级后等待重启时间"], tips="设备升级完成，校验版本")
    engine.add_doc_info("升级后，查询版本及SN、DK、配置参数")
    engine.add_doc_info('上一版本发布版本不支持过零检测功能，所以查询CO20时，回复82 04 00')

    engine.send_did("READ", "设备描述信息设备制造商0003")
    engine.expect_did("READ", "设备描述信息设备制造商0003", config["应用程序上一版发布版本"])
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
                             "设备描述信息设备制造商0003", config["应用程序上一版发布版本"],
                             "DKEY0005", config["DKEY0005"],
                             "SN0007", config["SN0007"])

    engine.send_did("READ", "继电器上电状态C060")
    engine.expect_did("READ", "继电器上电状态C060", "00")
    engine.send_did("READ", "继电器过零点动作延迟时间C020", "07")
    engine.expect_did("READ", "继电器过零点动作延迟时间C020", "04 00") # 上一发布版本不支持C020
    engine.send_did("READ", "读写面板默认背光亮度百分比C135", "07")
    engine.expect_did("READ", "读写面板默认背光亮度百分比C135", '07 32 32 32')

    engine.send_did("READ", "主动上报使能标志D005")
    engine.expect_did("READ", "主动上报使能标志D005", "00 01")
    engine.send_did("READ", "读取或设置被控设备端的控制地址FB20", 设备通道=1)
    engine.expect_did("READ", "读取或设置被控设备端的控制地址FB20",
                      设备通道=1, 被控设备AID=config["测试设备地址"], 被控设备通道='01')
    engine.add_doc_info('因为通道2配置了情景模式，FC29查询，所以采用模拟点击的方式，测试通道2的配置信息正常:'
                        '因为ESTK-03-3S1A(v1.3)-20191205不支持SWB协议，所以无法进行模拟点击，通道2本次不验证')
    # engine.set_device_sensor_status("按键输入", "短按", 1)
    # engine.broadcast_expect_multi_dids('WRITE',
    #                                    [73], 'U8', '单轨窗帘目标开度0A03', '64',
    #                                    [2, 5, 6, 12], 'BIT1', '开关机E013', '01',
    #                                    [75], 'U8', '通断操作C012', '02')
    engine.send_did("READ", "读取或设置被控设备端的控制地址FB20", 设备通道=3)
    engine.expect_did("READ", "读取或设置被控设备端的控制地址FB20",
                      设备通道=3, 被控设备AID=0, 被控设备通道='01')

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
    engine.add_doc_info('升级测试结束后发送CD00清除参数，使被测设备恢复出厂参数')

    engine.send_did("WRITE", "复位等待时间CD00", "00")
    engine.expect_did("WRITE", "复位等待时间CD00", "00")

    engine.add_doc_info('将CD00不能恢复的参数，设置回默认参数，便于后续的测试项目运行')

    engine.send_did("WRITE", "继电器上电状态C060", "02")
    engine.expect_did("WRITE", "继电器上电状态C060", "02")
    engine.send_did("WRITE", "继电器过零点动作延迟时间C020", "07 33 39 33 39 33 39")
    engine.expect_did("WRITE", "继电器过零点动作延迟时间C020", "07 33 39 33 39 33 39")
    engine.send_did("WRITE", "读写面板默认背光亮度百分比C135", '07 01 01 01')
    engine.expect_did("WRITE", "读写面板默认背光亮度百分比C135", '07 01 01 01')
