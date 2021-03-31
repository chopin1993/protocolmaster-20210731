# encoding:utf-8
from autotest.公共用例.public常用测试模块 import *
from .常用测试模块 import *

测试组说明 = "功能类报文测试"


def test_出厂默认参数():
    """
    01_默认出厂参数测试
    1、出厂状态同步默认为03同时上报设备和网关  主动上报使能标志D005
    2、出厂默认继电器断开延时为1.4ms，闭合延时为3.6ms  继电器过零点动作延迟时间C020
    3、出厂默认行程时间为00 00 00 00  单轨电机窗帘上升下降行程时间0A02
    4、出厂默认保险栓开关状态为00关闭  保险栓开关状态0A06
    5、出厂默认保险栓使能状态为00禁用  保险栓功能使能标识0A30
    6、出厂默认窗帘天空模型使能为00禁用  窗帘天空模型配置0A0A
    7、出厂默认天空模型强制校准次数为30次  窗帘天空模型强制校准次数0A0B
    8、出厂默认窗帘校准后动作次数为0次  窗帘校准后动作次数0A0C

    """
    read_default_configuration()


def test_主动上报使能标志D005():
    """
    02_主动上报使能标志D005
    TT为传感器类型，XX 为0x00:无上报；0x01：上报网关；0x02：上报设备；0x03同时上报设备和网关（状态同步的普遍使用方案）；
    1、查询被测设备的默认状态同步使能参数为0x03同时上报设备和网关；
    2、设置不同的传感器类型，均可以设置成功，说明执行器类设备不判断传感器类型仅识别上报属性配置；
    3、设置不支持的工作模式，如0x04:平台控制；0x05：报警模式，均不能设置，再次查询配置信息未改变；
    4、设置不同的工作模式0x00:无上报；0x01：上报网关；0x02：上报设备；0x03:同时上报设备和网关，并进行查询验证
    """
    engine.add_doc_info("1、查询被测设备的默认状态同步使能参数为0x03同时上报设备和网关；")
    engine.send_did("READ", "主动上报使能标志D005", '')
    engine.expect_did("READ", "主动上报使能标志D005", '00 03')

    engine.add_doc_info("2、设置不同的传感器类型，均可以设置成功，说明执行器类设备不判断传感器类型仅识别上报属性配置；")
    for sensor in ['温度', '湿度', '未知']:
        engine.send_did('WRITE', '主动上报使能标志D005', 传感器类型=sensor, 上报命令='上报网关')
        engine.expect_did('WRITE', '主动上报使能标志D005', 传感器类型=sensor, 上报命令='上报网关')
        engine.send_did("READ", "主动上报使能标志D005", "")
        engine.expect_did("READ", "主动上报使能标志D005", 传感器类型='未知', 上报命令='上报网关')

    engine.add_doc_info("3、设置不支持的工作模式，如0x04:平台控制；0x05：报警模式，均不能设置，再次查询配置信息未改变；")
    for mode in ['平台控制', '报警模式']:
        engine.send_did('WRITE', '主动上报使能标志D005', 传感器类型='未知', 上报命令=mode)
        engine.expect_did('WRITE', '主动上报使能标志D005', '03 00')
        engine.send_did("READ", "主动上报使能标志D005", "")
        engine.expect_did("READ", "主动上报使能标志D005", 传感器类型='未知', 上报命令='上报网关')

    engine.add_doc_info("4、设置不同的工作模式0x00:无上报；0x01：上报网关；0x02：上报设备；0x03:同时上报设备和网关，并进行查询验证")
    for mode in ['无上报', '上报网关', '上报设备', '同时上报设备和网关']:
        engine.send_did('WRITE', '主动上报使能标志D005', 传感器类型='未知', 上报命令=mode)
        engine.expect_did('WRITE', '主动上报使能标志D005', 传感器类型='未知', 上报命令=mode)
        engine.send_did("READ", "主动上报使能标志D005", "")
        engine.expect_did("READ", "主动上报使能标志D005", 传感器类型='未知', 上报命令=mode)


def test_继电器过零点动作延迟时间C020():
    """
    03_继电器过零点动作延迟时间C020
    xx(通道)xx（继电器断开延迟时间ms）xx（继电器闭合延迟时间）
    1、查询开关控制模块的默认参数:出厂默认继电器断开延时为1.4ms，闭合延时为3.6ms；
    2、测试设置不同的继电器过零点动作延迟时间C020，要求均可以设置成功；
    """
    engine.add_doc_info("1、查询开关控制模块的默认参数:出厂默认继电器断开延时为1.4ms，闭合延时为3.6ms；01 0E 24")
    engine.send_did("READ", "继电器过零点动作延迟时间C020", "01")
    engine.expect_did("READ", "继电器过零点动作延迟时间C020", "01 0E 24")

    engine.add_doc_info("2、测试设置不同的继电器过零点动作延迟时间C020，要求均可以设置成功；")
    for value in ['01 00 00', '01 20 21', '01 0E 24']:
        engine.send_did("WRITE", "继电器过零点动作延迟时间C020", value)
        engine.expect_did("WRITE", "继电器过零点动作延迟时间C020", value)
        engine.send_did("READ", "继电器过零点动作延迟时间C020", "01")
        engine.expect_did("READ", "继电器过零点动作延迟时间C020", value)


def test_电机转动0A01():
    """
    04_电机转动0A01
    本数据标识0A01，主要是通过时间控制窗帘动作，时间范围为0-180s,超过180s的时间按照180s进行计时。正转输出接通道0，反转输出接通道1
    1、分别测试暂停、正转、反转等3个指令，测试下列步骤：暂停-正转-暂停-反转-正转-反转-暂停，测试窗帘控制模块运行正常；
    2、分别测试不同的电机运行时间，如0s，20s，120s，180s，测试窗帘控制模块运行正常；
    3、分别测试超过180s的电机运行时间，如300s，最大值0xFFFF = 6553.5s，测试均按照180s进行计时运行；
    """
    engine.add_doc_info('1、分别测试暂停、正转、反转等3个指令，测试步骤：暂停-正转-暂停-反转-正转-反转-暂停，测试窗帘控制模块运行正常；')
    engine.add_doc_info('测试不同的切换方式：暂停切换正转、暂停切换反转、正转切换反转、正转切换暂停、反转切换暂停、反转切换正转等6种情况')

    for key, value in enumerate(['暂停', '正转', '暂停', '反转', '正转', '反转', '暂停']):
        engine.send_did("WRITE", "电机转动0A01", 电机类型='交流电机', 电机状态=value, 转动时间=30 * 100)
        engine.expect_did("WRITE", "电机转动0A01", 电机类型='交流电机', 电机状态=value, 转动时间=30 * 100)
        engine.wait(1)
        if key == 4 or key == 5:
            engine.wait(1, tips='因为正转切换反转、反转切换正转用时约需1s,所以此处多等待1s')
        if value == '暂停':
            engine.expect_cross_zero_status(0, 0)
            engine.expect_cross_zero_status(1, 0)
        elif value == '正转':
            engine.expect_cross_zero_status(0, 1)
            engine.expect_cross_zero_status(1, 0)
        elif value == '反转':
            engine.expect_cross_zero_status(0, 0)
            engine.expect_cross_zero_status(1, 1)
        else:
            engine.add_doc_info('无效的电机状态')

    engine.add_doc_info('2、分别测试不同的电机运行时间，如0s，20s，120s，180s，测试窗帘控制模块运行正常；')
    for run_time in [0, 20, 120, 180]:
        engine.add_doc_info('测试电机运行时间为{}秒时，窗帘控制模块时间控制持续时间工作正常'.format(run_time))
        engine.send_did("WRITE", "电机转动0A01", 电机类型='交流电机', 电机状态='正转', 转动时间=run_time * 100)
        engine.expect_did("WRITE", "电机转动0A01", 电机类型='交流电机', 电机状态='正转', 转动时间=run_time * 100)

        if run_time == 0:
            engine.wait(2, tips='转动时间为0时，不需要验证窗帘模式持续时间')
        else:
            engine.wait(1)
            engine.expect_cross_zero_status(0, 1)
            engine.expect_cross_zero_status(1, 0)
            engine.wait((run_time - 1), tips='等待{}s后，检查此时仍处于正转状态'.format(run_time - 1))
            engine.expect_cross_zero_status(0, 1)
            engine.expect_cross_zero_status(1, 0)
        engine.wait(1, tips='等待{}s后，检查此时窗帘控制模块已断开供电'.format(run_time))
        engine.expect_cross_zero_status(0, 0)
        engine.expect_cross_zero_status(1, 0)

    engine.add_doc_info('3、分别测试超过180s的电机运行时间，如300s，500s,最大值0xFFFF = 655.35s，测试均按照180s进行计时运行；')
    for run_time in [300, 500, 655.35]:
        engine.add_doc_info('测试电机运行时间为{}秒时，窗帘控制模块实际供电持续时间为180s'.format(run_time))
        if run_time != 655.35:
            engine.send_did("WRITE", "电机转动0A01", 电机类型='交流电机', 电机状态='反转', 转动时间=run_time * 100)
            engine.expect_did("WRITE", "电机转动0A01", 电机类型='交流电机', 电机状态='反转', 转动时间=run_time * 100)
        else:
            engine.send_did("WRITE", "电机转动0A01", '00 03 FF FF')
            engine.expect_did("WRITE", "电机转动0A01", '00 03 FF FF')
        if run_time > 180:
            run_time = 180
        engine.wait(1)
        engine.expect_cross_zero_status(0, 0)
        engine.expect_cross_zero_status(1, 1)
        engine.wait((run_time - 1), tips='等待{}s后，检查此时仍处于反转状态'.format(run_time - 1))
        engine.expect_cross_zero_status(0, 0)
        engine.expect_cross_zero_status(1, 1)
        engine.wait(1, tips='等待{}s后，检查此时窗帘控制模块已断开供电'.format(run_time))
        engine.expect_cross_zero_status(0, 0)
        engine.expect_cross_zero_status(1, 0)


def test_单轨电机窗帘上升下降行程时间0A02():
    """
    05_单轨电机窗帘上升下降行程时间0A02
    1、出厂默认行程时间为00 00 00 00，在未设置行程时查询单轨窗帘目标开度0A03，窗帘模块会回复82 03 00；
    2、设置不同的行程时间，平台限定时间范围是5-120s，设备范围为5-180s，并进行查询验证；
    3、设置不符合时间范围的行程时间，要求回复82 03 00，并进行查询验证；
    4、行程时间无法设置00 00 00 00 ，可以通过CD00数据标识，进行恢复；
    """
    engine.add_doc_info('1、出厂默认行程时间为00 00 00 00，在未设置行程时查询单轨窗帘目标开度0A03，窗帘模块会回复82 03 00；')
    engine.send_did('READ', '单轨电机窗帘上升下降行程时间0A02', '')
    engine.expect_did('READ', '单轨电机窗帘上升下降行程时间0A02', '00 00 00 00')
    engine.send_did('READ', '单轨窗帘目标开度0A03', '')
    engine.expect_did('READ', '单轨窗帘目标开度0A03', '03 00')

    engine.add_doc_info('2、设置不同的行程时间，平台限定时间范围是5-120s，设备范围为5-180s，并进行查询验证；')
    engine.add_doc_info('设置上升行程和下降行程不一致的情况，并进行查询验证；如上升行程60s大于下降行程59s、上升行程60s小于下降行程61s')
    for value in ['70 17 0C 17', '70 17 D4 17']:
        engine.send_did('WRITE', '单轨电机窗帘上升下降行程时间0A02', value)
        engine.expect_did('WRITE', '单轨电机窗帘上升下降行程时间0A02', value)
        engine.send_did('READ', '单轨电机窗帘上升下降行程时间0A02', '')
        engine.expect_did('READ', '单轨电机窗帘上升下降行程时间0A02', value)

    engine.add_doc_info('备注：因为窗帘控制模块，正反转电压输出最长时间为180s，当行程时间为180s时，180*1.25=225s大于180s，实际输出180s后就会断电，'
                        '所以实际最长行程可设置时间 = 180/1.25=144s')
    for value in [5, 120, 144]:
        engine.send_did('WRITE', '单轨电机窗帘上升下降行程时间0A02', 上升行程=value * 100, 下降行程=value * 100)
        engine.expect_did('WRITE', '单轨电机窗帘上升下降行程时间0A02', 上升行程=value * 100, 下降行程=value * 100)
        engine.send_did('READ', '单轨电机窗帘上升下降行程时间0A02', '')
        engine.expect_did('READ', '单轨电机窗帘上升下降行程时间0A02', 上升行程=value * 100, 下降行程=value * 100)
        wait_time = value * 1.25  # 测试设置行程时间时，反转动作持续时间长度
        engine.wait(1, tips='反转开始时检测输出正常')
        engine.expect_cross_zero_status(0, 0)
        engine.expect_cross_zero_status(1, 1)
        engine.wait(wait_time - 1, tips='反转结束时，检测输出也正常')
        engine.expect_cross_zero_status(0, 0)
        engine.expect_cross_zero_status(1, 1)
        engine.wait(2)
        engine.expect_cross_zero_status(0, 0)
        engine.expect_cross_zero_status(1, 0)
        engine.send_did('READ', '单轨窗帘目标开度0A03', '')
        engine.expect_did('READ', '单轨窗帘目标开度0A03', 开度=0)
        engine.wait(10, tips='不同测试保持10s间隔')

    engine.add_doc_info('3、设置不符合时间范围的行程时间，要求回复82 03 00，并进行查询验证；')
    for value in [0, 4, 181]:
        engine.send_did('WRITE', '单轨电机窗帘上升下降行程时间0A02', 上升行程=value * 100, 下降行程=value * 100)
        engine.expect_did('WRITE', '单轨电机窗帘上升下降行程时间0A02', '03 00')
        engine.send_did('READ', '单轨电机窗帘上升下降行程时间0A02', '')
        engine.expect_did('READ', '单轨电机窗帘上升下降行程时间0A02', 上升行程=144 * 100, 下降行程=144 * 100)
    engine.add_doc_info('测试存在微小差距只差10ms时，4.99s = 499 =0x1F3,180.01s = 18001 =0x4651')
    for value in ['F3 01 F3 01', '51 46 51 46']:
        engine.send_did('WRITE', '单轨电机窗帘上升下降行程时间0A02', value)
        engine.expect_did('WRITE', '单轨电机窗帘上升下降行程时间0A02', '03 00')
        engine.send_did('READ', '单轨电机窗帘上升下降行程时间0A02', '')
        engine.expect_did('READ', '单轨电机窗帘上升下降行程时间0A02', 上升行程=144 * 100, 下降行程=144 * 100)

    engine.add_doc_info('4、行程时间无法设置00 00 00 00 ，可以通过CD00数据标识，进行恢复；')
    engine.send_did('WRITE', '复位等待时间CD00', '00')
    engine.expect_did('WRITE', '复位等待时间CD00', '00')
    engine.wait(5, tips='通过复位等待时间CD00恢复出厂，预留充足时间')
    engine.send_did('READ', '单轨电机窗帘上升下降行程时间0A02', '')
    engine.expect_did('READ', '单轨电机窗帘上升下降行程时间0A02', '00 00 00 00')


def test_单轨窗帘目标开度0A03():
    """
    06_单轨窗帘目标开度0A03
    本数据标识0A03，主要是通过开度控制窗帘动作
    1、默认出厂行程为00 00 00 00 时，查询单轨窗帘目标开度0A03，窗帘模块会回复82 03 00，
    在05_test_单轨电机窗帘上升下降行程时间0A02已验证,不再重复测试；
    2、设置行程时间为10s后，此时电机会反转10s*1.25 = 12.5s，查询单轨窗帘目标开度0A03默认为0
    3、分别设置开度为从小到大、从大到小2种情况：测试均可以设置成功，并且输出端运行正常；
    4、测试完毕，将行程时间恢复出厂参数00 00 00 00
    """
    engine.add_doc_info("1、默认出厂行程为00 00 00 00 时，查询单轨窗帘目标开度0A03，"
                        "窗帘模块会回复82 03 00，在05_test_单轨电机窗帘上升下降行程时间0A02已验证,不再重复测试；")

    engine.add_doc_info('2、设置行程时间为10s后，此时电机会反转10s*1.25 = 12.5s，查询单轨窗帘目标开度0A03默认为0')
    engine.send_did('WRITE', '单轨电机窗帘上升下降行程时间0A02', 上升行程=10 * 100, 下降行程=10 * 100)
    engine.expect_did('WRITE', '单轨电机窗帘上升下降行程时间0A02', 上升行程=10 * 100, 下降行程=10 * 100)
    engine.send_did('READ', '单轨电机窗帘上升下降行程时间0A02', '')
    engine.expect_did('READ', '单轨电机窗帘上升下降行程时间0A02', 上升行程=10 * 100, 下降行程=10 * 100)
    engine.add_doc_info('设置行程时间的时候，窗帘控制模块会反转至底部，控制器的控制时间比实际设置的时间增加了1/4')
    engine.wait(10 * 1.25, tips='等待设置行程时间，反转至底部，查询默认开度为0')
    engine.send_did('READ', '单轨窗帘目标开度0A03', '')
    engine.expect_did('READ', '单轨窗帘目标开度0A03', 开度=0)
    engine.wait(2, tips='本项测试结束，间隔2s')

    engine.add_doc_info('3、分别设置开度为从小到大、从大到小2种情况：测试均可以设置成功，并且输出端运行正常；')
    engine.add_doc_info('当前开度为0，测试开度从小到大，从0到100%的情况')
    for value in [30, 60, 90, 100]:
        engine.send_did('WRITE', '单轨窗帘目标开度0A03', 开度=value)
        engine.expect_did('WRITE', '单轨窗帘目标开度0A03', 开度=value)
        engine.wait(1)
        engine.expect_cross_zero_status(0, 1)
        engine.expect_cross_zero_status(1, 0)
        if value != 100:
            engine.wait(3 - 1, tips='行程时间为10s，从0到30%，到60%，到90%，各用时3s')
        else:
            engine.wait(3.5 - 1, tips='行程时间为10s，从90%到100%，用时1+10*0.25=3.5s')
        engine.expect_cross_zero_status(0, 1)
        engine.expect_cross_zero_status(1, 0)
        engine.wait(2, tips='行程时间结束，再次检测，输出端均为断开')
        engine.expect_cross_zero_status(0, 0)
        engine.expect_cross_zero_status(1, 0)
        engine.wait(2, tips='各项窗帘控制模块操作，间隔2s')

    engine.add_doc_info('当前开度为100，测试开度从大到小，从100%到0的情况')
    for value in [70, 40, 10, 0]:
        engine.send_did('WRITE', '单轨窗帘目标开度0A03', 开度=value)
        engine.expect_did('WRITE', '单轨窗帘目标开度0A03', 开度=value)
        engine.wait(1)
        engine.expect_cross_zero_status(0, 0)
        engine.expect_cross_zero_status(1, 1)
        if value != 0:
            engine.wait(3 - 1, tips='行程时间为10s，从100到70%，到40%，到10%，各用时3s')
        else:
            engine.wait(3.5 - 1, tips='行程时间为10s，从10%到0，用时1+10*0.25=3.5s')
        engine.expect_cross_zero_status(0, 0)
        engine.expect_cross_zero_status(1, 1)
        engine.wait(2, tips='行程时间结束，再次检测，输出端均为断开')
        engine.expect_cross_zero_status(0, 0)
        engine.expect_cross_zero_status(1, 0)
        engine.wait(2, tips='各项窗帘控制模块操作，间隔2s')

    engine.add_doc_info('4、测试完毕，将行程时间恢复出厂参数00 00 00 00')
    engine.send_did('WRITE', '复位等待时间CD00', '00')
    engine.expect_did('WRITE', '复位等待时间CD00', '00')
    engine.wait(5, tips='通过复位等待时间CD00恢复出厂，预留充足时间')
    engine.send_did('READ', '单轨电机窗帘上升下降行程时间0A02', '')
    engine.expect_did('READ', '单轨电机窗帘上升下降行程时间0A02', '00 00 00 00')


def test_电机转动0A04():
    """
    07_电机转动0A04
    本数据标识0A04，主要是通过开度控制窗帘动作，1表示暂停，2表示正转，3表示反转
    1、测试行程时间为0时，分别测试暂停、正转、反转等3个指令，测试步骤：暂停-正转-暂停-反转-正转-反转-暂停，测试窗帘控制模块运行正常；
    2、测试行程时间为20s时，分别测试暂停、正转、反转等3个指令，测试步骤：暂停-正转-暂停-反转-正转-反转-暂停，测试窗帘控制模块运行正常；
    """
    engine.add_doc_info('1、测试行程时间为0时，分别测试暂停、正转、反转等3个指令，测试步骤：暂停-正转-暂停-反转-正转-反转-暂停，测试窗帘控制模块运行正常；')
    engine.add_doc_info('测试不同的切换方式：暂停切换正转、暂停切换反转、正转切换反转、正转切换暂停、反转切换暂停、反转切换正转等6种情况')
    engine.send_did('READ', '单轨电机窗帘上升下降行程时间0A02', '')
    engine.expect_did('READ', '单轨电机窗帘上升下降行程时间0A02', '00 00 00 00')
    for key, value in enumerate(['暂停', '正转', '暂停', '反转', '正转', '反转', '暂停']):
        engine.send_did("WRITE", "电机转动0A04", 电机状态=value)
        engine.expect_did("WRITE", "电机转动0A04", 电机状态=value)
        engine.wait(1)
        if key == 4 or key == 5:
            engine.wait(1, tips='因为正转切换反转、反转切换正转用时约需1s,所以此处多等待1s')
        if value == '暂停':
            engine.expect_cross_zero_status(0, 0)
            engine.expect_cross_zero_status(1, 0)
        elif value == '正转':
            engine.expect_cross_zero_status(0, 1)
            engine.expect_cross_zero_status(1, 0)
        elif value == '反转':
            engine.expect_cross_zero_status(0, 0)
            engine.expect_cross_zero_status(1, 1)
        else:
            engine.add_doc_info('无效的电机状态')

    engine.wait(5, tips='测试完不同控制方式的切换均正常后，行程时间为0时，正转和反转的运行时间默认为180s')
    for key, value in enumerate(['正转', '反转']):
        engine.send_did("WRITE", "电机转动0A04", 电机状态=value)
        engine.expect_did("WRITE", "电机转动0A04", 电机状态=value)
        engine.wait(1)
        if value == '正转':
            engine.expect_cross_zero_status(0, 1)
            engine.expect_cross_zero_status(1, 0)
            engine.wait(180 - 1, tips='输出最长持续180s')
            engine.expect_cross_zero_status(0, 1)
            engine.expect_cross_zero_status(1, 0)
        elif value == '反转':
            engine.expect_cross_zero_status(0, 0)
            engine.expect_cross_zero_status(1, 1)
            engine.wait(180 - 1, tips='输出最长持续180s')
            engine.expect_cross_zero_status(0, 0)
            engine.expect_cross_zero_status(1, 1)

        engine.wait(2, tips='行程时间结束，再次检测，输出端均为断开')
        engine.expect_cross_zero_status(0, 0)
        engine.expect_cross_zero_status(1, 0)

    engine.add_doc_info('2、测试行程时间为20s时，分别测试暂停、正转、反转等3个指令，测试步骤：暂停-正转-暂停-反转-正转-反转-暂停，测试窗帘控制模块运行正常；')
    engine.add_doc_info('测试不同的切换方式：暂停切换正转、暂停切换反转、正转切换反转、正转切换暂停、反转切换暂停、反转切换正转等6种情况')
    engine.send_did('WRITE', '单轨电机窗帘上升下降行程时间0A02', 上升行程=20 * 100, 下降行程=20 * 100)
    engine.expect_did('WRITE', '单轨电机窗帘上升下降行程时间0A02', 上升行程=20 * 100, 下降行程=20 * 100)
    engine.send_did('READ', '单轨电机窗帘上升下降行程时间0A02', '')
    engine.expect_did('READ', '单轨电机窗帘上升下降行程时间0A02', 上升行程=20 * 100, 下降行程=20 * 100)
    engine.add_doc_info('设置行程时间的时候，窗帘控制模块会反转至底部，控制器的控制时间比实际设置的时间增加了1/4')
    engine.wait(20 * 1.25, tips='等待设置行程时间，反转至底部，查询默认开度为0')
    engine.send_did('READ', '单轨窗帘目标开度0A03', '')
    engine.expect_did('READ', '单轨窗帘目标开度0A03', 开度=0)
    engine.wait(5, tips='各项窗帘控制模块操作，间隔5s')

    for key, value in enumerate(['暂停', '正转', '暂停', '反转', '正转', '反转', '暂停']):
        engine.send_did("WRITE", "电机转动0A04", 电机状态=value)
        engine.expect_did("WRITE", "电机转动0A04", 电机状态=value)
        engine.wait(1)
        if key == 4 or key == 5:
            engine.wait(1, tips='因为正转切换反转、反转切换正转用时约需1s,所以此处多等待1s')
        if value == '暂停':
            engine.expect_cross_zero_status(0, 0)
            engine.expect_cross_zero_status(1, 0)
        elif value == '正转':
            engine.expect_cross_zero_status(0, 1)
            engine.expect_cross_zero_status(1, 0)
        elif value == '反转':
            engine.expect_cross_zero_status(0, 0)
            engine.expect_cross_zero_status(1, 1)
        else:
            engine.add_doc_info('无效的电机状态')

    engine.wait(5, tips='测试完不同控制方式的切换均正常后，行程时间为20s时，正转和反转的运行时间为20*1.25=25s')
    for key, value in enumerate(['正转', '反转']):
        engine.send_did("WRITE", "电机转动0A04", 电机状态=value)
        engine.expect_did("WRITE", "电机转动0A04", 电机状态=value)
        engine.wait(1)
        if value == '正转':
            engine.expect_cross_zero_status(0, 1)
            engine.expect_cross_zero_status(1, 0)
            engine.wait(25 - 1, tips='输出最长持续180s')
            engine.expect_cross_zero_status(0, 1)
            engine.expect_cross_zero_status(1, 0)
        elif value == '反转':
            engine.expect_cross_zero_status(0, 0)
            engine.expect_cross_zero_status(1, 1)
            engine.wait(25 - 1, tips='输出最长持续180s')
            engine.expect_cross_zero_status(0, 0)
            engine.expect_cross_zero_status(1, 1)

        engine.wait(2, tips='行程时间结束，再次检测，输出端均为断开')
        engine.expect_cross_zero_status(0, 0)
        engine.expect_cross_zero_status(1, 0)


def test_保险栓开关状态0A06():
    """
    08_保险栓开关状态0A06
    1、查询出厂默认保险栓开关状态为00关闭
    2、设置保险栓开关状态为01开启、00关闭，并进行查询验证
    """
    engine.add_doc_info('1、查询出厂默认保险栓开关状态为00关闭')
    engine.send_did('READ', '保险栓开关状态0A06', '')
    engine.expect_did('READ', '保险栓开关状态0A06', '00')

    engine.add_doc_info('2、设置保险栓开关状态为01开启、00关闭，并进行查询验证')
    for value in ['01', '00']:
        engine.send_did('WRITE', '保险栓开关状态0A06', value)
        engine.expect_did('WRITE', '保险栓开关状态0A06', value)
        engine.send_did('READ', '保险栓开关状态0A06', '')
        engine.expect_did('READ', '保险栓开关状态0A06', value)


def test_保险栓功能使能标识0A30():
    """
    09_保险栓功能使能标识0A30
    1、查询出厂默认保险栓使能状态为00禁能
    2、设置保险栓使能状态为01使能、00禁能，并进行查询验证
    """
    engine.add_doc_info('1、查询出厂默认保险栓使能状态为00禁能')
    engine.send_did('READ', '保险栓功能使能标识0A30', '')
    engine.expect_did('READ', '保险栓功能使能标识0A30', 使能状态='禁能')

    engine.add_doc_info('2、设置保险栓使能状态为01使能、00禁能，并进行查询验证')
    for value in ['使能', '禁能']:
        engine.send_did('WRITE', '保险栓功能使能标识0A30', 使能状态=value)
        engine.expect_did('WRITE', '保险栓功能使能标识0A30', 使能状态=value)
        engine.send_did('READ', '保险栓功能使能标识0A30', '')
        engine.expect_did('READ', '保险栓功能使能标识0A30', 使能状态=value)


def test_窗帘天空模型配置0A0A():
    """
    10_窗帘天空模型配置0A0A
    1、查询出厂默认窗帘天空模型使能状态为00禁能
    2、设置窗帘天空模型使能状态为01使能、00禁能，并进行查询验证
    """
    engine.add_doc_info('1、查询出厂默认窗帘天空模型使能状态为00禁能')
    engine.send_did('READ', '窗帘天空模型配置0A0A', '')
    engine.expect_did('READ', '窗帘天空模型配置0A0A', '00')

    engine.add_doc_info('2、设置窗帘天空模型使能状态为01使能、00禁能，并进行查询验证')
    for value in ['使能', '禁能']:
        engine.send_did('WRITE', '窗帘天空模型配置0A0A', 使能状态=value)
        engine.expect_did('WRITE', '窗帘天空模型配置0A0A', 使能状态=value)
        engine.send_did('READ', '窗帘天空模型配置0A0A', '')
        engine.expect_did('READ', '窗帘天空模型配置0A0A', 使能状态=value)


def test_窗帘天空模型强制校准次数0A0B():
    """
    11_窗帘天空模型强制校准次数0A0B
    1、查询出厂默认天空模型强制校准次数为30次
    2、设置不同的天空模型强制校准次数，并进行查询验证
    """
    engine.add_doc_info('1、查询出厂默认天空模型强制校准次数为30次')
    engine.send_did('READ', '窗帘天空模型强制校准次数0A0B', '')
    engine.expect_did('READ', '窗帘天空模型强制校准次数0A0B', '1E')

    engine.add_doc_info('2、设置不同的天空模型强制校准次数，并进行查询验证')
    for value in [0, 120, 255, 30]:
        engine.send_did('WRITE', '窗帘天空模型强制校准次数0A0B', 校准次数=value)
        engine.expect_did('WRITE', '窗帘天空模型强制校准次数0A0B', 校准次数=value)
        engine.send_did('READ', '窗帘天空模型强制校准次数0A0B', '')
        engine.expect_did('READ', '窗帘天空模型强制校准次数0A0B', 校准次数=value)


def test_窗帘校准后动作次数0A0C():
    """
    12_窗帘校准后动作次数0A0C
    1、查询出厂默认窗帘校准后动作次数为0次
    2、测试不同的控制方式，如时间控制，开度控制，正转反转，测试动作次数会进行+1，并且到开度为0或100时，自动清除校准次数；
    """
    engine.add_doc_info('1、查询出厂默认窗帘校准后动作次数为0次')
    engine.send_did('READ', '窗帘校准后动作次数0A0C', '')
    engine.expect_did('READ', '窗帘校准后动作次数0A0C', '00')

    engine.add_doc_info('查询当前的行程时间为20s，分别测试不同方式控制')
    engine.send_did('READ', '单轨电机窗帘上升下降行程时间0A02', '')
    engine.expect_did('READ', '单轨电机窗帘上升下降行程时间0A02', 上升行程=20 * 100, 下降行程=20 * 100)
    engine.send_did('READ', '单轨窗帘目标开度0A03', '')
    engine.expect_did('READ', '单轨窗帘目标开度0A03', 开度=0)

    def action_nums_expect(scene_type='时间控制', write_value='正转'):
        if write_value == '正转':
            write_value = '02'
            percent = 100
        elif write_value == '反转':
            write_value = '03'
            percent = 0
        else:
            engine.add_fail_test('注意：无效的控制值')

        if scene_type == '时间控制':
            engine.send_did("WRITE", "电机转动0A01", '00 ' + write_value + ' FF FF')
            engine.expect_did("WRITE", "电机转动0A01", '00 ' + write_value + ' FF FF')
        elif scene_type == '开度控制01':
            engine.send_did('WRITE', '单轨窗帘目标开度0A03', 开度=50)
            engine.expect_did('WRITE', '单轨窗帘目标开度0A03', 开度=50)
        elif scene_type == '开度控制02':
            engine.send_did("WRITE", "电机转动0A04", write_value)
            engine.expect_did("WRITE", "电机转动0A04", write_value)
        engine.wait(10)
        if scene_type == '时间控制':
            engine.send_did("WRITE", "电机转动0A01", '00 01 FF FF')
            engine.expect_did("WRITE", "电机转动0A01", '00 01 FF FF')
        else:
            engine.send_did("WRITE", "电机转动0A04", 电机状态='暂停')
            engine.expect_did("WRITE", "电机转动0A04", 电机状态='暂停')
        engine.wait(1)
        engine.send_did('READ', '窗帘校准后动作次数0A0C', '')
        engine.expect_did('READ', '窗帘校准后动作次数0A0C', '01')
        if scene_type == '时间控制':
            engine.send_did("WRITE", "电机转动0A01", '00 ' + write_value + ' FF FF')
            engine.expect_did("WRITE", "电机转动0A01", '00 ' + write_value + ' FF FF')
        elif scene_type == '开度控制01':
            engine.send_did('WRITE', '单轨窗帘目标开度0A03', 开度=percent)
            engine.expect_did('WRITE', '单轨窗帘目标开度0A03', 开度=percent)
        elif scene_type == '开度控制02':
            engine.send_did("WRITE", "电机转动0A04", write_value)
            engine.expect_did("WRITE", "电机转动0A04", write_value)

        engine.wait(20 * 1.25)
        engine.send_did('READ', '窗帘校准后动作次数0A0C', '')
        engine.expect_did('READ', '窗帘校准后动作次数0A0C', '00')

    engine.add_doc_info('（1）测试时间控制，正转10s后暂停，此时校准次数为1，正转至100%后，此时校准次数为0')
    action_nums_expect(scene_type='时间控制', write_value='正转')

    engine.add_doc_info('（2）测试时间控制，反转10s后暂停，此时校准次数为1，反转至0后，此时校准次数为0')
    action_nums_expect(scene_type='时间控制', write_value='反转')

    engine.add_doc_info('（3）测试开度控制，设置开度为50%，此时校准次数为1，设置开度为100%后，此时校准次数为0')
    action_nums_expect(scene_type='开度控制01', write_value='正转')

    engine.add_doc_info('（4）测试开度控制，设置开度为50%，此时校准次数为1，设置开度为0后，此时校准次数为0')
    action_nums_expect(scene_type='开度控制01', write_value='反转')

    engine.add_doc_info('（5）测试开度控制，正转10s后暂停，此时校准次数为1，正转至100%后，此时校准次数为0')
    action_nums_expect(scene_type='开度控制02', write_value='正转')

    engine.add_doc_info('（6）测试开度控制，反转10s后暂停，此时校准次数为1，反转至0后，此时校准次数为0')
    action_nums_expect(scene_type='开度控制02', write_value='反转')

    engine.add_doc_info('（7）测试开度控制，设置不同的开度40% 60%，分别设置15轮，共计30次，查询此时校准次数为30次')
    engine.send_did('READ', '窗帘校准后动作次数0A0C', '')
    engine.expect_did('READ', '窗帘校准后动作次数0A0C', '00')
    for num in range(15):
        engine.add_doc_info('******第{}轮开度控制测试******'.format(num + 1))
        engine.send_did('WRITE', '单轨窗帘目标开度0A03', 开度=40)
        engine.expect_did('WRITE', '单轨窗帘目标开度0A03', 开度=40)
        if num == 0:
            engine.wait(10, tips='首次测试，开度从0至40%，预留10s间隔')
        engine.wait(5, tips='每次开度控制操作，预留5s间隔')
        engine.send_did('WRITE', '单轨窗帘目标开度0A03', 开度=60)
        engine.expect_did('WRITE', '单轨窗帘目标开度0A03', 开度=60)
        engine.wait(5, tips='每次开度控制操作，预留5s间隔')
    engine.send_did('READ', '窗帘校准后动作次数0A0C', '')
    engine.expect_did('READ', '窗帘校准后动作次数0A0C', '1E')

    engine.add_doc_info('（8）继续（7）的测试，设置开度0%，测试校准次数会自动清除变成0')
    engine.send_did('WRITE', '单轨窗帘目标开度0A03', 开度=0)
    engine.expect_did('WRITE', '单轨窗帘目标开度0A03', 开度=0)
    engine.wait(20 * 1.25)
    engine.send_did('READ', '窗帘校准后动作次数0A0C', '')
    engine.expect_did('READ', '窗帘校准后动作次数0A0C', '00')


def test_错误类报文测试():
    """
    13_错误类报文测试
    1、数据格式错误，返回错误字00 03（C0 12的数据长度为2，而发送命令中的长度为3）
    2、数据域少一个字节，返回错误字00 01数据域长度错误
    3、发送不存在的数据项FB20，返回错误字00 04数据项不存在
    """
    engine.add_doc_info("1、数据格式错误，返回错误字00 03（0A03的数据长度为1，而发送命令中的长度为3）")
    engine.send_did("WRITE", "单轨窗帘目标开度0A03", "01 02 03")
    engine.expect_did("WRITE", "单轨窗帘目标开度0A03", "03 00")

    engine.add_doc_info("2、数据域少一个字节，返回错误字00 01数据域长度错误")
    engine.add_doc_info('本种错误由载波适配层判断并直接回复，所以SWB总线是监控不到的')
    engine.send_raw("07 05 D0 02 03")
    engine.expect_did("WRITE", "主动上报使能标志D005", "01 00")

    engine.add_doc_info("3、发送不存在的数据项，返回错误字00 04数据项不存在")
    engine.send_did("READ", "总有功电能9010", "")
    engine.expect_did("READ", "总有功电能9010", "04 00")


def test_复位等待时间CD00():
    """
    14_复位等待时间CD00
    1、将被测设备的参数配置成与默认参数不一致；
    2、断电重启，测试参数是否丢失；验证断电前后，参数保持不变；
    3、恢复出厂默认参数并进行验证，便于后续的测试项目运行；
    4、再次断电重启，测试断电重启后恢复出厂后的参数仍然正常；
    """
    engine.add_doc_info('1、将被测设备的参数配置成与默认参数不一致，并进行查询验证；')
    modify_default_configuration(modify=True, verify=True)

    engine.add_doc_info('2、断电重启，测试参数是否丢失；验证断电前后，参数保持不变；')
    power_control()
    modify_default_configuration(modify=False, verify=True)

    engine.add_doc_info('3、恢复出厂默认参数并进行验证，便于后续的测试项目运行')
    engine.send_did('WRITE', '复位等待时间CD00', '00')
    engine.expect_did('WRITE', '复位等待时间CD00', '00')

    engine.wait(5, tips='通过复位等待时间CD00恢复出厂，预留充足时间')
    engine.add_doc_info('复位等待时间CD00恢复出厂参数，其中继电器过零点动作延迟时间C020属于工装校准参数，不会被清除，'
                        '为了便于后续测试，将该参数设置回默认参数')
    engine.send_did('WRITE', '继电器过零点动作延迟时间C020', '01 0E 24')
    engine.expect_did('WRITE', '继电器过零点动作延迟时间C020', '01 0E 24')
    read_default_configuration()

    engine.add_doc_info('4、再次断电重启，测试断电重启后恢复出厂后的参数仍然正常；')
    power_control()
    read_default_configuration()
