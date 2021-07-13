# encoding:utf-8
from autotest.公共用例.public常用测试模块 import *
from .常用测试模块 import *

测试组说明 = "功能类报文测试"


def test_出厂默认参数():
    """
    01_默认出厂参数测试
    1、传感器无效时间60s
    2、滑动窗口时间5s
    3、工作模式:09  01上报网关
    4、上报网关模式，有无人定频默认0s，默认关闭，步长上报默认1，默认开启
    5、上报网关模式，光照度定频0s，默认关闭，步长上报默认20 lux，默认开启
    6、传感器补偿参数   默认11%
    7、开关灯阈值   开灯:40,关灯60
    8、控制目标地址：空  数据域为 00 01 FF FF FF FF 00
    """
    read_default_configuration()


def test_传感器无效时间D702():
    """
    02_传感器无效时间D702
    1、传感器器无效时间默认为60s，并进行查询验证
    2、测试设置不同的传感器无效时间，如60s、120s、180s均可以设置成功；
    3、测试设置不允许的传感器无效时间，如0s、59s，设备回复成功，实际按照60s作为最小时间；
    4、测试设置回默认的无效时间60s
    """
    engine.add_doc_info('1、传感器器无效时间默认为60s，并进行查询验证')
    engine.send_did('READ', '传感器无效时间D702', '')
    engine.expect_did('READ', '传感器无效时间D702', 60)

    engine.add_doc_info('2、测试设置不同的传感器无效时间，如60s、120s、180s均可以设置成功；')
    for value in [60, 180, 300]:
        engine.send_did('WRITE', '传感器无效时间D702', 无效时间=value)
        engine.expect_did('WRITE', '传感器无效时间D702', 无效时间=value)
        engine.send_did('READ', '传感器无效时间D702', '')
        engine.expect_did('READ', '传感器无效时间D702', 无效时间=value)

    engine.add_doc_info('3、测试设置不允许的传感器无效时间，如0s、59s，设备回复格式不正确，实际按照60s作为最小时间保存')
    for value in [0, 30, 59]:
        engine.send_did('WRITE', '传感器无效时间D702', 无效时间=value)
        engine.expect_did('WRITE', '传感器无效时间D702', '03 00')
        engine.send_did('READ', '传感器无效时间D702', '')
        engine.expect_did('READ', '传感器无效时间D702', 无效时间=300)

    engine.add_doc_info('4、测试设置回默认的无效时间60s')
    engine.send_did('WRITE', '传感器无效时间D702', 无效时间=60)
    engine.expect_did('WRITE', '传感器无效时间D702', 无效时间=60)
    engine.send_did('READ', '传感器无效时间D702', '')
    engine.expect_did('READ', '传感器无效时间D702', 无效时间=60)


def test_上报间隔设置D004():
    """
    03_上报间隔设置D004
    1、查询默认的滑动窗口时间5s,限定值：5~65535s
    2、测试设置不被允许的滑差时间(要求大于5s)，如0s、4s，或者不同的传感器类型，验证均不可以设置成功；
    3、测试设置不同的滑差时间，如60s，180s，300s，5s，验证均可以设置成功；
    """
    engine.add_doc_info('1、查询默认的滑动窗口时间5s')
    engine.send_did('READ', '上报间隔设置D004', '09')
    engine.expect_did('READ', '上报间隔设置D004', '09 05 00')

    engine.add_doc_info('2、测试设置不被允许的滑差时间(要求大于5s)，如0s、4s，验证均不可以设置成功')
    for value in [0, 4]:
        engine.send_did('WRITE', '上报间隔设置D004', 传感器类型='人体红外移动', 滑差时间=value)
        engine.expect_did('WRITE', '上报间隔设置D004', '03 00')
        engine.send_did('READ', '上报间隔设置D004', 传感器类型='人体红外移动')
        engine.expect_did('READ', '上报间隔设置D004', 传感器类型='人体红外移动', 滑差时间=5)
    engine.add_doc_info('设置不符合的传感器类型，验证不可以设置成功')
    for sensor_type in ['红外百分比', '照度']:
        engine.send_did('WRITE', '上报间隔设置D004', 传感器类型=sensor_type, 滑差时间=60)
        engine.expect_did('WRITE', '上报间隔设置D004', '03 00')
        engine.send_did('READ', '上报间隔设置D004', 传感器类型='人体红外移动')
        engine.expect_did('READ', '上报间隔设置D004', 传感器类型='人体红外移动', 滑差时间=5)

    engine.add_doc_info('3、测试设置不同的滑差时间，如60s，1800s，5s，验证均可以设置成功；')
    for value in [60, 1800, 5]:
        engine.send_did('WRITE', '上报间隔设置D004', 传感器类型='人体红外移动', 滑差时间=value)
        engine.expect_did('WRITE', '上报间隔设置D004', 传感器类型='人体红外移动', 滑差时间=value)
        engine.send_did('READ', '上报间隔设置D004', 传感器类型='人体红外移动')
        engine.expect_did('READ', '上报间隔设置D004', 传感器类型='人体红外移动', 滑差时间=value)


def test_上报频率D104():
    """
    04_上报频率D104
    1、刚出厂的状态下，有无人定频默认0s，光照度定频默认0s；限定值：0,10~65535s
    2、测试设置不被允许的时间，如1s，9s，测试验证均不可以设置成功，查询上报频率不变；
    3、测试不同传感器设置不同的定频上报时间，然后查询验证时间正常；
    """
    engine.add_doc_info('1、刚出厂的状态下，有无人定频默认0s，光照度定频默认0s；')
    for sensor_type in ['人体红外移动', '照度']:
        engine.send_did('READ', '上报频率D104', 传感器类型=sensor_type)
        engine.expect_did('READ', '上报频率D104', 传感器类型=sensor_type, 定频=0)

    engine.add_doc_info('2、测试设置不被允许的时间，如1s，9s，测试验证均不可以设置成功；')
    for value in [1, 9]:
        for sensor_type in ['人体红外移动', '照度']:
            engine.send_did('WRITE', '上报频率D104', 传感器类型=sensor_type, 定频=value)
            engine.expect_did('WRITE', '上报频率D104', '03 00')
            engine.send_did('READ', '上报频率D104', 传感器类型=sensor_type)
            engine.expect_did('READ', '上报频率D104', 传感器类型=sensor_type, 定频=0)

    engine.add_doc_info('3、测试不同传感器设置不同的定频上报时间，然后查询验证时间正常；')
    for value in [60, 1800, 0]:
        for sensor_type in ['人体红外移动', '照度']:
            engine.send_did('WRITE', '上报频率D104', 传感器类型=sensor_type, 定频=value)
            engine.expect_did('WRITE', '上报频率D104', 传感器类型=sensor_type, 定频=value)
            engine.send_did('READ', '上报频率D104', 传感器类型=sensor_type)
            engine.expect_did('READ', '上报频率D104', 传感器类型=sensor_type, 定频=value)


def test_上报步长D103():
    """
    05_上报步长D103
    1、刚出厂的状态下，有无人步长默认1，光照度步长默认20lux；限定值：0,10~299lux
    2、测试设置不被允许的步长值，如1lux，9lux，测试验证均不可以设置成功，查询上报步长不变；
    3、测试不同传感器设置不同的上报步长，然后查询验证时间正常；
    """
    engine.add_doc_info('1、刚出厂的状态下，有无人步长默认1，光照度步长默认20lux；')
    engine.send_did('READ', '上报步长D103', '09')
    engine.expect_did('READ', '上报步长D103', '09 01')
    engine.send_did('READ', '上报步长D103', '0B')
    engine.expect_did('READ', '上报步长D103', '0B 20 00')

    engine.add_doc_info('2、测试设置不被允许的步长值，如9lux，300lux，测试验证均不可以设置成功，查询上报步长不变')
    engine.add_doc_info('测试有无人传感器')
    for value in ['02', '99']:
        engine.send_did('WRITE', '上报步长D103', 传感器类型='人体红外移动', 步长=value)
        engine.expect_did('WRITE', '上报步长D103', '03 00')
        engine.send_did('READ', '上报步长D103', 传感器类型='人体红外移动')
        engine.expect_did('READ', '上报步长D103', 传感器类型='人体红外移动', 步长='01')
    engine.add_doc_info('测试光照度传感器')
    for value in ['09 00', '00 03']:
        engine.send_did('WRITE', '上报步长D103', '0B ' + value)
        engine.expect_did('WRITE', '上报步长D103', '03 00')
        engine.send_did('READ', '上报步长D103', '0B')
        engine.expect_did('READ', '上报步长D103', '0B 20 00')

    engine.add_doc_info('3、测试不同传感器设置不同的上报步长，然后查询验证时间正常；')
    engine.add_doc_info('测试有无人传感器')
    for value in ['00', '01']:
        engine.send_did('WRITE', '上报步长D103', 传感器类型='人体红外移动', 步长=value)
        engine.expect_did('WRITE', '上报步长D103', 传感器类型='人体红外移动', 步长=value)
        engine.send_did('READ', '上报步长D103', 传感器类型='人体红外移动')
        engine.expect_did('READ', '上报步长D103', 传感器类型='人体红外移动', 步长=value)

    engine.add_doc_info('测试光照度传感器')
    for value in ['10 00', '99 02', '20 00']:
        engine.send_did('WRITE', '上报步长D103', '0B ' + value)
        engine.expect_did('WRITE', '上报步长D103', '0B ' + value)
        engine.send_did('READ', '上报步长D103', '0B')
        engine.expect_did('READ', '上报步长D103', '0B ' + value)


def test_主动上报使能标志D005():
    """
    06_主动上报使能标志D005
    TT为传感器类型，XX 为0x00:无上报；0x01：上报网关；0x02：上报设备；0x03同时上报设备和网关（状态同步的普遍使用方案）；
    1、查询被测设备的默认状态同步使能参数为工作模式:09  01上报网关
    2、设置不同的工作模式0x02：本地联动；0x05：报警模式；01上报网关，并进行查询验证
    """
    engine.add_doc_info("1、查询被测设备的默认状态同步使能参数为工作模式:09  01上报网关")
    engine.send_did("READ", "主动上报使能标志D005", "")
    engine.expect_did("READ", "主动上报使能标志D005", '09 01')

    engine.add_doc_info("2、设置不同的工作模式0x02：本地联动；0x05：报警模式；0x01：上报网关并进行查询验证")
    for mode in ['上报设备', '报警模式', '上报网关']:
        engine.send_did('WRITE', '主动上报使能标志D005', 传感器类型='人体红外移动', 上报命令=mode)
        engine.expect_did('WRITE', '主动上报使能标志D005', 传感器类型='人体红外移动', 上报命令=mode)
        engine.send_did("READ", "主动上报使能标志D005", "")
        engine.expect_did("READ", "主动上报使能标志D005", 传感器类型='人体红外移动', 上报命令=mode)


def test_传感器数据补偿百分比D106():
    """
    07_传感器数据补偿百分比D106
    1、刚出厂的状态下，传感器补偿百分比参数：默认11%,此值一般不会改动； 限定值：0~99%
    2、测试不在范围内不支持的传感器补偿百分比，回复82 03 00 然后查询设置不生效，仍是11%；
    3、测试不同的传感器补偿百分比(允许范围0-99)，然后查询设置生效正常；
    """
    engine.add_doc_info('1、刚出厂的状态下，传感器补偿百分比参数：默认11%,此值一般不会改动；')
    engine.send_did('READ', '传感器数据补偿百分比D106', '0B')
    engine.expect_did('READ', '传感器数据补偿百分比D106', '0B 11')

    engine.add_doc_info('2、测试不在范围内不支持的传感器补偿百分比，回复82 03 00 然后查询设置不生效，仍是11%；')
    engine.add_doc_info('测试设置错误的传感器类型：')
    for value in ['03 20', '04 20', '09 20']:
        engine.send_did('WRITE', '传感器数据补偿百分比D106', value)
        engine.expect_did('WRITE', '传感器数据补偿百分比D106', '03 00')
        engine.send_did('READ', '传感器数据补偿百分比D106', '0B')
        engine.expect_did('READ', '传感器数据补偿百分比D106', '0B 11')
    engine.add_doc_info('测试设置错误的传感器百分比：')
    for value in ['0B 9A', '0B FF']:
        engine.send_did('WRITE', '传感器数据补偿百分比D106', value)
        engine.expect_did('WRITE', '传感器数据补偿百分比D106', '03 00')
        engine.send_did('READ', '传感器数据补偿百分比D106', '0B')
        engine.expect_did('READ', '传感器数据补偿百分比D106', '0B 11')

    engine.add_doc_info('3、测试不同的传感器补偿百分比，然后查询设置生效正常；')
    for value in ['0B 00', '0B 99', '0B 11']:
        engine.send_did('WRITE', '传感器数据补偿百分比D106', value)
        engine.expect_did('WRITE', '传感器数据补偿百分比D106', value)
        engine.send_did('READ', '传感器数据补偿百分比D106', '0B')
        engine.expect_did('READ', '传感器数据补偿百分比D106', value)


def test_传感器直接操作设备阀值D003():
    """
    08_传感器直接操作设备阀值D003
    1、查询出厂默认参数，开关灯阈值   开灯:40,关灯60  限定值：1~99%
    2、测试不符合规范的开关灯阈值；如开灯0关灯0、开灯50关灯100、开灯60大于关灯50，验证均不能设置成功，且参数不被修改；
    3、测试配置多种情况，如开灯1关灯99、开灯50关灯80、开灯40关灯60，然后查询设置生效正常；
    """
    engine.add_doc_info('1、查询出厂默认参数，开关灯阈值   开灯:40,关灯60 限定值：1~99%')
    engine.send_did('READ', '传感器直接操作设备阀值D003', '0B')
    engine.expect_did('READ', '传感器直接操作设备阀值D003', '0B 28 3C')

    engine.add_doc_info('2、测试不符合规范的开关灯阈值；如开灯0关灯0、开灯50关灯100、开灯大于关灯，'
                        '验证均不能设置成功，且参数不被修改；')
    for value in ['0B 00 00', '0B 32 64', '0B 3C 32']:
        engine.send_did('WRITE', '传感器直接操作设备阀值D003', value)
        engine.expect_did('WRITE', '传感器直接操作设备阀值D003', '03 00')
        engine.send_did('READ', '传感器直接操作设备阀值D003', '0B')
        engine.expect_did('READ', '传感器直接操作设备阀值D003', '0B 28 3C')

    engine.add_doc_info('3、测试配置多种情况，如开灯1关灯99、开灯50关灯80、开灯40关灯60，然后查询设置生效正常；')
    for value in ['0B 01 63', '0B 32 50', '0B 28 3C']:
        engine.send_did('WRITE', '传感器直接操作设备阀值D003', value)
        engine.expect_did('WRITE', '传感器直接操作设备阀值D003', value)
        engine.send_did('READ', '传感器直接操作设备阀值D003', '0B')
        engine.expect_did('READ', '传感器直接操作设备阀值D003', value)


def test_控制目的设备地址D006():
    """
    09_控制目的设备地址D006
    1、查询出厂默认参数，控制目标地址：空  数据域为 00 01 FF FF FF FF 00
    2、测试配置单个设备，并进行查询验证；
    3、测试配置多个设备，并进行查询验证；
    4、测试完毕，将配置参数还原默认配置 00 01 FF FF FF FF 00
    """

    engine.add_doc_info('1、查询出厂默认参数，控制目标地址：空  数据域为 00 01 FF FF FF FF 00')
    engine.send_did('READ', '控制目的设备地址D006', '')
    engine.expect_did('READ', '控制目的设备地址D006', '00 01 FF FF FF FF 00')

    engine.add_doc_info('2、测试配置单个设备，并进行查询验证；')
    engine.add_doc_info('3、测试配置多个设备，并进行查询验证；')
    engine.add_doc_info('4、测试完毕，将配置参数还原默认配置 00 01 FF FF FF FF 00')
    # 通过for循环，实现同时测试步骤2步骤3和步骤4
    for value in ['00 01 14 00 00 00 01',
                  '01 01 01 08 01 04 C6 03 02 05 05 06 01 02 06 01 04 C4 03 02 05 01 04 06 01 00 C0 03 05 05 01 08 06 01 00 C0 03 05 05',
                  '00 01 FF FF FF FF 00']:
        engine.send_did('WRITE', '控制目的设备地址D006', value)
        engine.expect_did('WRITE', '控制目的设备地址D006', value)
        engine.send_did('READ', '控制目的设备地址D006', '')
        engine.expect_did('READ', '控制目的设备地址D006', value)


def test_读传感器数据B701():
    """
    10_读传感器数据B701
    此处暂不支持SWB协议，无法设置传感器数值，所以对数据采用通配符*
    05红外百分比、09人体红外移动、0B照度
    1、查询当前的传感器数据 05红外百分比
    2、查询当前的传感器数据 09人体红外移动
    3、查询当前的传感器数据 0B照度
    """
    engine.add_doc_info('1、查询当前的传感器数据 05红外百分比')
    engine.send_did('READ', '读传感器数据B701', '05')
    engine.expect_did('READ', '读传感器数据B701', '05 **')

    engine.add_doc_info('2、查询当前的传感器数据 09人体红外移动')
    engine.send_did('READ', '读传感器数据B701', '09')
    engine.expect_did('READ', '读传感器数据B701', '09 **')

    engine.add_doc_info('3、查询当前的传感器数据 0B照度')
    engine.send_did('READ', '读传感器数据B701', '0B')
    engine.expect_did('READ', '读传感器数据B701', '0B ** **')


def test_错误类报文测试():
    """
    11_错误类报文测试
    1、数据格式错误，返回错误字00 03（C0 12的数据长度为2，而发送命令中的长度为3）
    2、数据域少一个字节，返回错误字00 01数据域长度错误
    3、发送不存在的数据项FB20，返回错误字00 04数据项不存在
    """
    engine.add_doc_info("1、数据格式错误，返回错误字00 03（D1 04的数据长度为1，而发送命令中的长度为3）")
    engine.send_did("WRITE", "上报频率D104", "01 02 03")
    engine.expect_did("WRITE", "上报频率D104", "03 00")

    engine.add_doc_info("2、数据域少一个字节，返回错误字00 01数据域长度错误")
    engine.add_doc_info('本种错误由载波适配层判断并直接回复，所以SWB总线是监控不到的')
    engine.send_raw("07 05 D0 02 03")
    engine.expect_did("WRITE", "主动上报使能标志D005", "01 00")

    engine.add_doc_info("3、发送不存在的数据项，返回错误字00 04数据项不存在")
    engine.send_did("READ", "总有功电能9010", "")
    engine.expect_did("READ", "总有功电能9010", "04 00")


def test_断电参数测试():
    """
    12_断电参数测试
    1、将被测设备的参数配置成与默认参数不一致；
    2、断电重启，测试参数是否丢失；验证断电前后，参数保持不变；
    3、恢复出厂默认参数并进行验证，便于后续的测试项目运行；
    4、再次断电重启，查看恢复出厂后的参数仍然正常；
    """

    engine.add_doc_info('1、将被测设备的参数配置成与默认参数不一致，并进行查询验证；')
    modify_default_configuration(modify=True, verify=True)

    engine.add_doc_info('2、断电重启，测试参数是否丢失；验证断电前后，参数保持不变；')
    power_control()
    modify_default_configuration(modify=False, verify=True)

    engine.add_doc_info('3、恢复出厂默认参数并进行验证，便于后续的测试项目运行')
    return_to_factory()
    read_default_configuration()

    engine.add_doc_info('4、再次断电重启，查看恢复出厂后的参数仍然正常；')
    power_control()
    read_default_configuration()
