# encoding:utf-8
import engine
from autotest.公共用例.public常用测试模块 import *
import time

测试组说明 = "功能类报文测试"


def test_出厂默认参数():
    """
    01_默认出厂参数测试
    1、出厂第一次继电器默认为断开00 通断操作C012
    2、断电后默认上电状态为02上电状态为上次断电状态 继电器上电状态C060
    3、状态同步默认状态03同时上报设备和网关 主动上报使能标志D005
    4、面板锁定默认处于00停止状态
    """
    engine.add_doc_info('01_默认出厂参数测试')

    engine.send_did("READ", "通断操作C012", "")
    engine.expect_did("READ", "通断操作C012", "00")

    engine.send_did("READ", "继电器上电状态C060", "")
    engine.expect_did("READ", "继电器上电状态C060", "02")

    engine.send_did("READ", "主动上报使能标志D005", "")
    engine.expect_did("READ", "主动上报使能标志D005", "0A 03")

    engine.send_did("READ", "面板锁定E014", "")
    engine.expect_did("READ", "面板锁定E014", "00")


def test_通断操作C012():
    """
    02_通断操作C012
    1、查询当前通断状态00
    2、打开通道，然后查询当前通断状态
    3、关闭通道，然后查询当前通断状态
    """
    engine.add_doc_info('02_通断操作C012测试')
    engine.send_did("READ", "通断操作C012", "")
    engine.expect_did("READ", "通断操作C012", "00")

    engine.send_did("WRITE", "通断操作C012", "81")
    engine.expect_did("WRITE", "通断操作C012", "01")
    engine.wait(1)
    engine.send_did("READ", "通断操作C012", "")
    engine.expect_did("READ", "通断操作C012", "01")

    engine.send_did("WRITE", "通断操作C012", "01")
    engine.expect_did("WRITE", "通断操作C012", "00")
    engine.wait(1)
    engine.send_did("READ", "通断操作C012", "")
    engine.expect_did("READ", "通断操作C012", "00")


def test_继电器翻转C018():
    """
    03_继电器翻转C018
    bit5~bit0:1/0表示通道操作/不操作；bit0表示第1个通道，回复时按C012报文格式回复
    1、查询当前通断状态00关闭
    2、继电器翻转，然后查询当前通断状态01打开
    3、继电器翻转，然后查询当前通断状态00关闭
    """
    engine.add_doc_info('03_继电器翻转C018测试')
    engine.send_did("READ", "通断操作C012", "")
    engine.expect_did("READ", "通断操作C012", "00")

    engine.send_did("WRITE", "继电器翻转C018", "01")
    engine.expect_did("WRITE", "通断操作C012", "01")
    engine.wait(1)
    engine.send_did("READ", "通断操作C012", "")
    engine.expect_did("READ", "通断操作C012", "01")

    engine.send_did("WRITE", "继电器翻转C018", "01")
    engine.expect_did("WRITE", "通断操作C012", "00")
    engine.wait(1)
    engine.send_did("READ", "通断操作C012", "")
    engine.expect_did("READ", "通断操作C012", "00")


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

    engine.add_doc_info("测试被测设备为关的时候断电，根据配置，断电重启后为关")
    engine.send_did("WRITE", "通断操作C012", "01")
    engine.expect_did("WRITE", "通断操作C012", "00")
    power_control()
    engine.send_did("READ", "通断操作C012", "")
    engine.expect_did("READ", "通断操作C012", "00")

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

    engine.add_doc_info("测试被测设备为关的时候断电，根据配置，断电重启后为关")
    engine.send_did("WRITE", "通断操作C012", "01")
    engine.expect_did("WRITE", "通断操作C012", "00")
    power_control()
    engine.send_did("READ", "通断操作C012", "")
    engine.expect_did("READ", "通断操作C012", "00")

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

    engine.add_doc_info("测试被测设备为关的时候断电，根据配置，断电重启后为开")
    engine.send_did("WRITE", "通断操作C012", "01")
    engine.expect_did("WRITE", "通断操作C012", "00")
    power_control()
    engine.send_did("READ", "通断操作C012", "")
    engine.expect_did("READ", "通断操作C012", "01")
    # 设置回默认参数，02上电状态为上次断电状态
    engine.send_did("WRITE", "继电器上电状态C060", "02")
    engine.expect_did("WRITE", "继电器上电状态C060", "02")
    engine.send_did("READ", "继电器上电状态C060")
    engine.expect_did("READ", "继电器上电状态C060", "02")


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
    engine.add_doc_info("查询被测设备的默认状态同步使能参数为03")
    engine.send_did("READ", "主动上报使能标志D005","")
    engine.expect_did("READ", "主动上报使能标志D005", 传感器类型="通断", 上报命令="同时上报设备和网关")
    # 智能交互终端不支持设置无上报模式，该设置被屏蔽
    engine.send_did("WRITE", "主动上报使能标志D005", 传感器类型="未知", 上报命令="无上报")
    engine.expect_did("WRITE", "主动上报使能标志D005", '03 00')
    engine.send_did("READ", "主动上报使能标志D005")
    engine.expect_did("READ", "主动上报使能标志D005", 传感器类型="通断", 上报命令="同时上报设备和网关")

    engine.send_did("WRITE", "主动上报使能标志D005", 传感器类型="未知", 上报命令="上报网关")
    engine.expect_did("WRITE", "主动上报使能标志D005", 传感器类型="未知", 上报命令="上报网关")
    engine.send_did("READ", "主动上报使能标志D005")
    engine.expect_did("READ", "主动上报使能标志D005", 传感器类型="通断", 上报命令="上报网关")

    engine.send_did("WRITE", "主动上报使能标志D005", 传感器类型="未知", 上报命令="上报设备")
    engine.expect_did("WRITE", "主动上报使能标志D005", 传感器类型="未知", 上报命令="上报设备")
    engine.send_did("READ", "主动上报使能标志D005")
    engine.expect_did("READ", "主动上报使能标志D005", 传感器类型="通断", 上报命令="上报设备")

    engine.send_did("WRITE", "主动上报使能标志D005", 传感器类型="未知", 上报命令="同时上报设备和网关")
    engine.expect_did("WRITE", "主动上报使能标志D005", 传感器类型="未知", 上报命令="同时上报设备和网关")
    engine.send_did("READ", "主动上报使能标志D005")
    engine.expect_did("READ", "主动上报使能标志D005", 传感器类型="通断", 上报命令="同时上报设备和网关")

def test_日期C010():
    """
    06_日期C010
    1、设置不同的日期，测试均可以设置成功
    """
    engine.add_doc_info('设置日期为2024年2月29日')
    engine.send_did("WRITE", "日期C010", '29 02 24')
    engine.expect_did("WRITE", "日期C010", '29 02 24')

    engine.add_doc_info('设置日期为2021年1月1日')
    engine.send_did("WRITE", "日期C010", '01 01 21')
    engine.expect_did("WRITE", "日期C010", '01 01 21')


    nowDate = time.strftime("%d %m %y", time.localtime())
    engine.add_doc_info('设置日期为当前日期')
    engine.send_did("WRITE", "日期C010", nowDate)
    engine.expect_did("WRITE", "日期C010", nowDate)

def test_时刻C011():
    """
    07_时刻C011
    1、设置不同的时刻，测试均可以设置成功
    """
    engine.add_doc_info('设置时间为23:59:50')
    engine.send_did("WRITE", "时刻C011", '50 59 23')
    engine.expect_did("WRITE", "时刻C011", '50 59 23')

    engine.add_doc_info('设置时间为00:59:50')
    engine.send_did("WRITE", "时刻C011", '50 59 00')
    engine.expect_did("WRITE", "时刻C011", '50 59 00')

    nowTime = time.strftime("%S %M %H", time.localtime())
    engine.add_doc_info('设置时间为当前')
    engine.send_did("WRITE", "时刻C011", nowTime)
    engine.expect_did("WRITE", "时刻C011", nowTime)

def test_面板锁定E014():
    """
    08_面板锁定E014
    1、将智能交互终端设置为锁定状态，查询设置成功
    2、将智能交互终端断电重启，再次查询，仍处于锁定状态
    3、将智能交互终端设置为解锁状态，查询设置成功
    """
    engine.send_did("WRITE", "面板锁定E014", "01")
    engine.expect_did("WRITE", "面板锁定E014", "01")
    engine.send_did("READ", "面板锁定E014", "")
    engine.expect_did("READ", "面板锁定E014", "01")

    power_control()
    engine.send_did("READ", "面板锁定E014", "")
    engine.expect_did("READ", "面板锁定E014", "01")

    engine.send_did("WRITE", "面板锁定E014", "00")
    engine.expect_did("WRITE", "面板锁定E014", "00")
    engine.send_did("READ", "面板锁定E014", "")
    engine.expect_did("READ", "面板锁定E014", "00")

def test_错误类报文测试():
    """
    09_错误类报文测试
    1、数据格式错误，返回错误字00 03（C0 12的数据长度为2，而发送命令中的长度为3）
    2、数据域少一个字节，返回错误字00 01数据域长度错误
    3、发送不存在的数据项FB20，返回错误字00 04数据项不存在
    """
    engine.add_doc_info("1、数据格式错误，返回错误字00 03（C0 60的数据长度为2，而发送命令中的长度为3）")

    engine.send_did("WRITE", "继电器上电状态C060", "01 02 03")
    engine.expect_did("WRITE", "继电器上电状态C060", "03 00")

    engine.add_doc_info("2、数据域少一个字节，返回错误字00 01数据域长度错误")
    engine.send_raw("07 05 D0 02 03")
    engine.expect_did("WRITE", "主动上报使能标志D005", "01 00")

    engine.add_doc_info("3、发送不存在的数据项FB20，返回错误字00 04数据项不存在")
    engine.send_did("READ", "读取或设置被控设备端的控制地址FB20", "01")
    engine.expect_did("READ", "读取或设置被控设备端的控制地址FB20", "04 00")


def test_参数修改后断电验证():
    """
    10_参数修改后断电验证
    1、将参数配置成与默认参数不一致；
    2、断电重启，测试参数是否丢失；
    3、将参数设置回默认参数，便于后续的测试项目运行
    """
    # 继电器上电状态C060为00上电状态为上电断开
    engine.send_did("WRITE", "继电器上电状态C060", "00")
    engine.expect_did("WRITE", "继电器上电状态C060", "00")
    # 主动上报使能标志D005设置为01 上报网关
    engine.send_did("WRITE", "主动上报使能标志D005", 传感器类型="未知", 上报命令="上报网关")
    engine.expect_did("WRITE", "主动上报使能标志D005", 传感器类型="未知", 上报命令="上报网关")
    # 将设备设置为锁定模式
    engine.send_did("WRITE", "面板锁定E014", "01")
    engine.expect_did("WRITE", "面板锁定E014", "01")


    # 断电重启，然后查询参数和断电前一致
    power_control()

    engine.send_did("READ", "继电器上电状态C060")
    engine.expect_did("READ", "继电器上电状态C060", "00")
    engine.send_did("READ", "主动上报使能标志D005")
    engine.expect_did("READ", "主动上报使能标志D005", 传感器类型="通断", 上报命令="上报网关")
    engine.send_did("READ", "面板锁定E014", "")
    engine.expect_did("READ", "面板锁定E014", "01")

    # 将修改后的参数，设置回默认参数
    engine.send_did("WRITE", "通断操作C012", "01")
    engine.expect_did("WRITE", "通断操作C012", "00")
    engine.send_did("WRITE", "继电器上电状态C060", "02")
    engine.expect_did("WRITE", "继电器上电状态C060", "02")
    engine.send_did("WRITE", "主动上报使能标志D005", 传感器类型="未知", 上报命令="同时上报设备和网关")
    engine.expect_did("WRITE", "主动上报使能标志D005", 传感器类型="未知", 上报命令="同时上报设备和网关")
    engine.send_did("WRITE", "面板锁定E014", "00")
    engine.expect_did("WRITE", "面板锁定E014", "00")


def test_chuankou():
    """
    test
    """
    def test_chuankou(data):
        if data == '01' :
            return True

        else:
            return False
    engine.send_local_msg("查询透传模式", '')
    result = engine.expect_local_msg("回复透传模式",test_chuankou)
    engine.add_doc_info(result)
    # if test_chuankou:
    #     engine.add_doc_info('将当前的串口波特率为9600，将其设置为115200')
    #     engine.send_local_msg("设置串口波特率", '04 00') # 115200bps
    #     engine.expect_local_msg("确认")
    #     config["波特率"] = "115200"
    #     engine.send_did("READ", "面板锁定E014", "")
    #     engine.expect_did("READ", "面板锁定E014", "00")

