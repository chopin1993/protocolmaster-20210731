# encoding:utf-8
import engine
from autotest.公共用例.public常用测试模块 import *

测试组说明 = "功能类报文测试"


def test_出厂默认参数():
    """
    01_默认出厂参数测试
    1、出厂第一次继电器默认为断开00 通断操作C012
    2、断电后默认上电状态为02上电状态为上次断电状态 继电器上电状态C060
    3、继电器过零保护出厂默认参数为 默认断开延时1ms，默认闭合延时3ms 01 33 39 继电器过零点动作延迟时间C020
    4、状态同步默认状态03同时上报设备和网关 主动上报使能标志D005
    5、继电器延时关闭时间默认为关闭00 设备运行状态信息统计E019
    """
    # 出厂默认为00断开
    engine.send_did("READ", "通断操作C012", "")
    engine.expect_did("READ", "通断操作C012", "00")
    # 继电器上电状态C060为02保持断电前的状态
    engine.send_did("READ", "继电器上电状态C060")
    engine.expect_did("READ", "继电器上电状态C060", "02")
    # xx(通道)xx（继电器断开延迟时间）xx（继电器闭合延迟时间）
    # 默认断开延时5.1ms（51=0x33），默认闭合延时5.7ms(57=0x39)
    engine.send_did("READ", "继电器过零点动作延迟时间C020", "01")
    engine.expect_did("READ", "继电器过零点动作延迟时间C020", "01 33 39")
    # 主动上报使能标志D005默认为03，同时上报设备和网关
    engine.send_did("READ", "主动上报使能标志D005")
    engine.expect_did("READ", "主动上报使能标志D005", "00 03")
    # 触摸开关默认控制的设备AID为自身的AID
    engine.send_did("READ", "读取或设置被控设备端的控制地址FB20", 设备通道="01")
    engine.expect_did("READ", "读取或设置被控设备端的控制地址FB20", 设备通道="01",被控设备AID=config["测试设备地址"],被控设备通道='01')
    # 面板的默认背光亮度为1%
    engine.send_did("READ", "读写面板默认背光亮度百分比C135", 设备通道="01")
    engine.expect_did("READ", "读写面板默认背光亮度百分比C135", 设备通道="01",背光亮度='01')

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
    engine.expect_cross_zero_status(0,1)


    engine.send_did("WRITE", "通断操作C012", "01")
    engine.expect_did("WRITE", "通断操作C012", "00")
    engine.wait(1)
    engine.send_did("READ", "通断操作C012", "")
    engine.expect_did("READ", "通断操作C012", "00")
    engine.add_doc_info('监测器检测被测设备的输出端')
    engine.expect_cross_zero_status(0,0)



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
    engine.expect_cross_zero_status(0,1)

    engine.send_did("WRITE", "继电器翻转C018", "01")
    engine.expect_did("WRITE", "通断操作C012", "00")
    engine.wait(1)
    engine.send_did("READ", "通断操作C012", "")
    engine.expect_did("READ", "通断操作C012", "00")
    engine.add_doc_info('监测器检测被测设备的输出端')
    engine.expect_cross_zero_status(0,0)

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
    engine.send_did("READ", "主动上报使能标志D005","")
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


def test_设备运行状态信息统计E019():
    """
    07_读取或设置被控设备端的控制地址FB20
    0x08-（被测设备）延时关闭时间（毫秒）TT+XXXXXXXX
    写操作为清除某个信息项的统计信息，XX必须为00；
    1、查询延时闭合时间E019默认为关闭
    2、设置延时闭合时间为10s，并进行验证
    3、设置延时闭合时间为60s，并进行验证
    4、设置延时闭合时间为0s关闭状态，并进行验证
    """
    engine.add_doc_info("查询延时闭合时间E019默认为关闭")
    engine.send_did("READ", "设备运行状态信息统计E019", E019设备信息项="延时关闭时间毫秒")
    engine.expect_did("READ", "设备运行状态信息统计E019", E019设备信息项="延时关闭时间毫秒", 时间=0)

    engine.send_did("WRITE", "设备运行状态信息统计E019", E019设备信息项="延时关闭时间毫秒", 时间=10)
    engine.expect_did("WRITE", "设备运行状态信息统计E019", E019设备信息项="延时关闭时间毫秒", 时间=10)
    engine.send_did("READ", "设备运行状态信息统计E019", E019设备信息项="延时关闭时间毫秒")
    engine.expect_did("READ", "设备运行状态信息统计E019", E019设备信息项="延时关闭时间毫秒", 时间=10)

    engine.send_did("WRITE", "设备运行状态信息统计E019", E019设备信息项="延时关闭时间毫秒", 时间=6000)
    engine.expect_did("WRITE", "设备运行状态信息统计E019", E019设备信息项="延时关闭时间毫秒", 时间=6000)
    engine.send_did("READ", "设备运行状态信息统计E019", E019设备信息项="延时关闭时间毫秒")
    engine.expect_did("READ", "设备运行状态信息统计E019", E019设备信息项="延时关闭时间毫秒", 时间=6000)

    engine.send_did("WRITE", "设备运行状态信息统计E019", E019设备信息项="延时关闭时间毫秒", 时间=0)
    engine.expect_did("WRITE", "设备运行状态信息统计E019", E019设备信息项="延时关闭时间毫秒", 时间=0)
    engine.send_did("READ", "设备运行状态信息统计E019", E019设备信息项="延时关闭时间毫秒")
    engine.expect_did("READ", "设备运行状态信息统计E019", E019设备信息项="延时关闭时间毫秒", 时间=0)


def test_错误类报文测试():
    """
    08_错误类报文测试
    1、数据格式错误，返回错误字00 03（C0 12的数据长度为2，而发送命令中的长度为3）
    2、数据域少一个字节，返回错误字00 01数据域长度错误
    3、发送不存在的数据项FB20，返回错误字00 04数据项不存在
    """
    engine.add_doc_info("1、数据格式错误，返回错误字00 03（C0 12的数据长度为1，而发送命令中的长度为3）")

    engine.send_did("WRITE", "通断操作C012", "01 02 03")
    engine.expect_did("WRITE", "通断操作C012", "03 00")

    engine.add_doc_info("2、数据域少一个字节，返回错误字00 01数据域长度错误")
    engine.send_raw("07 05 D0 02 03")
    engine.expect_did("WRITE", "主动上报使能标志D005", "01 00")

    engine.add_doc_info("3、发送不存在的数据项FB20，返回错误字00 04数据项不存在")
    engine.send_did("READ", "读取或设置被控设备端的控制地址FB20", "01")
    engine.expect_did("READ", "读取或设置被控设备端的控制地址FB20", "04 00")


def test_参数修改后断电验证():
    """
    09_参数修改后断电验证
    1、将被测设备的参数配置成与默认参数不一致；
    2、断电重启，测试参数是否丢失；
    3、将参数设置回默认参数，便于后续的测试项目运行
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

    # 断电重启，然后查询参数和断电前一致
    power_control()

    engine.send_did("READ", "继电器上电状态C060")
    engine.expect_did("READ", "继电器上电状态C060", "00")
    engine.send_did("READ", "继电器过零点动作延迟时间C020", "01")
    engine.expect_did("READ", "继电器过零点动作延迟时间C020", "01 20 20")
    engine.send_did("READ", "主动上报使能标志D005")
    engine.expect_did("READ", "主动上报使能标志D005", 传感器类型="未知", 上报命令="上报网关")
    engine.send_did("READ", "设备运行状态信息统计E019", E019设备信息项="延时关闭时间毫秒")
    engine.expect_did("READ", "设备运行状态信息统计E019", E019设备信息项="延时关闭时间毫秒", 时间=6000)

    # 将修改后的参数，设置回默认参数
    engine.send_did("WRITE", "通断操作C012", "01")
    engine.expect_did("WRITE", "通断操作C012", "00")
    engine.send_did("WRITE", "继电器上电状态C060", "02")
    engine.expect_did("WRITE", "继电器上电状态C060", "02")
    engine.send_did("WRITE", "继电器过零点动作延迟时间C020", "01 33 39")
    engine.expect_did("WRITE", "继电器过零点动作延迟时间C020", "01 33 39")
    engine.send_did("WRITE", "主动上报使能标志D005", 传感器类型="未知", 上报命令="同时上报设备和网关")
    engine.expect_did("WRITE", "主动上报使能标志D005", 传感器类型="未知", 上报命令="同时上报设备和网关")
    engine.send_did("WRITE", "设备运行状态信息统计E019", E019设备信息项="延时关闭时间毫秒", 时间=0)
    engine.expect_did("WRITE", "设备运行状态信息统计E019", E019设备信息项="延时关闭时间毫秒", 时间=0)
