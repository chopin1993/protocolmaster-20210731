# encoding:utf-8
import engine
from autotest.公共用例.public常用测试模块 import *
from .常用测试模块 import *

测试组说明 = "功能类报文测试"

channel_dict = {1: '01'}  # 设备通道及对应值


def rcv_data_no_check(data):
    return True


def test_出厂默认参数():
    """
    01_默认出厂参数测试
    1、出厂第一次继电器默认为断开00 通断操作C012
    2、过压欠压跳闸阈值B511，过压：264.0(V)，欠压：176.0(V)
    3、过流跳闸阈值B521，此设备有两个版本32A(32A过流),和63A(63A过流)
    4、状态同步默认状态01同时上报网关 主动上报使能标志D005
    5、过流过欠压功率保护使能标识B624,默认关闭01打开
    6、本地按键使能C008，使能默认01开启
    """
    engine.send_did("READ", "通断操作C012", "")
    engine.expect_did("READ", "通断操作C012", "00")

    engine.send_did("READ", "过压欠压跳闸阈值B511")
    engine.expect_did("READ", "过压欠压跳闸阈值B511", "00 40 26 60 17")

    if config["被测设备硬件版本"] == "63A版本":
        engine.send_did('READ', '过流跳闸阈值B521', '')
        engine.expect_did('READ', '过流跳闸阈值B521', '00 00 30 06')
    else:   # config["被测设备硬件版本"] == "32A版本":
        engine.send_did('READ', '过流跳闸阈值B521', '')
        engine.expect_did('READ', '过流跳闸阈值B521', '00 00 20 03')

    engine.send_did('READ', '过流过欠压功率保护使能标识B624', '')
    engine.expect_did('READ', '过流过欠压功率保护使能标识B624', '01')

    engine.send_did('READ', '上报频率D104', '')
    engine.expect_did('READ', '上报频率D104', '0C 00 00')

    engine.send_did('READ', '上报步长D103', '')
    engine.expect_did('READ', '上报步长D103', '0C 00 00')

    engine.send_did("READ", "主动上报使能标志D005")
    engine.expect_did("READ", "主动上报使能标志D005", "00 03")

    engine.send_did("READ", "电压B611", '')
    engine.expect_did("READ", "电压B611", "** 2*")

    engine.send_did("READ", "本地按键使能C008")
    engine.expect_did("READ", "本地按键使能C008", "01")

    engine.send_did("READ", "A相电流B621")
    engine.expect_did("READ", "A相电流B621", "** ** **")

    engine.send_did("READ", "瞬时总功率B630")
    engine.expect_did("READ", "瞬时总功率B630", "** ** **")

    engine.send_did("READ", "总有功电能9010")
    engine.expect_did("READ", "总有功电能9010", "** ** ** **")

    # 继电器过零保护用例待完善！


def test_通断操作C012():
    """
    02_通断操作C012
    1、关闭所有通道；
    2、查询当前通断状态00；
    3、打开通道，然后查询当前通断状态，监测器输出监测正常；
    4、关闭通道，然后查询当前通断状态，监测器输出监测正常；
    """
    engine.send_did("WRITE", "通断操作C012", "01")
    engine.expect_did("WRITE", "通断操作C012", "00")

    engine.send_did("READ", "通断操作C012", "")
    engine.expect_did("READ", "通断操作C012", "00")

    engine.add_doc_info("通道1控制通断测试")
    relay_output_test(did="通断操作C012", relay_channel=1, output_channel=[0])


def test_继电器翻转C018():
    """
    03_继电器翻转C018
    bit5~bit0:1/0表示通道操作/不操作；bit0表示第1个通道，回复时按C012报文格式回复
    1、查询当前通断状态00关闭
    2、继电器翻转，然后查询当前通断状态，监测器输出监测正常；
    3、继电器翻转，然后查询当前通断状态，监测器输出监测正常；
    """
    engine.send_did("READ", "通断操作C012", "")
    engine.expect_did("READ", "通断操作C012", "00")

    engine.add_doc_info('通道1控制翻转测试')
    relay_output_test(did="继电器翻转C018", relay_channel=1, output_channel=[0])


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


def test_错误类报文测试():
    """
    10_错误类报文测试
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
    engine.send_did("READ", "颜色值C040", "")
    engine.expect_did("READ", "颜色值C040", "04 00")
