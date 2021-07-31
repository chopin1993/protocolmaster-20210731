# encoding:utf-8
import engine
from autotest.公共用例.public常用测试模块 import *
from .常用测试模块 import *

测试组说明 = "功能类报文测试"
# 判断按键数量
if config["被测设备按键数"] == 4:
    channel_dict = {1: '01', 2: '02', 3: '04', 4: '08'}  # 设备通道及对应值
elif config["被测设备按键数"] == 3:
    channel_dict = {1: '01', 2: '02', 3: '04'}
elif config["被测设备按键数"] == 2:
    channel_dict = {1: '01', 2: '02'}
else:   # config["被测设备按键数"] == 1
    channel_dict = {1: '01'}


def rcv_data_no_check(data):
    return True


def test_出厂默认参数():
    """
    01_默认出厂参数测试
    1、出厂第一次继电器默认为断开00 通断操作C012
    2、断电后默认上电状态为02上电状态为上次断电状态 继电器上电状态C060
    3、继电器过零保护出厂为3路，可分别设置，默认断开延时5.1ms，默认闭合延时5.7ms 07 33 39 33 39 33 39 继电器过零点动作延迟时间C020，可控硅版本无此参数信息
    4、状态同步默认状态03同时上报设备和网关 主动上报使能标志D005
    5、触摸开关默认控制的设备AID为自身的AID 读取或设置被控设备端的控制地址FB20
    6、面板的默认背光亮度为1% 读写面板默认背光亮度百分比C135
    7、继电器版继电器动作次数读取；
    """
    if config["被测设备类型"] == "开关":
        engine.send_did("READ", "通断操作C012", "")
        engine.expect_did("READ", "通断操作C012", "00")

        engine.send_did("READ", "继电器上电状态C060")
        engine.expect_did("READ", "继电器上电状态C060", "02")

        engine.send_did("READ", "主动上报使能标志D005")
        engine.expect_did("READ", "主动上报使能标志D005", "00 03")
    else:
        engine.add_doc_info('检测到此设备是触摸面板，不测试此项！！！')

    if config["被测设备硬件版本"] == "继电器版本":
        if config["被测设备按键数"] == 1:
            engine.send_did("READ", "继电器过零点动作延迟时间C020", "01")
            engine.expect_did("READ", "继电器过零点动作延迟时间C020", "01 33 39")
        else:   # config["被测设备按键数"] == 2:
            engine.send_did("READ", "继电器过零点动作延迟时间C020", "01")
            engine.expect_did("READ", "继电器过零点动作延迟时间C020", "01 33 39")
            engine.send_did("READ", "继电器过零点动作延迟时间C020", "02")
            engine.expect_did("READ", "继电器过零点动作延迟时间C020", "02 33 39")
    else:
        engine.send_did("READ", "继电器过零点动作延迟时间C020", "07")
        engine.expect_did("READ", "继电器过零点动作延迟时间C020", "04 00")

    for channel, value in channel_dict.items():
        engine.send_did("READ", "读取或设置被控设备端的控制地址FB20", 设备通道=channel)
        engine.expect_did("READ", "读取或设置被控设备端的控制地址FB20",
                          设备通道=channel, 被控设备AID=config["测试设备地址"], 被控设备通道=value)
    if config["被测设备按键数"] == 3:
        engine.send_did("READ", "读写面板默认背光亮度百分比C135", "07")
        engine.expect_did("READ", "读写面板默认背光亮度百分比C135", '07 01 01 01')
    elif config["被测设备按键数"] == 2:
        engine.send_did("READ", "读写面板默认背光亮度百分比C135", "03")
        engine.expect_did("READ", "读写面板默认背光亮度百分比C135", '03 01 01')
    else:   # config["被测设备按键数"] == 1
        engine.send_did("READ", "读写面板默认背光亮度百分比C135", "01")
        engine.expect_did("READ", "读写面板默认背光亮度百分比C135", '01 01')

    if config["被测设备硬件版本"] == "继电器版本":
        engine.send_did("READ", "读取继电器操作次数C132", "07")
        engine.expect_did("READ", "读取继电器操作次数C132", rcv_data_no_check)
    elif config["被测设备硬件版本"] == "开关":
        pass
    else:
        engine.send_did("READ", "读取继电器操作次数C132", "03")
        engine.expect_did("READ", "读取继电器操作次数C132", "** ** ** ** **")


def test_读取或设置被控设备端的控制地址FB20():
    """
    06_读取或设置被控设备端的控制地址FB20
    1、查询默认配置，为自身的AID；
    2、配置其他的设备AID，并进行查询验证，通过SWB接口协议，模拟人工点击验证配置信息；
    3、配置回默认参数，并进行查询验证；
    """
    engine.add_doc_info("1、查询默认配置，为自身的AID")
    for channel, value in channel_dict.items():
        engine.send_did("READ", "读取或设置被控设备端的控制地址FB20", 设备通道=channel)
        engine.expect_did("READ", "读取或设置被控设备端的控制地址FB20",
                          设备通道=channel, 被控设备AID=config["测试设备地址"], 被控设备通道=value)

    engine.add_doc_info("2、配置其他的设备AID，并进行查询验证")
    for channel, value in channel_dict.items():
        engine.add_doc_info('测试通道{}配置其他设备AID'.format(channel))

        engine.send_did("WRITE", "读取或设置被控设备端的控制地址FB20",
                        设备通道=channel, 被控设备AID=config["抄控器默认源地址"], 被控设备通道=value)
        engine.expect_did("WRITE", "读取或设置被控设备端的控制地址FB20",
                          设备通道=channel, 被控设备AID=config["抄控器默认源地址"], 被控设备通道=value)
        engine.send_did("READ", "读取或设置被控设备端的控制地址FB20", 设备通道=channel)
        engine.expect_did("READ", "读取或设置被控设备端的控制地址FB20",
                          设备通道=channel, 被控设备AID=config["抄控器默认源地址"], 被控设备通道=value)

        engine.add_doc_info('模拟点击控制其他设备闭合和断开，进行相关的测试')
        engine.set_device_sensor_status("按键输入", "短按", channel=(channel - 1))
        engine.expect_did('WRITE', '继电器翻转C018', value, check_seq=False)
        engine.send_did('WRITE', '通断操作C012', value, reply=True)
        engine.wait(1)
        engine.set_device_sensor_status("按键输入", "短按", channel=(channel - 1))
        engine.expect_did('WRITE', '继电器翻转C018', value, check_seq=False)
        engine.send_did('WRITE', '通断操作C012', '00', reply=True)
        engine.wait(1)

    engine.add_doc_info("3、配置回默认参数，并进行查询验证")
    for channel, value in channel_dict.items():
        engine.add_doc_info('测试通道{}配置回默认参数，并进行查询验证'.format(channel))
        engine.send_did("WRITE", "读取或设置被控设备端的控制地址FB20",
                        设备通道=channel, 被控设备AID=config["测试设备地址"], 被控设备通道=value)
        engine.expect_did("WRITE", "读取或设置被控设备端的控制地址FB20",
                          设备通道=channel, 被控设备AID=config["测试设备地址"], 被控设备通道=value)
        engine.send_did("READ", "读取或设置被控设备端的控制地址FB20", 设备通道=channel)
        engine.expect_did("READ", "读取或设置被控设备端的控制地址FB20",
                          设备通道=channel, 被控设备AID=config["测试设备地址"], 被控设备通道=value)


def test_读写面板默认背光亮度百分比C135():
    """
    07_读写面板默认背光亮度百分比C135
    1、查询默认的背光亮度百分比为1%
    2、设置背光亮度百分比为其他数值，如1%-50%可以正常配置，0，及大于50%不能设置成功
    3、设置背光亮度百分比回默认1%，并进行验证
    """
    engine.add_doc_info("""测试说明：
    触摸类设备的背光以设备区分，不以通道区分，按照协议发送可只发送一路的配置即可，当发送多路时以最后一个通道的配置为准。亮度值范围为1-50，设置数据值和百分比关系如下：
        1：中国风背光亮度，百分比为1/4000 = 0.00025
        2-50：其它面板背光，百分比为 (2-50)*2 /4000 = 0.001-0.025(千分之一至千分之二十五，步长为千分之0.5调节)
        >50：错误配置""")
    engine.add_doc_info("1、查询默认的背光亮度百分比为1%")

    if config["被测设备按键数"] == 2:
        engine.send_did("READ", "读写面板默认背光亮度百分比C135", "03")
        engine.expect_did("READ", "读写面板默认背光亮度百分比C135", '03 01 01')
    else:   # config["被测设备按键数"] == 1
        engine.send_did("READ", "读写面板默认背光亮度百分比C135", "01")
        engine.expect_did("READ", "读写面板默认背光亮度百分比C135", '01 01')

    engine.add_doc_info("2、设置背光亮度百分比为其他数值")
    for channel, value in channel_dict.items():
        engine.add_doc_info('测试通道{}设置不同的背光亮度百分比'.format(channel))
        for i in [10, 32, 50]:
            engine.send_did("WRITE", "读写面板默认背光亮度百分比C135", 设备通道=value, 背光亮度=i)
            engine.expect_did("WRITE", "读写面板默认背光亮度百分比C135", 设备通道=value, 背光亮度=i)
            engine.send_did("READ", "读写面板默认背光亮度百分比C135", 设备通道=value)
            engine.expect_did("READ", "读写面板默认背光亮度百分比C135", 设备通道=value, 背光亮度=i)

        engine.add_doc_info('设置不支持的背光百分比范围，均回复0003格式不正确')
        for i in [0, 51, 200]:
            engine.send_did("WRITE", "读写面板默认背光亮度百分比C135", 设备通道=value, 背光亮度=i)
            engine.expect_did("WRITE", "读写面板默认背光亮度百分比C135", '03 00')

        engine.add_doc_info('设置不支持的背光百分比范围不成功，背光百分比仍是之前设置成功的参数')
        engine.send_did("READ", "读写面板默认背光亮度百分比C135", 设备通道=value)
        engine.expect_did("READ", "读写面板默认背光亮度百分比C135", 设备通道=value, 背光亮度=50)

    engine.add_doc_info("3、设置背光亮度百分比回默认1%，并进行验证")
    if config["被测设备按键数"] == 4:
        engine.send_did("WRITE", "读写面板默认背光亮度百分比C135", '0f 01 01 01 01')
        engine.expect_did("WRITE", "读写面板默认背光亮度百分比C135", '0f 01 01 01 01')
        engine.send_did("READ", "读写面板默认背光亮度百分比C135", "0f")
        engine.expect_did("READ", "读写面板默认背光亮度百分比C135", '0f 01 01 01 01')
    elif config["被测设备按键数"] == 3:
        engine.send_did("WRITE", "读写面板默认背光亮度百分比C135", '07 01 01 01')
        engine.expect_did("WRITE", "读写面板默认背光亮度百分比C135", '07 01 01 01')
        engine.send_did("READ", "读写面板默认背光亮度百分比C135", "07")
        engine.expect_did("READ", "读写面板默认背光亮度百分比C135", '07 01 01 01')
    elif config["被测设备按键数"] == 2:
        engine.send_did("WRITE", "读写面板默认背光亮度百分比C135", '01 01')
        engine.expect_did("WRITE", "读写面板默认背光亮度百分比C135", '01 01')
        engine.send_did("READ", "读写面板默认背光亮度百分比C135", "01")
        engine.expect_did("READ", "读写面板默认背光亮度百分比C135", '01 01')

        engine.send_did("WRITE", "读写面板默认背光亮度百分比C135", '02 01')
        engine.expect_did("WRITE", "读写面板默认背光亮度百分比C135", '02 01')
        engine.send_did("READ", "读写面板默认背光亮度百分比C135", "02")
        engine.expect_did("READ", "读写面板默认背光亮度百分比C135", '02 01')
    else:
        engine.send_did("WRITE", "读写面板默认背光亮度百分比C135", '01 01')
        engine.expect_did("WRITE", "读写面板默认背光亮度百分比C135", '01 01')
        engine.send_did("READ", "读写面板默认背光亮度百分比C135", "01")
        engine.expect_did("READ", "读写面板默认背光亮度百分比C135", '01 01')


def test_通断操作C012():
    """
    02_通断操作C012
    1、关闭所有通道；
    2、查询当前通断状态00；
    3、打开通道，然后查询当前通断状态，监测器输出监测正常；
    4、关闭通道，然后查询当前通断状态，监测器输出监测正常；
    """
    if config["被测设备类型"] == "面板":
        engine.add_doc_info('此设备为面板类设备而非开关，不测试此项目！')
        return
    engine.send_did("WRITE", "通断操作C012", "07")
    engine.expect_did("WRITE", "通断操作C012", "00")

    engine.send_did("READ", "通断操作C012", "")
    engine.expect_did("READ", "通断操作C012", "00")

    engine.add_doc_info("通道1控制通断测试")
    relay_output_test(did="通断操作C012", relay_channel=1, output_channel=[0])
    if config["被测设备按键数"] == 2:
        engine.add_doc_info("通道2控制通断测试")
        relay_output_test(did="通断操作C012", relay_channel=2, output_channel=[1])
        engine.add_doc_info("2个通道同时控制通断测试")
        relay_output_test(did="通断操作C012", relay_channel=3, output_channel=[0, 1])

    if config["被测设备按键数"] == 3:
        engine.add_doc_info("通道3控制通断测试")
        relay_output_test(did="通断操作C012", relay_channel=4, output_channel=[2])

        engine.add_doc_info("3个通道同时控制通断测试")
        relay_output_test(did="通断操作C012", relay_channel=7, output_channel=[0, 1, 2])


def test_继电器翻转C018():
    """
    03_继电器翻转C018
    bit5~bit0:1/0表示通道操作/不操作；bit0表示第1个通道，回复时按C012报文格式回复
    1、查询当前通断状态00关闭
    2、继电器翻转，然后查询当前通断状态，监测器输出监测正常；
    3、继电器翻转，然后查询当前通断状态，监测器输出监测正常；
    """
    if config["被测设备类型"] == "面板":
        engine.add_doc_info('此设备为面板类设备而非开关，不测试此项目！')
        return
    engine.send_did("READ", "通断操作C012", "")
    engine.expect_did("READ", "通断操作C012", "00")

    engine.add_doc_info('通道1控制翻转测试')
    relay_output_test(did="继电器翻转C018", relay_channel=1, output_channel=[0])
    if config["被测设备按键数"] == 2:
        engine.add_doc_info('通道2控制翻转测试')
        relay_output_test(did="继电器翻转C018", relay_channel=2, output_channel=[1])
        engine.add_doc_info('2个通道同时控制翻转测试')
        relay_output_test(did="继电器翻转C018", relay_channel=3, output_channel=[0, 1])
    if config["被测设备按键数"] == 3:
        engine.add_doc_info('通道3控制翻转测试')
        relay_output_test(did="继电器翻转C018", relay_channel=4, output_channel=[2])
        engine.add_doc_info('3个通道同时控制翻转测试')
        relay_output_test(did="继电器翻转C018", relay_channel=7, output_channel=[0, 1, 2])


def test_继电器上电状态C060():
    """
    04_继电器上电状态C060
    0x00表示上电断开，0x01表示上电闭合，0x02表示上电状态为上次断电状态
    1、查询断电后默认上电状态为02上电状态为上次断电状态
    2、设置断电后上电状态为00上电状态为上电断开，然后进行查询确定
    3、设置断电后上电状态为01上电状态为上电闭合，然后进行查询确定
    4、设置断电后上电状态为02上电状态为上次断电状态，然后进行查询确定
    5、设置回默认上电状态为02上电状态为上次断电状态
    """
    if config["被测设备类型"] == "面板":
        engine.add_doc_info('此设备为面板类设备而非开关，不测试此项目！')
        return
    # 02上电状态为上次断电状态
    engine.send_did("READ", "继电器上电状态C060", "")
    engine.expect_did("READ", "继电器上电状态C060", "02")

    engine.add_doc_info("测试被测设备为开的时候断电，根据配置，断电重启后为开")
    engine.send_did("WRITE", "通断操作C012", "83")
    engine.expect_did("WRITE", "通断操作C012", "03")
    power_control()
    engine.send_did("READ", "通断操作C012", "")
    engine.expect_did("READ", "通断操作C012", "03")
    
    engine.add_doc_info('监测器检测被测设备的输出端')
    for channel in [0, 1]:
        engine.expect_cross_zero_status(channel, 1)

    engine.add_doc_info("测试被测设备为关的时候断电，根据配置，断电重启后为关")
    engine.send_did("WRITE", "通断操作C012", "03")
    engine.expect_did("WRITE", "通断操作C012", "00")
    power_control()
    engine.send_did("READ", "通断操作C012", "")
    engine.expect_did("READ", "通断操作C012", "00")
    engine.add_doc_info('监测器检测被测设备的输出端')
    for channel in [0, 1]:
        engine.expect_cross_zero_status(channel, 0)

    # 00上电状态为上电断开
    engine.add_doc_info("测试上电状态为上电断开，通过前置的工装通断电，给被测设备通断电")
    engine.send_did("WRITE", "继电器上电状态C060", "00")
    engine.expect_did("WRITE", "继电器上电状态C060", "00")
    engine.send_did("READ", "继电器上电状态C060", "")
    engine.expect_did("READ", "继电器上电状态C060", "00")

    engine.add_doc_info("测试被测设备为开的时候断电，根据配置，断电重启后为关")
    engine.send_did("WRITE", "通断操作C012", "83")
    engine.expect_did("WRITE", "通断操作C012", "03")
    power_control()
    engine.send_did("READ", "通断操作C012", "")
    engine.expect_did("READ", "通断操作C012", "00")
    engine.add_doc_info('监测器检测被测设备的输出端')
    for channel in [0, 1]:
        engine.expect_cross_zero_status(channel, 0)

    engine.add_doc_info("测试被测设备为关的时候断电，根据配置，断电重启后为关")
    engine.send_did("WRITE", "通断操作C012", "03")
    engine.expect_did("WRITE", "通断操作C012", "00")
    power_control()
    engine.send_did("READ", "通断操作C012", "")
    engine.expect_did("READ", "通断操作C012", "00")
    engine.add_doc_info('监测器检测被测设备的输出端')
    for channel in [0, 1]:
        engine.expect_cross_zero_status(channel, 0)

    # 01上电状态为上电闭合
    engine.add_doc_info("测试上电状态为上电闭合，通过前置的工装通断电，给被测设备通断电")
    engine.send_did("WRITE", "继电器上电状态C060", "01")
    engine.expect_did("WRITE", "继电器上电状态C060", "01")
    engine.send_did("READ", "继电器上电状态C060")
    engine.expect_did("READ", "继电器上电状态C060", "01")

    engine.add_doc_info("测试被测设备为开的时候断电，根据配置，断电重启后为开")
    engine.send_did("WRITE", "通断操作C012", "83")
    engine.expect_did("WRITE", "通断操作C012", "03")
    power_control()
    engine.send_did("READ", "通断操作C012", "")
    engine.expect_did("READ", "通断操作C012", "03")
    engine.add_doc_info('监测器检测被测设备的输出端')
    for channel in [0, 1]:
        engine.expect_cross_zero_status(channel, 1)

    engine.add_doc_info("测试被测设备为关的时候断电，根据配置，断电重启后为开")
    engine.send_did("WRITE", "通断操作C012", "03")
    engine.expect_did("WRITE", "通断操作C012", "00")
    power_control()
    engine.send_did("READ", "通断操作C012", "")
    engine.expect_did("READ", "通断操作C012", "03")
    engine.add_doc_info('监测器检测被测设备的输出端')
    for channel in [0, 1]:
        engine.expect_cross_zero_status(channel, 1)

    engine.add_doc_info('设置回默认参数，02上电状态为上次断电状态')
    engine.send_did("WRITE", "继电器上电状态C060", "02")
    engine.expect_did("WRITE", "继电器上电状态C060", "02")
    engine.send_did("READ", "继电器上电状态C060")
    engine.expect_did("READ", "继电器上电状态C060", "02")
    engine.send_did("WRITE", "通断操作C012", "03")
    engine.expect_did("WRITE", "通断操作C012", "00")


def test_主动上报使能标志D005():
    """
    05_主动上报使能标志D005
    TT为传感器类型，XX 为0x00:无上报；0x01：上报网关；0x02：上报设备；0x03同时上报设备和网关（状态同步的普遍使用方案）；
    1、查询被测设备的默认状态同步使能参数为03
    2、设置主动上报使能标志D005为00：无上报，并进行查询验证
    3、设置主动上报使能标志D005为01：上报网关，并进行查询验证
    4、设置主动上报使能标志D005为02：上报设备，并进行查询验证
    5、设置主动上报使能标志D005为03：同时上报设备和网关，并进行查询验证
    """
    if config["被测设备类型"] == "面板":
        engine.add_doc_info('此设备为面板类设备而非开关，不测试此项目！')
        return
    engine.add_doc_info("1、查询被测设备的默认状态同步使能参数为03")
    engine.send_did("READ", "主动上报使能标志D005", "")
    engine.expect_did("READ", "主动上报使能标志D005", 传感器类型="未知", 上报命令="同时上报设备和网关")

    engine.add_doc_info('2、设置为无上报模式并进行查询验证')
    engine.send_did("WRITE", "主动上报使能标志D005", 传感器类型="未知", 上报命令="无上报")
    engine.expect_did("WRITE", "主动上报使能标志D005", 传感器类型="未知", 上报命令="无上报")
    engine.send_did("READ", "主动上报使能标志D005")
    engine.expect_did("READ", "主动上报使能标志D005", 传感器类型="未知", 上报命令="无上报")

    engine.add_doc_info('3、设置为上报网关模式并进行查询验证')
    engine.send_did("WRITE", "主动上报使能标志D005", 传感器类型="未知", 上报命令="上报网关")
    engine.expect_did("WRITE", "主动上报使能标志D005", 传感器类型="未知", 上报命令="上报网关")
    engine.send_did("READ", "主动上报使能标志D005")
    engine.expect_did("READ", "主动上报使能标志D005", 传感器类型="未知", 上报命令="上报网关")

    engine.add_doc_info('4、设置为上报设备模式并进行查询验证')
    engine.send_did("WRITE", "主动上报使能标志D005", 传感器类型="未知", 上报命令="上报设备")
    engine.expect_did("WRITE", "主动上报使能标志D005", 传感器类型="未知", 上报命令="上报设备")
    engine.send_did("READ", "主动上报使能标志D005")
    engine.expect_did("READ", "主动上报使能标志D005", 传感器类型="未知", 上报命令="上报设备")

    engine.add_doc_info('5、设置为同时上报设备和网关模式并进行查询验证')
    engine.send_did("WRITE", "主动上报使能标志D005", 传感器类型="未知", 上报命令="同时上报设备和网关")
    engine.expect_did("WRITE", "主动上报使能标志D005", 传感器类型="未知", 上报命令="同时上报设备和网关")
    engine.send_did("READ", "主动上报使能标志D005")
    engine.expect_did("READ", "主动上报使能标志D005", 传感器类型="未知", 上报命令="同时上报设备和网关")


def test_继电器过零点动作延迟时间C020():
    """
    08_继电器过零点动作延迟时间C020
    xx(通道)xx（继电器断开延迟时间ms）xx（继电器闭合延迟时间），可控硅硬件无此项测试
    1、查询被测设备的默认参数
    2、分别设置每路不同的过零点动作时间为01 00 00、02 00 01、04 00 02，并进行查询验证
    3、同时设置3路通道不同的过零点动作时间为07 20 20 20 21 20 22、，并进行查询验证
    4、设置回默认过零点动作时间为07 33 39 33 39 33 39，并进行查询验证
    """
    if config["被测设备类型"] == "面板":
        engine.add_doc_info('此设备为面板类设备而非开关，不测试此项目！')
        return
    if config["被测设备硬件版本"] == "继电器版本":
        engine.add_doc_info("1、查询默认的继电器过零点动作延迟时间C020，01 33 39")
        for channel, value in channel_dict.items():
            engine.send_did("READ", "继电器过零点动作延迟时间C020", value)
            engine.expect_did("READ", "继电器过零点动作延迟时间C020", value + " 33 39")

        engine.add_doc_info("2、测试设置不同的继电器过零点动作延迟时间C020，要求均可以设置成功")
        if config["被测设备按键数"] == 2:
            for value in ["01 00 00", "02 00 01"]:
                engine.send_did("WRITE", "继电器过零点动作延迟时间C020", value)
                engine.expect_did("WRITE", "继电器过零点动作延迟时间C020", value)
        else:   # config["被测设备按键数"] == 1
            for value in ["01 00 00"]:
                engine.send_did("WRITE", "继电器过零点动作延迟时间C020", value)
                engine.expect_did("WRITE", "继电器过零点动作延迟时间C020", value)
        if config["被测设备按键数"] == 2:
            engine.send_did("READ", "继电器过零点动作延迟时间C020", "01")
            engine.expect_did("READ", "继电器过零点动作延迟时间C020", "01 00 00")
            engine.send_did("READ", "继电器过零点动作延迟时间C020", "02")
            engine.expect_did("READ", "继电器过零点动作延迟时间C020", "02 00 01")
        else:   # config["被测设备按键数"] == 1
            engine.send_did("READ", "继电器过零点动作延迟时间C020", "01")
            engine.expect_did("READ", "继电器过零点动作延迟时间C020", "01 00 00")

        engine.add_doc_info("3、测试设置不同的继电器过零点动作延迟时间C020，要求均可以设置成功")
        # 读写第一通道
        engine.send_did("WRITE", "继电器过零点动作延迟时间C020", "01 20 20")
        engine.expect_did("WRITE", "继电器过零点动作延迟时间C020", "01 20 20")
        engine.send_did("READ", "继电器过零点动作延迟时间C020", "01")
        engine.expect_did("READ", "继电器过零点动作延迟时间C020", "01 20 20")
        if config["被测设备按键数"] == 2:
            engine.send_did("WRITE", "继电器过零点动作延迟时间C020", "02 20 20")
            engine.expect_did("WRITE", "继电器过零点动作延迟时间C020", "02 20 20")
            engine.send_did("READ", "继电器过零点动作延迟时间C020", "02")
            engine.expect_did("READ", "继电器过零点动作延迟时间C020", "02 20 20")
        else:   # config["被测设备按键数"] == 1
            engine.send_did("WRITE", "继电器过零点动作延迟时间C020", "01 20 20")
            engine.expect_did("WRITE", "继电器过零点动作延迟时间C020", "01 20 20")
            engine.send_did("READ", "继电器过零点动作延迟时间C020", "01")
            engine.expect_did("READ", "继电器过零点动作延迟时间C020", "01 20 20")

        engine.add_doc_info("4、为便于后续的测试，将参数设置回默认参数")
        # 读写第一通道
        engine.send_did("WRITE", "继电器过零点动作延迟时间C020", "01 33 39")
        engine.expect_did("WRITE", "继电器过零点动作延迟时间C020", "01 33 39")
        engine.send_did("READ", "继电器过零点动作延迟时间C020", "01")
        engine.expect_did("READ", "继电器过零点动作延迟时间C020", "01 33 39")
        if config["被测设备按键数"] == 2:
            engine.send_did("WRITE", "继电器过零点动作延迟时间C020", "02 33 39")
            engine.expect_did("WRITE", "继电器过零点动作延迟时间C020", "02 33 39")
            engine.send_did("READ", "继电器过零点动作延迟时间C020", "02")
            engine.expect_did("READ", "继电器过零点动作延迟时间C020", "02 33 39")
    else:
        engine.send_did("READ", "继电器过零点动作延迟时间C020", "07")
        engine.expect_did("READ", "继电器过零点动作延迟时间C020", "82 04 00")
        engine.add_doc_info("可控硅硬件无此项测试")


def test_继电器动作次数C132():
    """
    09_继电器动作次数C132
    xx(通道)xx（继电器动作次数），可控硅硬件无此项测试
    1、查询被测设备的现有动作次数
    2、分别设置每路进行动作，并进行动作次数查询验证
    3、同时设置3路通道动作，并进行动作次数查询验证
    4、设备断电自动动作一次，读取动作次数查询验证
    """
    if config["被测设备类型"] == "面板":
        engine.add_doc_info('此设备为面板类设备而非开关，不测试此项目！')
        return
    if config["被测设备硬件版本"] == "继电器版本":

        engine.send_did("WRITE", "通断操作C012", "07")
        engine.expect_did("WRITE", "通断操作C012", "00")
        engine.wait(seconds=2, tips='保证动作完成')

        opt_time = [0, 0, 0]

        def get_ret_opt_time(data):
            if len(data) != 3:
                return False
            else:
                time = int(data[1]) * 256 + int(data[2])
                if 1 == data[0]:
                    opt_time[0] = time
                if 2 == data[0]:
                    opt_time[1] = time
                if 4 == data[0]:
                    opt_time[2] = time
                return True

        engine.add_doc_info("1、查询当前继电器动作次数C132，07")
        for channel, value in channel_dict.items():
            engine.send_did("READ", "读取继电器操作次数C132", value)
            engine.expect_did("READ", "读取继电器操作次数C132", get_ret_opt_time)

        engine.add_doc_info("2、每次动作不同的继电器，测试动作次数增加")
        for channel, value in channel_dict.items():
            engine.send_did("WRITE", "继电器翻转C018", value)
            engine.expect_did("WRITE", "通断操作C012", value)
            engine.wait(seconds=2, tips='保证动作完成')
            engine.send_did("READ", "读取继电器操作次数C132", value)
            cnt = opt_time[channel - 1] + 1
            expect = value + " " + str(hex(int(cnt / 256))[2:]).rjust(2, "0") + " " + str(
                hex(int(cnt % 256))[2:]).rjust(2, "0")
            engine.expect_did("READ", "读取继电器操作次数C132", expect)
            engine.send_did("WRITE", "继电器翻转C018", value)
            engine.expect_did("WRITE", "通断操作C012", "0")
            engine.wait(seconds=2, tips='保证动作完成')
            cnt = opt_time[channel - 1] + 2
            expect = value + " " + str(hex(int(cnt / 256))[2:]).rjust(2, "0") + " " + str(
                hex(int(cnt % 256))[2:]).rjust(2, "0")
            engine.send_did("READ", "读取继电器操作次数C132", value)
            engine.expect_did("READ", "读取继电器操作次数C132", expect)
        if config["被测设备按键数"] == 2:
            engine.add_doc_info("3、同时动作2颗继电器，测试动作次数增加")
            engine.send_did("WRITE", "继电器翻转C018", "03")
            engine.expect_did("WRITE", "通断操作C012", "03")
        engine.wait(seconds=5, tips='保证动作完成')
        for channel, value in channel_dict.items():
            cnt = opt_time[channel - 1] + 3
            expect = value + " " + str(hex(int(cnt / 256))[2:]).rjust(2, "0") + " " + str(
                hex(int(cnt % 256))[2:]).rjust(2, "0")
            engine.send_did("READ", "读取继电器操作次数C132", value)
            engine.expect_did("READ", "读取继电器操作次数C132", expect)

        engine.send_did("WRITE", "继电器翻转C018", "07")
        engine.expect_did("WRITE", "通断操作C012", "0")
        engine.wait(seconds=5, tips='保证动作完成')
        for channel, value in channel_dict.items():
            cnt = opt_time[channel - 1] + 4
            expect = value + " " + str(hex(int(cnt / 256))[2:]).rjust(2, "0") + " " + str(
                hex(int(cnt % 256))[2:]).rjust(2, "0")
            engine.send_did("READ", "读取继电器操作次数C132", value)
            engine.expect_did("READ", "读取继电器操作次数C132", expect)

        engine.add_doc_info("4、设备断电，测试动作次数增加")
        power_control()
        engine.wait(seconds=5, tips='保证动作完成')
        for channel, value in channel_dict.items():
            cnt = opt_time[channel - 1] + 5
            expect = value + " " + str(hex(int(cnt / 256))[2:]).rjust(2, "0") + " " + str(
                hex(int(cnt % 256))[2:]).rjust(2, "0")
            engine.send_did("READ", "读取继电器操作次数C132", value)
            engine.expect_did("READ", "读取继电器操作次数C132", expect)

        engine.send_did("WRITE", "通断操作C012", "07")
        engine.expect_did("WRITE", "通断操作C012", "00")
    else:
        engine.send_did("READ", "读取继电器操作次数C132", "07")
        engine.expect_did("READ", "读取继电器操作次数C132", "82 04 00")


def test_错误类报文测试():
    """
    10_错误类报文测试
    1、数据格式错误，返回错误字00 03（C0 12的数据长度为2，而发送命令中的长度为3）
    2、数据域少一个字节，返回错误字00 01数据域长度错误
    3、发送不存在的数据项FB20，返回错误字00 04数据项不存在
    """
    if config["被测设备类型"] == '开关':
        engine.add_doc_info("1、数据格式错误，返回错误字00 03（C0 12的数据长度为1，而发送命令中的长度为3）")
        engine.send_did("WRITE", "通断操作C012", "01 02 03")
        engine.expect_did("WRITE", "通断操作C012", "03 00")
    elif config["被测设备类型"] == '面板':
        engine.add_doc_info("1、数据格式错误，返回错误字00 03（C0 12的数据长度为1，而发送命令中的长度为3）")
        engine.send_did("WRITE", "读写面板默认背光亮度百分比C135", "01 01 01")
        engine.expect_did("WRITE", "读写面板默认背光亮度百分比C135", "03 00")

    engine.add_doc_info("2、数据域少一个字节，返回错误字00 01数据域长度错误")
    engine.add_doc_info('本种错误由载波适配层判断并直接回复，所以SWB总线是监控不到的')
    engine.send_raw("07 05 D0 02 03")
    engine.expect_did("WRITE", "主动上报使能标志D005", "01 00")

    engine.add_doc_info("3、发送不存在的数据项，返回错误字00 04数据项不存在")
    engine.send_did("READ", "总有功电能9010", "")
    engine.expect_did("READ", "总有功电能9010", "04 00")


def test_复位等待时间CD00():
    """
    11_复位等待时间CD00
    1、将被测设备的参数配置成与默认参数不一致；
    2、断电重启，测试参数是否丢失；
    3、发送复位等待时间CD00，验证所有的参数均恢复出厂设置
    （其中的继电器上电状态C060、继电器过零点动作延迟时间C020、读写面板默认背光亮度百分比C135需要保持不变，
    因为该选项为工装设置，且设置后不应该被更改）
    4、将所有参数设置回默认参数，便于后续的测试项目运行
    """
    engine.add_doc_info(
        """
        将被测设备的参数配置成与默认参数不一致，如下所示；
        1、继电器上电状态C060为00上电状态为上电断开
        2、继电器过零点动作延迟时间C020设置为07 20 20 20 21 20 22
        3、主动上报使能标志D005设置为01 上报网关
        4、读取或设置被控设备端的控制地址FB20设置地址为 抄控器默认源地址
        5、读写面板默认背光亮度百分比C135 设置为07 32 32 32
        """)
    if config["被测设备类型"] == "开关":
        engine.send_did("WRITE", "继电器上电状态C060", "00")
        engine.expect_did("WRITE", "继电器上电状态C060", "00")
    else:
        engine.add_doc_info('检测到当前测试设备是面板类设备，不检测-继电器上电状态C060！！！')

    if config["被测设备硬件版本"] == "继电器版本":
        engine.send_did("WRITE", "继电器过零点动作延迟时间C020", "01 20 20")
        engine.expect_did("WRITE", "继电器过零点动作延迟时间C020", "01 20 20")
        if config["被测设备按键数"] == 2:
            engine.send_did("WRITE", "继电器过零点动作延迟时间C020", "02 20 21")
            engine.expect_did("WRITE", "继电器过零点动作延迟时间C020", "02 20 21")
    else:
        engine.add_doc_info('检测到当前测试设备是面板类设备，无-继电器上电状态C060！！！')

    if config["被测设备类型"] == "开关":
        engine.send_did("WRITE", "主动上报使能标志D005", 传感器类型="未知", 上报命令="上报网关")
        engine.expect_did("WRITE", "主动上报使能标志D005", 传感器类型="未知", 上报命令="上报网关")
    else:
        pass

    for channel, value in channel_dict.items():
        engine.send_did("WRITE", "读取或设置被控设备端的控制地址FB20",
                        设备通道=channel, 被控设备AID=config["抄控器默认源地址"], 被控设备通道=value)
        engine.expect_did("WRITE", "读取或设置被控设备端的控制地址FB20",
                          设备通道=channel, 被控设备AID=config["抄控器默认源地址"], 被控设备通道=value)

    if config["被测设备按键数"] == 2:
        engine.send_did("WRITE", "读写面板默认背光亮度百分比C135", '03 01 01')
        engine.expect_did("WRITE", "读写面板默认背光亮度百分比C135", '03 01 01')
    else:   # config["被测设备按键数"] == 1
        engine.send_did("WRITE", "读写面板默认背光亮度百分比C135", '01 01 01')
        engine.expect_did("WRITE", "读写面板默认背光亮度百分比C135", '01 01 01')

    engine.add_doc_info('控制被测设备断电重启，然后查询参数和断电前一致')
    power_control()
    if config["被测设备类型"] == "开关":
        engine.send_did("READ", "通断操作C012", "")
        engine.expect_did("READ", "通断操作C012", "00")
        engine.send_did("READ", "继电器上电状态C060")
        engine.expect_did("READ", "继电器上电状态C060", "00")

    if config["被测设备类型"] == "开关":
        engine.send_did("READ", "主动上报使能标志D005")
        engine.expect_did("READ", "主动上报使能标志D005", "00 01")
    else:
        pass

    for channel, value in channel_dict.items():
        engine.send_did("READ", "读取或设置被控设备端的控制地址FB20", 设备通道=channel)
        engine.expect_did("READ", "读取或设置被控设备端的控制地址FB20",
                          设备通道=channel, 被控设备AID=config["抄控器默认源地址"], 被控设备通道=value)
    engine.send_did("READ", "读写面板默认背光亮度百分比C135", '03')
    engine.expect_did("READ", "读写面板默认背光亮度百分比C135", '03 01 01')

    engine.add_doc_info('3、发送复位等待时间CD00，验证所有的参数均恢复出厂设置'
                        '（其中的继电器上电状态C060、继电器过零点动作延迟时间C020、读写面板默认背光亮度百分比C135需要保持不变，'
                        '因为该选项为工装设置，且设置后不应该被更改）')
    engine.send_did("WRITE", "复位等待时间CD00", "00")
    engine.expect_did("WRITE", "复位等待时间CD00", "00")

    engine.add_doc_info('下列参数恢复出厂设置成功')
    if config["被测设备类型"] == "开关":
        engine.send_did("READ", "通断操作C012", "")
        engine.expect_did("READ", "通断操作C012", "00")
        engine.send_did("READ", "主动上报使能标志D005")
        engine.expect_did("READ", "主动上报使能标志D005", "00 03")
    else:
        pass

    for channel, value in channel_dict.items():
        engine.send_did("READ", "读取或设置被控设备端的控制地址FB20", 设备通道=channel)
        engine.expect_did("READ", "读取或设置被控设备端的控制地址FB20",
                          设备通道=channel, 被控设备AID=config["测试设备地址"], 被控设备通道=value)

    engine.add_doc_info('下列参数保持不变，不受复位等待时间CD00干扰')
    if config["被测设备类型"] == "开关":
        engine.send_did("READ", "继电器上电状态C060")
        engine.expect_did("READ", "继电器上电状态C060", "00")
    else:
        pass

    if config["被测设备硬件版本"] == "继电器版本":
        engine.send_did("READ", "继电器过零点动作延迟时间C020", "01")
        engine.expect_did("READ", "继电器过零点动作延迟时间C020", "01 20 20")
        if config["被测设备按键数"] == 2:
            engine.send_did("READ", "继电器过零点动作延迟时间C020", "02")
            engine.expect_did("READ", "继电器过零点动作延迟时间C020", "02 20 21")
    engine.send_did("READ", "读写面板默认背光亮度百分比C135", '03')
    engine.expect_did("READ", "读写面板默认背光亮度百分比C135", '03 01 01')

    engine.add_doc_info('4、将CD00不能恢复的参数，设置回默认参数，便于后续的测试项目运行')
    if config["被测设备类型"] == "开关":
        engine.send_did("WRITE", "继电器上电状态C060", "02")
        engine.expect_did("WRITE", "继电器上电状态C060", "02")
    else:
        pass

    if config["被测设备硬件版本"] == "继电器版本":
        engine.send_did("WRITE", "继电器过零点动作延迟时间C020", "01 33 39")
        engine.expect_did("WRITE", "继电器过零点动作延迟时间C020", "01 33 39")
        if config["被测设备按键数"] == 2:
            engine.send_did("WRITE", "继电器过零点动作延迟时间C020", "02 33 39")
            engine.expect_did("WRITE", "继电器过零点动作延迟时间C020", "02 33 39")

    engine.send_did("WRITE", "读写面板默认背光亮度百分比C135", '01 01')
    engine.expect_did("WRITE", "读写面板默认背光亮度百分比C135", '01 01')
    if config["被测设备按键数"] == 2:
        engine.send_did("WRITE", "读写面板默认背光亮度百分比C135", '02 01')
        engine.expect_did("WRITE", "读写面板默认背光亮度百分比C135", '02 01')

    engine.add_doc_info('再次进行出厂默认参数的验证，便于后续的测试项目运行')

    engine.wait(10, tips='本轮测试结束')
