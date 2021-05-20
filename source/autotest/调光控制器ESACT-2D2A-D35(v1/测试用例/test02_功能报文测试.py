# encoding:utf-8
from .常用测试模块 import *
import engine

测试组说明 = "功能类报文测试"

channel_dict = {1: '01', 2: '02'}  # 设备通道及对应值


def test_出厂默认参数():
    """
    01_默认出厂参数测试
    1、出厂第一次继电器默认为断开00 通断操作C012
    2、断电后默认上电状态为02上电状态为上次断电状态 继电器上电状态C060
    3、继电器过零保护出厂为3路，可分别设置，默认断开延时5.1ms，默认闭合延时5.7ms 07 33 39 33 39 33 39 继电器过零点动作延迟时间C020
    4、状态同步默认状态03同时上报设备和网关 主动上报使能标志D005
    5、触摸开关默认控制的设备AID为自身的AID 读取或设置被控设备端的控制地址FB20
    6、面板的默认背光亮度为1% 读写面板默认背光亮度百分比C135
    """
    engine.add_doc_info("升级前读取默认参数")
    engine.send_did("READ", "线性调光时间C0A3", "01")
    engine.expect_did("READ", "线性调光时间C0A3", "01 05")
    engine.send_did("READ", "线性调光时间C0A3", "02")
    engine.expect_did("READ", "线性调光时间C0A3", "02 05")
    engine.send_did("READ", "查询设置通道的起始亮度C0A4", "01")
    engine.expect_did("READ", "查询设置通道的起始亮度C0A4", "01 28")
    engine.send_did("READ", "查询设置通道的起始亮度C0A4", "02")
    engine.expect_did("READ", "查询设置通道的起始亮度C0A4", "02 28")
    engine.send_did("READ", "查询设置超温保护温度上限C0A5", "01")
    engine.expect_did("READ", "查询设置超温保护温度上限C0A5", "01 64")
    engine.send_did("READ", "查询设置超温保护温度上限C0A5", "02")
    engine.expect_did("READ", "查询设置超温保护温度上限C0A5", "02 64")
    engine.send_did("READ", "设置调光曲线C0A6", "01")
    engine.expect_did("READ", "设置调光曲线C0A6", "01 01")
    engine.send_did("READ", "设置调光曲线C0A6", "02")
    engine.expect_did("READ", "设置调光曲线C0A6", "02 01")

    engine.send_did("READ", "主动上报使能标志D005")
    engine.expect_did("READ", "主动上报使能标志D005", "00 03")


def test_通断操作C012():
    """
    02_通断操作C012
    1、查询当前通断状态00
    2、打开通道，然后查询当前通断状态，监测器输出监测正常；
    3、关闭通道，然后查询当前通断状态，监测器输出监测正常；
    """
    engine.send_did("READ", "通断操作C012", "")
    engine.expect_did("READ", "通断操作C012", "00")

    engine.add_doc_info("通道1控制通断测试")
    relay_output_test(did="通断操作C012", relay_channel=1, output_channel=[0])

    engine.add_doc_info("通道2控制通断测试")
    relay_output_test(did="通断操作C012", relay_channel=2, output_channel=[1])

    engine.add_doc_info("2个通道同时控制通断测试")
    relay_output_test(did="通断操作C012", relay_channel=3, output_channel=[0, 1])


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

    engine.add_doc_info('通道2控制翻转测试')
    relay_output_test(did="继电器翻转C018", relay_channel=2, output_channel=[1])

    engine.add_doc_info('2个通道同时控制翻转测试')
    relay_output_test(did="继电器翻转C018", relay_channel=3, output_channel=[0, 1])


def test_超过保护温度关灯并上报C0A0():
    """
    04_超过保护温度关灯并上报C0A0
    1.读取1通道当前温度；
    2.读取2通道当前温度；
    :return:
    """
    engine.add_doc_info("测试步骤说明：读取所有（2）通道温度")       # 设备回复的温度是动态值
    engine.send_did("READ", "超过保护温度关灯并上报C0A0", "01")
    engine.expect_did("READ", "超过保护温度关灯并上报C0A0", "01 28")
    engine.send_did("READ", "超过保护温度关灯并上报C0A0", "02")
    engine.expect_did("READ", "超过保护温度关灯并上报C0A0", "02 21")


def test_保险丝断后上报C0A1():
    """
    05_保险丝断后上报C0A1;
    1.读取所有通道保险丝状态；
    :return:
    """
    engine.add_doc_info("测试步骤说明：读取所有（2）通道保险丝断后上报C0A1")
    engine.send_did("READ", "保险丝断后上报C0A1", "01")
    # engine.wait(0.5)
    engine.expect_did("READ", "保险丝断后上报C0A1", "01 00")
    engine.send_did("READ", "保险丝断后上报C0A1", "02")
    # engine.wait(0.5)
    engine.expect_did("READ", "保险丝断后上报C0A1", "02 00")


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


def test_亮度值C0A2():
    """
    07_亮度值C0A2;
    1.读写两通道亮度
    2.先读取通道状态，再依次写入亮度00,0A,32,64,00;
    3.调光过程需要一定的时间，增加延时读取0.5s
    :return:
    """
    engine.add_doc_info("测试步骤说明：读写-1通道-亮度值C0A2")
    engine.send_did("WRITE", "亮度值C0A2", "01 00")
    engine.expect_did("WRITE", "亮度值C0A2", "01 00 00")
    engine.wait(5)
    engine.send_did("READ", "亮度值C0A2", "01")
    engine.expect_did("READ", "亮度值C0A2", "01 00 00")
    engine.send_did("WRITE", "亮度值C0A2", "01 0A")
    engine.expect_did("WRITE", "亮度值C0A2", "01 0A 00")
    engine.wait(5)
    engine.send_did("READ", "亮度值C0A2", "01")
    engine.expect_did("READ", "亮度值C0A2", "01 0A 0A")
    engine.send_did("WRITE", "亮度值C0A2", "01 32")
    engine.expect_did("WRITE", "亮度值C0A2", "01 32 0A")
    engine.wait(5)
    engine.send_did("READ", "亮度值C0A2", "01")
    engine.expect_did("READ", "亮度值C0A2", "01 32 32")
    engine.send_did("WRITE", "亮度值C0A2", "01 64")
    engine.expect_did("WRITE", "亮度值C0A2", "01 64 32")
    engine.wait(5)
    engine.send_did("READ", "亮度值C0A2", "01")
    engine.expect_did("READ", "亮度值C0A2", "01 64 64")
    engine.send_did("WRITE", "亮度值C0A2", "01 00")
    engine.expect_did("WRITE", "亮度值C0A2", "01 00 64")
    engine.wait(5)

    engine.add_doc_info("测试步骤说明：读写-2通道-亮度值C0A2")
    engine.send_did("WRITE", "亮度值C0A2", "02 00")
    engine.expect_did("WRITE", "亮度值C0A2", "02 00 00")
    engine.wait(5)
    engine.send_did("READ", "亮度值C0A2", "02")
    engine.expect_did("READ", "亮度值C0A2", "02 00 00")
    engine.send_did("WRITE", "亮度值C0A2", "02 0A")
    engine.expect_did("WRITE", "亮度值C0A2", "01 0A 00")
    engine.wait(5)
    engine.send_did("READ", "亮度值C0A2", "02")
    engine.expect_did("READ", "亮度值C0A2", "02 0A 0A")
    engine.send_did("WRITE", "亮度值C0A2", "02 32")
    engine.expect_did("WRITE", "亮度值C0A2", "02 32 0A")
    engine.wait(5)
    engine.send_did("READ", "亮度值C0A2", "02")
    engine.expect_did("READ", "亮度值C0A2", "02 32 32")
    engine.send_did("WRITE", "亮度值C0A2", "02 64")
    engine.expect_did("WRITE", "亮度值C0A2", "02 64 32")
    engine.wait(5)
    engine.send_did("READ", "亮度值C0A2", "02")
    engine.expect_did("READ", "亮度值C0A2", "02 64 64")
    engine.send_did("WRITE", "亮度值C0A2", "02 00")
    engine.expect_did("WRITE", "亮度值C0A2", "02 00 64")


def test_线性调光时间C0A3():
    """
    08_线性调光时间C0A3;
    1.读写两通道线性调光时间
    2.先读取通道线性调光时间，再依次写入线性调光时间0A,05;
    :return:
    """
    engine.add_doc_info("测试步骤说明：读写-1通道-线性调光时间C0A3")
    engine.send_did("READ", "线性调光时间C0A3", "01")
    engine.expect_did("READ", "线性调光时间C0A3", "01 05")
    engine.send_did("WRITE", "线性调光时间C0A3", "01 00")
    engine.expect_did("WRITE", "线性调光时间C0A3", "01 00")
    engine.send_did("WRITE", "线性调光时间C0A3", "01 0A")
    engine.expect_did("WRITE", "线性调光时间C0A3", "01 0A")
    engine.send_did("WRITE", "线性调光时间C0A3", "01 05")
    engine.expect_did("WRITE", "线性调光时间C0A3", "01 05")
    engine.send_did("READ", "线性调光时间C0A3", "01")
    engine.expect_did("READ", "线性调光时间C0A3", "01 05")

    engine.add_doc_info("测试步骤说明：读写-2通道-线性调光时间C0A3")
    engine.send_did("READ", "线性调光时间C0A3", "02")
    engine.expect_did("READ", "线性调光时间C0A3", "02 05")
    engine.send_did("WRITE", "线性调光时间C0A3", "02 00")
    engine.expect_did("WRITE", "线性调光时间C0A3", "02 00")
    engine.send_did("WRITE", "线性调光时间C0A3", "02 0A")
    engine.expect_did("WRITE", "线性调光时间C0A3", "02 0A")
    engine.send_did("WRITE", "线性调光时间C0A3", "02 05")
    engine.expect_did("WRITE", "线性调光时间C0A3", "02 05")
    engine.send_did("READ", "线性调光时间C0A3", "02")
    engine.expect_did("READ", "线性调光时间C0A3", "02 05")


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


def test_查询设置通道的起始亮度C0A4():
    """
    10_查询设置通道的起始亮度C0A4;
    1.读写两通道起始亮度
    2.先读取通道起始亮度，再依次写入起始亮度32,64,28;
    :return:
    """
    engine.add_doc_info("测试步骤说明：读写-1通道-起始亮度C0A4")
    engine.send_did("READ", "查询设置通道的起始亮度C0A4", "01")
    engine.expect_did("READ", "查询设置通道的起始亮度C0A4", "01 28")
    engine.send_did("WRITE", "查询设置通道的起始亮度C0A4", "01 32")
    engine.expect_did("WRITE", "查询设置通道的起始亮度C0A4", "01 32")
    engine.send_did("WRITE", "查询设置通道的起始亮度C0A4", "01 64")
    engine.expect_did("WRITE", "查询设置通道的起始亮度C0A4", "01 64")
    engine.send_did("READ", "查询设置通道的起始亮度C0A4", "01")
    engine.expect_did("READ", "查询设置通道的起始亮度C0A4", "01 64")
    engine.send_did("WRITE", "查询设置通道的起始亮度C0A4", "01 28")
    engine.expect_did("WRITE", "查询设置通道的起始亮度C0A4", "01 28")

    engine.add_doc_info("测试步骤说明：读写-2通道-起始亮度C0A4")
    engine.send_did("READ", "查询设置通道的起始亮度C0A4", "02")
    engine.expect_did("READ", "查询设置通道的起始亮度C0A4", "02 28")
    engine.send_did("WRITE", "查询设置通道的起始亮度C0A4", "02 32")
    engine.expect_did("WRITE", "查询设置通道的起始亮度C0A4", "02 32")
    engine.send_did("WRITE", "查询设置通道的起始亮度C0A4", "02 64")
    engine.expect_did("WRITE", "查询设置通道的起始亮度C0A4", "02 64")
    engine.send_did("READ", "查询设置通道的起始亮度C0A4", "02")
    engine.expect_did("READ", "查询设置通道的起始亮度C0A4", "02 64")
    engine.send_did("WRITE", "查询设置通道的起始亮度C0A4", "02 28")
    engine.expect_did("WRITE", "查询设置通道的起始亮度C0A4", "02 28")


def test_查询设置超温保护温度上限C0A5():
    """
    11_查询设置超温保护温度上限C0A5;
    1.读写两通道超温保护温度上限C0A5
    2.先读取通道超温保护温度上限，再依次写入超温保护温度上限32,4B,64;
    :return:
    """
    engine.add_doc_info("测试步骤说明：读写-1通道-起始亮度C0A5")
    engine.send_did("READ", "查询设置超温保护温度上限C0A5", "01")
    engine.expect_did("READ", "查询设置超温保护温度上限C0A5", "01 64")
    engine.send_did("WRITE", "查询设置超温保护温度上限C0A5", "01 32")
    engine.expect_did("WRITE", "查询设置超温保护温度上限C0A5", "01 32")
    engine.send_did("WRITE", "查询设置超温保护温度上限C0A5", "01 4B")
    engine.expect_did("WRITE", "查询设置超温保护温度上限C0A5", "01 4B")
    engine.send_did("READ", "查询设置超温保护温度上限C0A5", "01")
    engine.expect_did("READ", "查询设置超温保护温度上限C0A5", "01 4B")
    engine.send_did("WRITE", "查询设置超温保护温度上限C0A5", "01 64")
    engine.expect_did("WRITE", "查询设置超温保护温度上限C0A5", "01 64")

    engine.add_doc_info("测试步骤说明：读写-2通道-起始亮度C0A5")
    engine.send_did("READ", "查询设置超温保护温度上限C0A5", "02")
    engine.expect_did("READ", "查询设置超温保护温度上限C0A5", "02 64")
    engine.send_did("WRITE", "查询设置超温保护温度上限C0A5", "02 32")
    engine.expect_did("WRITE", "查询设置超温保护温度上限C0A5", "02 32")
    engine.send_did("WRITE", "查询设置超温保护温度上限C0A5", "02 4B")
    engine.expect_did("WRITE", "查询设置超温保护温度上限C0A5", "02 4B")
    engine.send_did("READ", "查询设置超温保护温度上限C0A5", "02")
    engine.expect_did("READ", "查询设置超温保护温度上限C0A5", "02 4B")
    engine.send_did("WRITE", "查询设置超温保护温度上限C0A5", "02 64")
    engine.expect_did("WRITE", "查询设置超温保护温度上限C0A5", "02 64")


def test_自定义调光曲线C0A7():         # 需要确定曲线范围
    """
    12_自定义调光曲线;
    1.读写两通道自定义调光曲线C0A7;
    2.先读取通道自定义调光曲线，再依次写入自定义调光曲线;
    3.曲线共100个点，分多次读取（一条报文长度不足）
    :return:
    """
    engine.add_doc_info("测试步骤说明：读写-1通道-自定义调光曲线")
    engine.send_did("READ", "自定义调光曲线", "01 01 01")
    engine.expect_did("READ", "自定义调光曲线", "01 01 01 59 00")      # 01-通道号；01-调光起始；01-调光曲线块号；59 00-曲线上的第一个点
    engine.send_did("WRITE", "自定义调光曲线", "01 01 01 60 00")
    engine.expect_did("WRITE", "自定义调光曲线", "01 01 01 60 00")
    engine.send_did("READ", "自定义调光曲线", "01 01 01")
    engine.expect_did("READ", "自定义调光曲线", "01 01 01 60 00")
    engine.send_did("WRITE", "自定义调光曲线", "01 01 01 59 00")
    engine.expect_did("WRITE", "自定义调光曲线", "01 01 01 59 00")
    engine.send_did("READ", "自定义调光曲线", "01 01 01")
    engine.expect_did("READ", "自定义调光曲线", "01 01 01 59 00")

    engine.add_doc_info("测试步骤说明：读写-2通道-自定义调光曲线")
    engine.send_did("READ", "自定义调光曲线", "02 01 01")
    engine.expect_did("READ", "自定义调光曲线", "02 01 01 59 00")
    engine.send_did("WRITE", "自定义调光曲线", "02 01 01 60 00")
    engine.expect_did("WRITE", "自定义调光曲线", "02 01 01 60 00")
    engine.send_did("READ", "自定义调光曲线", "02 01 01")
    engine.expect_did("READ", "自定义调光曲线", "02 01 01 60 00")
    engine.send_did("WRITE", "自定义调光曲线", "02 01 01 59 00")
    engine.expect_did("WRITE", "自定义调光曲线", "02 01 01 59 00")
    engine.send_did("READ", "自定义调光曲线", "02 01 01")
    engine.expect_did("READ", "自定义调光曲线", "02 01 01 59 00")


def test_设置指定通道增加或降低亮度C0AA():
    """
    13_设置指定通道增加或降低亮度C0AA;
    1.写入最低亮度C0A2-01/02 00,作为调光起始值；
    2.使用通道增加或降低亮度C0AA，单步调节亮度;
    3.读取单步调节后的亮度值；
    :return:
    """
    engine.add_doc_info("测试步骤说明：读写-1通道-增加亮度")
    engine.send_did("WRITE", "亮度值C0A2", "01 00")     # 配置亮度00，作为调节起始点
    engine.expect_did("WRITE", "亮度值C0A2", "01 00 00")
    engine.send_did("WRITE", "设置指定通道增加或降低亮度C0AA", "01 01")
    engine.expect_did("WRITE", "设置指定通道增加或降低亮度C0AA", "01 01")
    engine.wait(5)
    engine.send_did("READ", "亮度值C0A2", "01")
    engine.expect_did("READ", "亮度值C0A2", "01 01 01")
    engine.send_did("WRITE", "设置指定通道增加或降低亮度C0AA", "01 01")
    engine.expect_did("WRITE", "设置指定通道增加或降低亮度C0AA", "01 01")
    engine.wait(5)
    engine.send_did("READ", "亮度值C0A2", "01")
    engine.expect_did("READ", "亮度值C0A2", "01 22 22")
    engine.send_did("WRITE", "设置指定通道增加或降低亮度C0AA", "01 01")
    engine.expect_did("WRITE", "设置指定通道增加或降低亮度C0AA", "01 01")
    engine.wait(5)
    engine.send_did("READ", "亮度值C0A2", "01")
    engine.expect_did("READ", "亮度值C0A2", "01 43 43")
    engine.send_did("WRITE", "设置指定通道增加或降低亮度C0AA", "01 01")
    engine.expect_did("WRITE", "设置指定通道增加或降低亮度C0AA", "01 01")
    engine.wait(5)
    engine.send_did("READ", "亮度值C0A2", "01")
    engine.expect_did("READ", "亮度值C0A2", "01 64 64")

    engine.add_doc_info("测试步骤说明：读写-1通道-降低亮度")
    engine.send_did("WRITE", "亮度值C0A2", "01 64")
    engine.expect_did("WRITE", "亮度值C0A2", "01 64 64")
    engine.send_did("WRITE", "设置指定通道增加或降低亮度C0AA", "01 00")
    engine.expect_did("WRITE", "设置指定通道增加或降低亮度C0AA", "01 00")
    engine.wait(5)
    engine.send_did("READ", "亮度值C0A2", "01")
    engine.expect_did("READ", "亮度值C0A2", "01 43 43")
    engine.send_did("WRITE", "设置指定通道增加或降低亮度C0AA", "01 00")
    engine.expect_did("WRITE", "设置指定通道增加或降低亮度C0AA", "01 00")
    engine.wait(5)
    engine.send_did("READ", "亮度值C0A2", "01")
    engine.expect_did("READ", "亮度值C0A2", "01 22 22")
    engine.send_did("WRITE", "设置指定通道增加或降低亮度C0AA", "01 00")
    engine.expect_did("WRITE", "设置指定通道增加或降低亮度C0AA", "01 00")
    engine.wait(5)
    engine.send_did("READ", "亮度值C0A2", "01")
    engine.expect_did("READ", "亮度值C0A2", "01 01 01")
    engine.send_did("WRITE", "设置指定通道增加或降低亮度C0AA", "01 00")
    engine.expect_did("WRITE", "设置指定通道增加或降低亮度C0AA", "01 00")
    engine.wait(5)
    engine.send_did("READ", "亮度值C0A2", "01")
    engine.expect_did("READ", "亮度值C0A2", "01 00 00")


def test_通道按键操作():      # 试验代码
    """
    1. 打开上报
    2. 配置初始亮度为00
    3. 手动增加亮度
       - 按一下应为1%，步长33%，直到100%；状态改变后上报两次，第二次的当前目标亮度一致。
    4. 手动减少亮度按一下应为67%，34%，1%，0%，步长33%。状态改变后上报两次，第二次的当前目标亮度一致。
    5. 重置亮度为0%
    6. 关闭上报
    :return:
    """
    engine.report_check_enable_all(True)

    engine.add_doc_info('test_通道按键操作-测试步骤1：设置通道一初始亮度0%')
    engine.send_did('WRITE', '亮度值C0A2', '01 00 00')
    engine.wait(1)
    engine.expect_did('WRITE', '亮度值C0A2', '01 00 00')

    engine.add_doc_info('test_通道按键操作-测试步骤2：设置通道一亮度1%,34%,67%,100%')
    for i in range(4):
        engine.set_device_sensor_status("可控硅输出", channel=1)     # 试验代码---控制可控硅输出
        twice_report_chack(channel=1)

    engine.add_doc_info('test_通道按键操作-测试步骤2：设置通道二亮度1%,34%,67%,100%')
    for i in range(4):
        engine.set_device_sensor_status("可控硅输出", channel=2)     # 试验代码---控制可控硅输出
        twice_report_chack(channel=2)