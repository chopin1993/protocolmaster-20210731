# encoding:utf-8
import engine
from autotest.公共用例.public常用测试模块 import *
from .常用测试模块 import *

测试组说明 = "功能类报文测试"


def test_出厂默认参数():
    """
    01_默认出厂参数测试
    1、默认工作模式为只上报网关01
    2、默认温湿度补偿参数为94 00 默认温度补偿-2摄氏度，湿度补偿0
    3、默认的心跳时间为1E 默认心跳时间为30min
    4、默认的红外补偿参数为2D 80 默认红外补偿时间为-45us
    """
    read_default_configuration()


def test_红外功能学习0901():
    """
    02_红外功能学习0901
    码库编号默认为0，按键编号只能为0001~FFFE，0000与FFFF按照数据项格式不正确错误字处理。
    1、发送支持配置的按键编号，如1，783，65534，测试配置学习正常，学习时间为6s；
    2、发送红外功能学习报文成功后，设备进行学习模式，此时再次收到配置报文，均会回复错误字0005设备忙；
    3、发送不支持配置的按键编号，如0,65535，测试按照数据项格式不正确错误字0003进行处理；
    """
    engine.add_doc_info('1、发送支持配置的按键编号，如1，783，65534，测试配置学习正常，学习时间为6s；')
    for value in [1, 783, 65534]:
        engine.send_did('WRITE', '红外功能学习0901', 码库值=0, 键值=value)
        engine.expect_did('WRITE', '红外功能学习0901', 码库值=0, 键值=value)
        engine.wait(10, tips='红外学习过程为6s，保持充分的间隔')

    engine.add_doc_info('2、发送红外功能学习报文成功后，设备进行学习模式，此时再次收到配置报文，均会回复错误字0005设备忙；')
    engine.send_did('WRITE', '红外功能学习0901', 码库值=0, 键值=1)
    engine.expect_did('WRITE', '红外功能学习0901', 码库值=0, 键值=1)
    engine.wait(2)
    engine.add_doc_info('等待2s，设备仍处于红外学习模式，此时再次发送相同键值学习报文，回复0005设备忙')
    engine.send_did('WRITE', '红外功能学习0901', 码库值=0, 键值=1)
    engine.expect_did('WRITE', '红外功能学习0901', '05 00')
    engine.wait(2)
    engine.add_doc_info('等待2s，设备仍处于红外学习模式，此时再次发送不同键值学习报文，回复0005设备忙')
    engine.send_did('WRITE', '红外功能学习0901', 码库值=0, 键值=10000)
    engine.expect_did('WRITE', '红外功能学习0901', '05 00')
    engine.wait(2 + 1)
    engine.add_doc_info('等待2s，设备退出红外学习模式，此时再次发送不同键值学习报文，测试配置学习模式正常')
    engine.send_did('WRITE', '红外功能学习0901', 码库值=0, 键值=10000)
    engine.expect_did('WRITE', '红外功能学习0901', 码库值=0, 键值=10000)
    engine.wait(10, tips='红外学习过程为6s，保持充分的间隔')

    engine.add_doc_info('3、发送不支持配置的按键编号，如0,65535，测试按照数据项格式不正确错误字0003进行处理；')
    for value in [0, 65535]:
        engine.send_did('WRITE', '红外功能学习0901', 码库值=0, 键值=value)
        engine.expect_did('WRITE', '红外功能学习0901', '03 00')


def test_红外直接发送0902():
    """
    03_红外直接发送0902
    1、发送不支持的键值，如0,65535，测试按照数据项格式不正确错误字0003进行处理；
    2、发送未学习的键值，如256,512，均会回复错误字000F1其他错；
    3、发送已学习的键值，如1，4127，65534，均红外发送正常；（因为出厂默认传感器是未学习状态，所以本项需要人工补测）；
    """
    engine.add_doc_info('1、发送不支持的键值，如0,65535，测试按照数据项格式不正确错误字0003进行处理；')
    for value in [0, 65535]:
        engine.send_did('WRITE', '红外直接发送0902', 码库值=0, 键值=value)
        engine.expect_did('WRITE', '红外直接发送0902', '03 00')

    engine.add_doc_info('2、发送未学习的键值，如256,512，均会回复错误字000F1其他错；')
    for value in [256, 512]:
        engine.send_did('WRITE', '红外直接发送0902', 码库值=0, 键值=value)
        engine.expect_did('WRITE', '红外直接发送0902', '0F 00')

    engine.add_doc_info('3、发送已学习的键值，如1，4127，65534，均红外发送正常；'
                        '（因为出厂默认传感器是未学习状态，所以本项需要人工补测）；')

    for value in [1, 4127, 65534]:
        engine.send_did('WRITE', '红外直接发送0902', 码库值=0, 键值=value)
        engine.expect_did('WRITE', '红外直接发送0902', 码库值=0, 键值=value)


def test_传感器数据B691():
    """
    04_传感器数据B691
    1、分别支持的传感器类型；温度、湿度，要求上报均正常；
    2、查询不支持的传感器类型，如未知，有无人，均回复0003格式不正确；
    """
    engine.add_doc_info('1、分别支持的传感器类型；温度03、湿度04，要求上报均正常；')
    for value in ['03', '04']:
        engine.send_did('READ', '传感器数据B691', value)
        engine.expect_did('READ', '传感器数据B691', value + ' ** **')
    engine.add_doc_info('2、查询不支持的传感器类型，如未知00，有无人09，均回复0003格式不正确；')
    for value in ['00', '09']:
        engine.send_did('READ', '传感器数据B691', value)
        engine.expect_did('READ', '传感器数据B691', '03 00')


def test_主动上报使能标志D005():
    """
    05_主动上报使能标志D005
    TT为传感器类型，XX 为0x00:无上报；0x01：上报网关；0x02：上报设备；0x03 同时上报设备和网关（状态同步的普遍使用方案）；
    1、查询被测设备的默认工作模式为01 上报网关
    2、设置不支持的工作模式，如0x02：上报设备；0x03同时上报设备和网关，测试回复0003格式不正确，设备内参数不变；
    3、设置不支持的传感器类型，如00未知、人体红外移动09，测试回复0003格式不正确，设备内参数不变；
    4、设置支持的工作模式和传感器类型，测试设置正常；
    """
    engine.add_doc_info("1、查询被测设备的默认工作模式为01 上报网关")
    engine.send_did("READ", "主动上报使能标志D005", "")
    engine.expect_did("READ", "主动上报使能标志D005", 传感器类型="温度", 上报命令="上报网关")

    engine.add_doc_info('2、设置不支持的工作模式，如0x02：上报设备；0x03同时上报设备和网关，测试回复0003格式不正确，设备内参数不变；')
    for mode in ['上报设备', '同时上报设备和网关']:
        engine.send_did("WRITE", "主动上报使能标志D005", 传感器类型="温度", 上报命令=mode)
        engine.expect_did("WRITE", "主动上报使能标志D005", '03 00')
        engine.send_did("READ", "主动上报使能标志D005")
        engine.expect_did("READ", "主动上报使能标志D005", 传感器类型="温度", 上报命令="上报网关")

    engine.add_doc_info('3、设置不支持的传感器类型，如00未知、人体红外移动09，测试回复0003格式不正确，设备内参数不变；')
    for sensor in ['未知', '人体红外移动']:
        engine.send_did("WRITE", "主动上报使能标志D005", 传感器类型=sensor, 上报命令="无上报")
        engine.expect_did("WRITE", "主动上报使能标志D005", '03 00')
        engine.send_did("READ", "主动上报使能标志D005")
        engine.expect_did("READ", "主动上报使能标志D005", 传感器类型="温度", 上报命令="上报网关")

    engine.add_doc_info('4、设置支持的工作模式和传感器类型，测试设置正常；')
    for sensor in ['温度', '湿度']:
        for mode in ['无上报', '上报网关']:
            engine.send_did("WRITE", "主动上报使能标志D005", 传感器类型=sensor, 上报命令=mode)
            engine.expect_did("WRITE", "主动上报使能标志D005", 传感器类型=sensor, 上报命令=mode)
            engine.send_did("READ", "主动上报使能标志D005", '')
            engine.expect_did("READ", "主动上报使能标志D005", 传感器类型="温度", 上报命令=mode)


def test_心跳时间D101():
    """
    06_心跳时间D101
    1、查询默认的心跳时间为1E 默认心跳时间为30min
    2、设置不同的心跳时间，如0,100,255，30，测试均可以设置成功并进行查询验证；
    """
    engine.add_doc_info('1、查询默认的心跳时间为1E 默认心跳时间为30min')
    engine.send_did('READ', '心跳时间D101', '')
    engine.expect_did('READ', '心跳时间D101', 心跳时间=30)

    engine.add_doc_info('2、设置不同的心跳时间，如0,100,255，30，测试均可以设置成功并进行查询验证；')
    for value in [0, 100, 255, 30]:
        engine.send_did('WRITE', '心跳时间D101', 心跳时间=value)
        engine.expect_did('WRITE', '心跳时间D101', 心跳时间=value)
        engine.send_did('READ', '心跳时间D101', '')
        engine.expect_did('READ', '心跳时间D101', 心跳时间=value)


def test_温湿度补偿参数FF08():
    """
    07_温湿度补偿参数FF08
    1、查询默认温湿度补偿参数为94 00 默认温度补偿-2摄氏度，湿度补偿0
    2、修改不同的温湿度补偿参数，测试设置是否成功，并进行验证
    """
    engine.add_doc_info('1、查询默认温湿度补偿参数为94 00 默认温度补偿-2摄氏度，湿度补偿0')
    engine.send_did('READ', '温湿度补偿参数FF08', '')
    engine.expect_did('READ', '温湿度补偿参数FF08', '94 00')

    engine.add_doc_info('2、修改不同的温湿度补偿参数，测试设置是否成功，并进行验证')
    for value in ['00 00', '14 14', '94 94', '94 00']:
        engine.send_did('WRITE', '温湿度补偿参数FF08', value)
        engine.expect_did('WRITE', '温湿度补偿参数FF08', value)
        engine.send_did('READ', '温湿度补偿参数FF08', '')
        engine.expect_did('READ', '温湿度补偿参数FF08', value)


def test_传感器数据补偿D107():
    """
    08_传感器数据补偿D107
    补偿时间范围-127到127之间，补偿时间为负数ZZ最高位置1
    1、查询默认的红外补偿参数为2D 80 默认红外补偿时间为-45us
    2、修改不同的红外补偿参数，测试设置是否成功，并进行验证
    """
    engine.add_doc_info('1、查询默认的红外补偿参数为2D 80 默认红外补偿时间为-45us')
    engine.send_did('READ', '传感器数据补偿D107', '1F')
    engine.expect_did('READ', '传感器数据补偿D107', '1F 2D 80')

    engine.add_doc_info('2、修改不同的红外补偿参数，测试设置是否成功，并进行验证')
    for value in ['00 00', '7F 80', '7F 00', '2D 80']:
        engine.send_did('WRITE', '传感器数据补偿D107', '1F ' + value)
        engine.expect_did('WRITE', '传感器数据补偿D107', '1F ' + value)
        if value == '00 00':
            engine.add_doc_info('当时设置补偿参数为00 00时，再次进行查询，实际回复的参数为00 80，此处进行特殊处理')
            value = '00 80'
        engine.send_did('READ', '传感器数据补偿D107', '1F')
        engine.expect_did('READ', '传感器数据补偿D107', '1F ' + value)


def test_错误类报文测试():
    """
    09_错误类报文测试
    1、数据格式错误，返回错误字00 03（C0 12的数据长度为2，而发送命令中的长度为3）
    2、数据域少一个字节，返回错误字00 01数据域长度错误
    3、发送不存在的数据项FB20，返回错误字00 04数据项不存在
    """
    engine.add_doc_info("1、数据格式错误，返回错误字C0 30（C0 30的数据长度为2，而发送命令中的长度为3）")
    engine.send_did("WRITE", "设置密码C030", "01 02 03")
    engine.expect_did("WRITE", "设置密码C030", "03 00")

    engine.add_doc_info("2、数据域少一个字节，返回错误字00 01数据域长度错误")
    engine.add_doc_info('本种错误由载波适配层判断并直接回复，所以SWB总线是监控不到的')
    engine.send_raw("07 05 D0 02 03")
    engine.expect_did("WRITE", "主动上报使能标志D005", "01 00")

    engine.add_doc_info("3、发送不存在的数据项，返回错误字00 04数据项不存在")
    engine.send_did("READ", "总有功电能9010", "")
    engine.expect_did("READ", "总有功电能9010", "04 00")


def test_断电验证参数测试():
    """
    10_断电验证参数测试
    1、将被测设备的参数配置成与默认参数不一致；
    2、断电重启，测试参数是否丢失；
    3、将所有参数设置回默认参数，便于后续的测试项目运行
    """
    engine.add_doc_info(
        """
        修改默认参数，使其与默认参数不一致
        1、工作模式修改为无上报00
        2、温湿度补偿参数修改为14 10 温度补偿2摄氏度，湿度补偿1.6%
        3、心跳时间修改为0x20=32min 
        4、红外补偿参数修改为2D 80  红外补偿时间为16us
        """)

    engine.add_doc_info('1、修改默认参数，使其与默认参数不一致')
    modify_default_configuration(modify=True, verify=True)

    engine.add_doc_info('2、控制被测设备断电重启，然后查询参数和断电前一致，说明断电测试不影响设置参数')
    power_control()
    modify_default_configuration(modify=False, verify=True)

    engine.add_doc_info('3、测试完毕，将所有的参数恢复出厂设置，并断电验证所有的参数均恢复出厂设置')
    engine.send_did('WRITE', '主动上报使能标志D005', '03 01')
    engine.expect_did('WRITE', '主动上报使能标志D005', '03 01')
    engine.send_did('WRITE', '心跳时间D101', '1E')
    engine.expect_did('WRITE', '心跳时间D101', '1E')
    engine.send_did('WRITE', '温湿度补偿参数FF08', '94 00')
    engine.expect_did('WRITE', '温湿度补偿参数FF08', '94 00')
    engine.send_did('WRITE', '传感器数据补偿D107', '1F 2D 80')
    engine.expect_did('WRITE', '传感器数据补偿D107', '1F 2D 80')
    read_default_configuration()

    engine.add_doc_info('断电重启，再次进行出厂默认参数的验证，便于后续的测试项目运行')
    power_control()
    read_default_configuration()
    engine.wait(20, '本部分测试用例测试结束，预留20s测试间隔')
