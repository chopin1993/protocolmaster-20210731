# encoding:utf-8
from autotest.公共用例.public常用测试模块 import *

测试组说明 = "功能类报文测试"


def test_出厂默认参数():
    """
    01_默认出厂参数测试
    1、出厂第一次继电器默认为断开00 通断操作C012
    2、断电后默认上电状态为02上电状态为上次断电状态 继电器上电状态C060
    3、继电器过零保护出厂默认参数为 默认断开延时1ms，默认闭合延时3ms 01 33 39 继电器过零点动作延迟时间C020
    4、状态同步默认状态03同时上报设备和网关 主动上报使能标志D005
    5、触摸开关默认控制的设备AID为自身的AID 读取或设置被控设备端的控制地址FB20
    6、面板的默认背光亮度为1% 读写面板默认背光亮度百分比C135
    """
    engine.add_doc_info('1、出厂第一次继电器默认为断开00 通断操作C012 '
                        '2、断电后默认上电状态为02上电状态为上次断电状态 继电器上电状态C060'
                        '3、继电器过零保护出厂默认参数为 默认断开延时1ms，默认闭合延时3ms 01 33 39 继电器过零点动作延迟时间C020 '
                        '4、状态同步默认状态03同时上报设备和网关 主动上报使能标志D005 '
                        '5、触摸开关默认控制的设备AID为自身的AID 读取或设置被控设备端的控制地址FB20 '
                        '6、面板的默认背光亮度为1% 读写面板默认背光亮度百分比C135')
    engine.send_did("READ", "通断操作C012", "")
    engine.expect_did("READ", "通断操作C012", "00")
    engine.send_did("READ", "继电器上电状态C060")
    engine.expect_did("READ", "继电器上电状态C060", "02")
    engine.send_did("READ", "继电器过零点动作延迟时间C020", "01")
    engine.expect_did("READ", "继电器过零点动作延迟时间C020", "01 33 39")
    engine.send_did("READ", "主动上报使能标志D005")
    engine.expect_did("READ", "主动上报使能标志D005", "00 03")
    engine.send_did("READ", "读取或设置被控设备端的控制地址FB20", 设备通道="01")
    engine.expect_did("READ", "读取或设置被控设备端的控制地址FB20", 设备通道="01", 被控设备AID=config["测试设备地址"], 被控设备通道='01')
    engine.send_did("READ", "读写面板默认背光亮度百分比C135", 设备通道="01")
    engine.expect_did("READ", "读写面板默认背光亮度百分比C135", 设备通道="01", 背光亮度='01')


def test_通断操作C012():
    """
    02_通断操作C012
    1、查询当前通断状态00
    2、打开通道，然后查询当前通断状态
    3、关闭通道，然后查询当前通断状态
    """
    engine.send_did("READ", "通断操作C012", "")
    engine.expect_did("READ", "通断操作C012", "00")

    engine.send_did("WRITE", "通断操作C012", "81")
    engine.expect_did("WRITE", "通断操作C012", "01")
    engine.wait(1)
    engine.send_did("READ", "通断操作C012", "")
    engine.expect_did("READ", "通断操作C012", "01")
    engine.add_doc_info('监测器检测被测设备的输出端')
    engine.expect_cross_zero_status(0, 1)

    engine.send_did("WRITE", "通断操作C012", "01")
    engine.expect_did("WRITE", "通断操作C012", "00")
    engine.wait(1)
    engine.send_did("READ", "通断操作C012", "")
    engine.expect_did("READ", "通断操作C012", "00")
    engine.add_doc_info('监测器检测被测设备的输出端')
    engine.expect_cross_zero_status(0, 0)


def test_继电器翻转C018():
    """
    03_继电器翻转C018
    bit5~bit0:1/0表示通道操作/不操作；bit0表示第1个通道，回复时按C012报文格式回复
    1、查询当前通断状态00关闭
    2、继电器翻转，然后查询当前通断状态01打开
    3、继电器翻转，然后查询当前通断状态00关闭
    """
    engine.send_did("READ", "通断操作C012", "")
    engine.expect_did("READ", "通断操作C012", "00")

    engine.send_did("WRITE", "继电器翻转C018", "01")
    engine.expect_did("WRITE", "通断操作C012", "01")
    engine.wait(1)
    engine.send_did("READ", "通断操作C012", "")
    engine.expect_did("READ", "通断操作C012", "01")
    engine.add_doc_info('监测器检测被测设备的输出端')
    engine.expect_cross_zero_status(0, 1)

    engine.send_did("WRITE", "继电器翻转C018", "01")
    engine.expect_did("WRITE", "通断操作C012", "00")
    engine.wait(1)
    engine.send_did("READ", "通断操作C012", "")
    engine.expect_did("READ", "通断操作C012", "00")
    engine.add_doc_info('监测器检测被测设备的输出端')
    engine.expect_cross_zero_status(0, 0)


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
    # 02上电状态为上次断电状态
    engine.send_did("READ", "继电器上电状态C060", "")
    engine.expect_did("READ", "继电器上电状态C060", "02")

    engine.add_doc_info("测试被测设备为开的时候断电，根据配置，断电重启后为开")
    engine.send_did("WRITE", "通断操作C012", "81")
    engine.expect_did("WRITE", "通断操作C012", "01")
    power_control()
    engine.send_did("READ", "通断操作C012", "")
    engine.expect_did("READ", "通断操作C012", "01")
    engine.add_doc_info('监测器检测被测设备的输出端')
    engine.expect_cross_zero_status(0, 1)

    engine.add_doc_info("测试被测设备为关的时候断电，根据配置，断电重启后为关")
    engine.send_did("WRITE", "通断操作C012", "01")
    engine.expect_did("WRITE", "通断操作C012", "00")
    power_control()
    engine.send_did("READ", "通断操作C012", "")
    engine.expect_did("READ", "通断操作C012", "00")
    engine.add_doc_info('监测器检测被测设备的输出端')
    engine.expect_cross_zero_status(0, 0)

    # 00上电状态为上电断开
    engine.add_doc_info("测试上电状态为上电断开，通过前置的工装通断电，给被测设备通断电")
    engine.send_did("WRITE", "继电器上电状态C060", "00")
    engine.expect_did("WRITE", "继电器上电状态C060", "00")
    engine.send_did("READ", "继电器上电状态C060", "")
    engine.expect_did("READ", "继电器上电状态C060", "00")

    engine.add_doc_info("测试被测设备为开的时候断电，根据配置，断电重启后为关")
    engine.send_did("WRITE", "通断操作C012", "81")
    engine.expect_did("WRITE", "通断操作C012", "01")
    power_control()
    engine.send_did("READ", "通断操作C012", "")
    engine.expect_did("READ", "通断操作C012", "00")
    engine.add_doc_info('监测器检测被测设备的输出端')
    engine.expect_cross_zero_status(0, 0)

    engine.add_doc_info("测试被测设备为关的时候断电，根据配置，断电重启后为关")
    engine.send_did("WRITE", "通断操作C012", "01")
    engine.expect_did("WRITE", "通断操作C012", "00")
    power_control()
    engine.send_did("READ", "通断操作C012", "")
    engine.expect_did("READ", "通断操作C012", "00")
    engine.add_doc_info('监测器检测被测设备的输出端')
    engine.expect_cross_zero_status(0, 0)

    # 01上电状态为上电闭合
    engine.add_doc_info("测试上电状态为上电闭合，通过前置的工装通断电，给被测设备通断电")
    engine.send_did("WRITE", "继电器上电状态C060", "01")
    engine.expect_did("WRITE", "继电器上电状态C060", "01")
    engine.send_did("READ", "继电器上电状态C060")
    engine.expect_did("READ", "继电器上电状态C060", "01")

    engine.add_doc_info("测试被测设备为开的时候断电，根据配置，断电重启后为开")
    engine.send_did("WRITE", "通断操作C012", "81")
    engine.expect_did("WRITE", "通断操作C012", "01")
    power_control()
    engine.send_did("READ", "通断操作C012", "")
    engine.expect_did("READ", "通断操作C012", "01")
    engine.add_doc_info('监测器检测被测设备的输出端')
    engine.expect_cross_zero_status(0, 1)

    engine.add_doc_info("测试被测设备为关的时候断电，根据配置，断电重启后为开")
    engine.send_did("WRITE", "通断操作C012", "01")
    engine.expect_did("WRITE", "通断操作C012", "00")
    power_control()
    engine.send_did("READ", "通断操作C012", "")
    engine.expect_did("READ", "通断操作C012", "01")
    engine.add_doc_info('监测器检测被测设备的输出端')
    engine.expect_cross_zero_status(0, 1)

    engine.add_doc_info('设置回默认参数，02上电状态为上次断电状态')
    engine.send_did("WRITE", "继电器上电状态C060", "02")
    engine.expect_did("WRITE", "继电器上电状态C060", "02")
    engine.send_did("READ", "继电器上电状态C060")
    engine.expect_did("READ", "继电器上电状态C060", "02")


def test_继电器过零点动作延迟时间C020():
    """
    05_继电器过零点动作延迟时间C020
    xx(通道)xx（继电器断开延迟时间ms）xx（继电器闭合延迟时间）
    1、查询被测设备的默认参数
    2、设置过零点动作时间为01 00 00，并进行查询验证
    3、设置过零点动作时间为01 20 20，并进行查询验证
    4、设置回零点动作时间为01 33 39，并进行查询验证
    """
    engine.add_doc_info("查询默认的继电器过零点动作延迟时间C020，01 33 39")
    engine.send_did("READ", "继电器过零点动作延迟时间C020", "01")
    engine.expect_did("READ", "继电器过零点动作延迟时间C020", "01 33 39")

    engine.add_doc_info("测试设置不同的继电器过零点动作延迟时间C020，要求均可以设置成功")
    engine.send_did("WRITE", "继电器过零点动作延迟时间C020", "01 00 00")
    engine.expect_did("WRITE", "继电器过零点动作延迟时间C020", "01 00 00")
    engine.send_did("READ", "继电器过零点动作延迟时间C020", "01")
    engine.expect_did("READ", "继电器过零点动作延迟时间C020", "01 00 00")

    engine.add_doc_info("测试设置不同的继电器过零点动作延迟时间C020，要求均可以设置成功")
    engine.send_did("WRITE", "继电器过零点动作延迟时间C020", "01 20 20")
    engine.expect_did("WRITE", "继电器过零点动作延迟时间C020", "01 20 20")
    engine.send_did("READ", "继电器过零点动作延迟时间C020", "01")
    engine.expect_did("READ", "继电器过零点动作延迟时间C020", "01 20 20")

    engine.add_doc_info("为便于后续的测试，将参数设置回默认参数")
    engine.send_did("WRITE", "继电器过零点动作延迟时间C020", "01 33 39")
    engine.expect_did("WRITE", "继电器过零点动作延迟时间C020", "01 33 39")
    engine.send_did("READ", "继电器过零点动作延迟时间C020", "01")
    engine.expect_did("READ", "继电器过零点动作延迟时间C020", "01 33 39")


def test_主动上报使能标志D005():
    """
    06_主动上报使能标志D005
    TT为传感器类型，XX 为0x00:无上报；0x01：上报网关；0x02：上报设备；0x03同时上报设备和网关（状态同步的普遍使用方案）；
    1、查询被测设备的默认状态同步使能参数为03
    2、设置主动上报使能标志D005为00：无上报，并进行查询验证
    3、设置主动上报使能标志D005为01：上报网关，并进行查询验证
    4、设置主动上报使能标志D005为02：上报设备，并进行查询验证
    5、设置主动上报使能标志D005为03：同时上报设备和网关，并进行查询验证
    """
    engine.add_doc_info("查询被测设备的默认状态同步使能参数为03")
    engine.send_did("READ", "主动上报使能标志D005", "")
    engine.expect_did("READ", "主动上报使能标志D005", 传感器类型="未知", 上报命令="同时上报设备和网关")

    engine.add_doc_info('设置为无上报模式并进行查询验证')
    engine.send_did("WRITE", "主动上报使能标志D005", 传感器类型="未知", 上报命令="无上报")
    engine.expect_did("WRITE", "主动上报使能标志D005", 传感器类型="未知", 上报命令="无上报")
    engine.send_did("READ", "主动上报使能标志D005")
    engine.expect_did("READ", "主动上报使能标志D005", 传感器类型="未知", 上报命令="无上报")

    engine.add_doc_info('设置为上报网关模式并进行查询验证')
    engine.send_did("WRITE", "主动上报使能标志D005", 传感器类型="未知", 上报命令="上报网关")
    engine.expect_did("WRITE", "主动上报使能标志D005", 传感器类型="未知", 上报命令="上报网关")
    engine.send_did("READ", "主动上报使能标志D005")
    engine.expect_did("READ", "主动上报使能标志D005", 传感器类型="未知", 上报命令="上报网关")

    engine.add_doc_info('设置为上报设备模式并进行查询验证')
    engine.send_did("WRITE", "主动上报使能标志D005", 传感器类型="未知", 上报命令="上报设备")
    engine.expect_did("WRITE", "主动上报使能标志D005", 传感器类型="未知", 上报命令="上报设备")
    engine.send_did("READ", "主动上报使能标志D005")
    engine.expect_did("READ", "主动上报使能标志D005", 传感器类型="未知", 上报命令="上报设备")

    engine.add_doc_info('设置为同时上报设备和网关模式并进行查询验证')
    engine.send_did("WRITE", "主动上报使能标志D005", 传感器类型="未知", 上报命令="同时上报设备和网关")
    engine.expect_did("WRITE", "主动上报使能标志D005", 传感器类型="未知", 上报命令="同时上报设备和网关")
    engine.send_did("READ", "主动上报使能标志D005")
    engine.expect_did("READ", "主动上报使能标志D005", 传感器类型="未知", 上报命令="同时上报设备和网关")


def test_读取或设置被控设备端的控制地址FB20():
    """
    07_读取或设置被控设备端的控制地址FB20
    1、查询默认配置，为自身的AID；
    2、配置其他的设备AID，并进行查询验证；
    3、配置回默认参数，并进行查询验证；
    """
    engine.add_doc_info("1、查询默认配置，为自身的AID")
    engine.send_did("READ", "读取或设置被控设备端的控制地址FB20", 设备通道="01")
    engine.expect_did("READ", "读取或设置被控设备端的控制地址FB20",
                      设备通道="01", 被控设备AID=config["测试设备地址"], 被控设备通道='01')

    engine.add_doc_info("2、配置其他的设备AID，并进行查询验证")
    engine.send_did("WRITE", "读取或设置被控设备端的控制地址FB20",
                    设备通道="01", 被控设备AID=config["抄控器默认源地址"], 被控设备通道='01')
    engine.expect_did("WRITE", "读取或设置被控设备端的控制地址FB20",
                      设备通道="01", 被控设备AID=config["抄控器默认源地址"], 被控设备通道='01')
    engine.send_did("READ", "读取或设置被控设备端的控制地址FB20", 设备通道="01")
    engine.expect_did("READ", "读取或设置被控设备端的控制地址FB20",
                      设备通道="01", 被控设备AID=config["抄控器默认源地址"], 被控设备通道='01')

    engine.add_doc_info('模拟点击控制其他设备闭合和断开，进行相关的测试')
    engine.set_device_sensor_status("按键输入", "短按")
    engine.expect_did('WRITE', '继电器翻转C018', '01', check_seq=False)
    engine.send_did('WRITE', '通断操作C012', '01', reply=True)
    engine.wait(1)
    engine.set_device_sensor_status("按键输入", "短按")
    engine.expect_did('WRITE', '继电器翻转C018', '01', check_seq=False)
    engine.send_did('WRITE', '通断操作C012', '00', reply=True)

    engine.add_doc_info("3、配置回默认参数，并进行查询验证")
    engine.send_did("WRITE", "读取或设置被控设备端的控制地址FB20",
                    设备通道="01", 被控设备AID=config["测试设备地址"], 被控设备通道='01')
    engine.expect_did("WRITE", "读取或设置被控设备端的控制地址FB20",
                      设备通道="01", 被控设备AID=config["测试设备地址"], 被控设备通道='01')
    engine.send_did("READ", "读取或设置被控设备端的控制地址FB20", 设备通道="01")
    engine.expect_did("READ", "读取或设置被控设备端的控制地址FB20",
                      设备通道="01", 被控设备AID=config["测试设备地址"], 被控设备通道='01')


def test_读写面板默认背光亮度百分比C135():
    """
    08_读写面板默认背光亮度百分比C135
    1、查询默认的背光亮度百分比为1%
    2、设置背光亮度百分比为其他数值，如0、50%、100%、200%，并进行验证0和200%不支持配置，50%和100%配置正常
    3、设置背光亮度百分比回默认1%，并进行验证
    """
    engine.add_doc_info("1、查询默认的背光亮度百分比为1%")
    engine.send_did("READ", "读写面板默认背光亮度百分比C135", 设备通道="01")
    engine.expect_did("READ", "读写面板默认背光亮度百分比C135", 设备通道="01", 背光亮度=1)

    engine.add_doc_info("2、设置背光亮度百分比为其他数值")
    for i in [10, 50, 100]:
        engine.send_did("WRITE", "读写面板默认背光亮度百分比C135", 设备通道="01", 背光亮度=i)
        engine.expect_did("WRITE", "读写面板默认背光亮度百分比C135", 设备通道="01", 背光亮度=i)
        engine.send_did("READ", "读写面板默认背光亮度百分比C135", 设备通道="01")
        engine.expect_did("READ", "读写面板默认背光亮度百分比C135", 设备通道="01", 背光亮度=i)

    engine.add_doc_info('设置不支持的背光百分比范围，均回复0003格式不正确')
    for i in [0, 101, 200]:
        engine.send_did("WRITE", "读写面板默认背光亮度百分比C135", 设备通道="01", 背光亮度=i)
    engine.expect_did("WRITE", "读写面板默认背光亮度百分比C135", '03 00')
    engine.add_doc_info('设置不支持的背光百分比范围不成功，背光百分比仍是之前设置成功的参数')

    engine.send_did("READ", "读写面板默认背光亮度百分比C135", 设备通道="01")
    engine.expect_did("READ", "读写面板默认背光亮度百分比C135", 设备通道="01", 背光亮度=100)

    engine.add_doc_info("3、设置背光亮度百分比回默认1%，并进行验证")
    engine.send_did("WRITE", "读写面板默认背光亮度百分比C135", 设备通道="01", 背光亮度=1)
    engine.expect_did("WRITE", "读写面板默认背光亮度百分比C135", 设备通道="01", 背光亮度=1)
    engine.send_did("READ", "读写面板默认背光亮度百分比C135", 设备通道="01")
    engine.expect_did("READ", "读写面板默认背光亮度百分比C135", 设备通道="01", 背光亮度=1)


def test_错误类报文测试():
    """
    09_错误类报文测试
    1、数据格式错误，返回错误字00 03（C0 12的数据长度为2，而发送命令中的长度为3）
    2、数据域少一个字节，返回错误字00 01数据域长度错误
    3、发送不存在的数据项FB20，返回错误字00 04数据项不存在
    """
    engine.add_doc_info("1、数据格式错误，返回错误字00 03（C0 12的数据长度为1，而发送命令中的长度为3）")
    engine.send_did("WRITE", "通断操作C012", "01 02 03")
    engine.expect_did("WRITE", "通断操作C012", "03 00")

    engine.add_doc_info("2、数据域少一个字节，返回错误字00 01数据域长度错误")
    engine.add_doc_info('本种错误由载波适配层判断并直接回复，所以SWB总线是监控不到的')
    engine.send_raw("07 05 D0 02 03")
    engine.expect_did("WRITE", "主动上报使能标志D005", "01 00")

    engine.add_doc_info("3、发送不存在的数据项，返回错误字00 04数据项不存在")
    engine.send_did("READ", "总有功电能9010", "")
    engine.expect_did("READ", "总有功电能9010", "04 00")


def test_复位等待时间CD00():
    """
    10_复位等待时间CD00
    1、将被测设备的参数配置成与默认参数不一致；
    2、断电重启，测试参数是否丢失；
    3、发送复位等待时间CD00，验证所有的参数均恢复出厂设置
    （其中的继电器上电状态C060、继电器过零点动作延迟时间C020、读写面板默认背光亮度百分比C135需要保持不变，
    因为该选项为工装设置，且设置后不应该被更改）
    4、将所有参数设置回默认参数，便于后续的测试项目运行
    """
    engine.add_doc_info(
        """
        1、继电器上电状态C060为00上电状态为上电断开
        2、继电器过零点动作延迟时间C020设置为01 20 20
        3、主动上报使能标志D005设置为01 上报网关
        4、读取或设置被控设备端的控制地址FB20设置地址为 抄控器默认源地址
        5、读写面板默认背光亮度百分比C135 设置为50% 
        """)
    engine.send_did("WRITE", "继电器上电状态C060", "00")
    engine.expect_did("WRITE", "继电器上电状态C060", "00")
    engine.send_did("WRITE", "继电器过零点动作延迟时间C020", "01 20 20")
    engine.expect_did("WRITE", "继电器过零点动作延迟时间C020", "01 20 20")
    engine.send_did("WRITE", "主动上报使能标志D005", 传感器类型="未知", 上报命令="上报网关")
    engine.expect_did("WRITE", "主动上报使能标志D005", 传感器类型="未知", 上报命令="上报网关")
    engine.send_did("WRITE", "读取或设置被控设备端的控制地址FB20",
                    设备通道="01", 被控设备AID=config["抄控器默认源地址"], 被控设备通道='01')
    engine.expect_did("WRITE", "读取或设置被控设备端的控制地址FB20",
                      设备通道="01", 被控设备AID=config["抄控器默认源地址"], 被控设备通道='01')
    engine.send_did("WRITE", "读写面板默认背光亮度百分比C135", 设备通道="01", 背光亮度=50)
    engine.expect_did("WRITE", "读写面板默认背光亮度百分比C135", 设备通道="01", 背光亮度=50)

    engine.add_doc_info('控制被测设备断电重启，然后查询参数和断电前一致')
    power_control()
    engine.send_did("READ", "通断操作C012", "")
    engine.expect_did("READ", "通断操作C012", "00")
    engine.send_did("READ", "继电器上电状态C060")
    engine.expect_did("READ", "继电器上电状态C060", "00")
    engine.send_did("READ", "继电器过零点动作延迟时间C020", "01")
    engine.expect_did("READ", "继电器过零点动作延迟时间C020", "01 20 20")
    engine.send_did("READ", "主动上报使能标志D005")
    engine.expect_did("READ", "主动上报使能标志D005", "00 01")
    engine.send_did("READ", "读取或设置被控设备端的控制地址FB20", 设备通道="01")
    engine.expect_did("READ", "读取或设置被控设备端的控制地址FB20", 设备通道="01", 被控设备AID=config["抄控器默认源地址"], 被控设备通道='01')
    engine.send_did("READ", "读写面板默认背光亮度百分比C135", 设备通道="01")
    engine.expect_did("READ", "读写面板默认背光亮度百分比C135", 设备通道="01", 背光亮度='50')

    engine.add_doc_info('3、发送复位等待时间CD00，验证所有的参数均恢复出厂设置'
                        '（其中的继电器上电状态C060、继电器过零点动作延迟时间C020、读写面板默认背光亮度百分比C135需要保持不变，'
                        '因为该选项为工装设置，且设置后不应该被更改）')
    engine.send_did("WRITE", "复位等待时间CD00", "00")
    engine.expect_did("WRITE", "复位等待时间CD00", "00")

    engine.send_did("READ", "通断操作C012", "")
    engine.expect_did("READ", "通断操作C012", "00")
    engine.send_did("READ", "主动上报使能标志D005")
    engine.expect_did("READ", "主动上报使能标志D005", "00 03")
    engine.send_did("READ", "读取或设置被控设备端的控制地址FB20", 设备通道="01")
    engine.expect_did("READ", "读取或设置被控设备端的控制地址FB20", 设备通道="01", 被控设备AID=config["测试设备地址"], 被控设备通道='01')

    engine.send_did("READ", "继电器上电状态C060")
    engine.expect_did("READ", "继电器上电状态C060", "00")
    engine.send_did("READ", "继电器过零点动作延迟时间C020", "01")
    engine.expect_did("READ", "继电器过零点动作延迟时间C020", "01 20 20")
    engine.send_did("READ", "读写面板默认背光亮度百分比C135", 设备通道="01")
    engine.expect_did("READ", "读写面板默认背光亮度百分比C135", 设备通道="01", 背光亮度='50')

    engine.add_doc_info('4、将CD00不能恢复的参数，设置回默认参数，便于后续的测试项目运行')
    engine.send_did("WRITE", "继电器上电状态C060", "02")
    engine.expect_did("WRITE", "继电器上电状态C060", "02")
    engine.send_did("WRITE", "继电器过零点动作延迟时间C020", "01 33 39")
    engine.expect_did("WRITE", "继电器过零点动作延迟时间C020", "01 33 39")
    engine.send_did("WRITE", "读写面板默认背光亮度百分比C135", 设备通道="01", 背光亮度=1)
    engine.expect_did("WRITE", "读写面板默认背光亮度百分比C135", 设备通道="01", 背光亮度=1)

    engine.add_doc_info('再次进行出厂默认参数的验证，便于后续的测试项目运行')
    test_出厂默认参数()
