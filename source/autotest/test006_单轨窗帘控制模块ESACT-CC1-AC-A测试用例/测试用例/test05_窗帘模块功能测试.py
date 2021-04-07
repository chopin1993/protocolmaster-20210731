#!/usr/bin/evn python
# -*- coding: utf-8 -*-
"""
@Time: 2021/3/31 16:37
@Author: SUN
@File: test05_窗帘模块功能测试.py
@Software: PyCharm
"""
from .常用测试模块 import *

测试组说明 = "窗帘模块功能测试"
"""
本模块主要用于测试窗帘控制模块的功能测试和场景测试
"""

config = engine.get_config()


def test_时间控制与开度控制兼容性():
    """
    01_时间控制与开度控制兼容性
    1、默认出厂行程时间为00 00 00 00时，不支持开度控制，支持时间控制（时间控制，时间范围为0-180s,超过180s的时间按照180s进行计时）
    和正转反转控制（行程时间为0时，正转和反转的运行时间默认为180s）本测试项在test02_功能类协议测试中已测试，不再重复；
    2、设置上升行程时间和下降行程时间，正转反转0A04控制的情况
    （无论正转还是反转，时间与设置的行程时间*1.25一致，在test_电机转动0A04已测试，不再重复测试）；
    3、设置上升行程时间和下降行程时间，测试时间控制时间大于行程时间的、等于、小于行程时间的情况
    （窗帘模块此时收到时间控制报文，无论大小，均按照行程时间*1.25运行）；
    4、进行开度控制的过程中，发送时间控制的报文；
    5、进行时间控制的过程中，发送开度控制的报文；
    6、窗口控制过程中发送停止命令，进行开度控制的过程中，发送控制暂停的报文；
    7、窗口控制过程中发送停止命令，进行时间控制的过程中，发送控制暂停的报文；
    """
    engine.report_check_enable_all(True)  # 打开上报检测
    report_power_on_expect(wait_times=[68], ack=True, wait_enable=False)
    engine.add_doc_info('状态同步测试项中已设置行程时间：上升行程20s、下降行程20s')
    engine.send_did('READ', '单轨电机窗帘上升下降行程时间0A02', '')
    engine.expect_did('READ', '单轨电机窗帘上升下降行程时间0A02', 上升行程=20 * 100, 下降行程=20 * 100)
    engine.send_did('READ', '单轨窗帘目标开度0A03', '')
    engine.expect_did('READ', '单轨窗帘目标开度0A03', 开度=0)
    engine.wait(5, tips='各项窗帘控制模块操作，间隔5s')

    engine.add_doc_info('1、默认出厂行程时间为00 00 00 00时，不支持开度控制，'
                        '支持时间控制''（时间控制，时间范围为0-180s,超过180s的时间按照180s进行计时）和'
                        '正转反转控制（行程时间为0时，正转和反转的运行时间默认为180s）'
                        '本测试项在  test02_功能类协议  测试中已测试，不再重复；')

    engine.add_doc_info('2、设置上升行程时间和下降行程时间，正转反转0A04控制的情况'
                        '（无论正转还是反转，时间与设置的行程时间*1.25一致，在test_电机转动0A04已测试，不再重复测试）；')

    engine.add_doc_info('3、设置上升行程时间和下降行程时间，测试时间控制时间大于行程时间的、等于、小于行程时间的情况'
                        '（窗帘模块此时收到时间控制报文，无论大小，均按照行程时间*1.25运行）；')

    engine.add_doc_info('测试时间控制大于、等于、小于行程时间的情况，分别为最大值30、20s、10s，均按照行程时间*1.25运行')
    for run_time in ['FF FF', 'D0 07', 'E8 03']:
        for value in ['02 ', '03 ']:
            # 正转为'02'，反转为'03'
            engine.send_did("WRITE", "电机转动0A01", '00 ' + value + run_time)
            engine.expect_did("WRITE", "电机转动0A01", '00 ' + value + run_time)
            if value == '02 ':
                output_detect_220V(True, 20, 20)
            elif value == '03 ':
                output_detect_220V(False, 20, 20)

    engine.add_doc_info('4、进行开度控制的过程中，发送时间控制的报文；')
    engine.add_doc_info('（1）初始开度为0时，此时发送0A04反转、开度控制至0，时间控制反转，继电器均不动作')
    engine.send_did("WRITE", "电机转动0A04", 电机状态='反转')
    engine.expect_did("WRITE", "电机转动0A04", 电机状态='反转')
    engine.wait(1)
    engine.expect_cross_zero_status(0, 0)
    engine.expect_cross_zero_status(1, 0)

    engine.send_did('WRITE', '单轨窗帘目标开度0A03', 开度=0)
    engine.expect_did('WRITE', '单轨窗帘目标开度0A03', 开度=0)
    engine.wait(1)
    engine.expect_cross_zero_status(0, 0)
    engine.expect_cross_zero_status(1, 0)

    engine.send_did("WRITE", "电机转动0A01", '00 03 FF FF')
    engine.expect_did("WRITE", "电机转动0A01", '00 03 FF FF')
    engine.wait(1)
    engine.expect_cross_zero_status(0, 0)
    engine.expect_cross_zero_status(1, 0)

    engine.add_doc_info('（2）初始开度为0时，开度控制正转，5s后发送时间控制反转，继电器动作正常')
    engine.send_did('WRITE', '单轨窗帘目标开度0A03', 开度=100)
    engine.expect_did('WRITE', '单轨窗帘目标开度0A03', 开度=100)
    engine.wait(1)
    engine.expect_cross_zero_status(0, 1)
    engine.expect_cross_zero_status(1, 0)
    engine.wait(5, tips='5s后发送时间控制反转')
    engine.send_did("WRITE", "电机转动0A01", '00 03 FF FF')
    engine.expect_did("WRITE", "电机转动0A01", '00 03 FF FF')
    engine.wait(2)
    engine.expect_cross_zero_status(0, 0)
    engine.expect_cross_zero_status(1, 1)

    engine.wait(30, tips='预留30s测试间隔')

    engine.add_doc_info('（3）将窗帘控制模块开度设置到100%，，此时发送0A04正转、开度控制至100，时间控制正转，继电器均不动作')
    report_subscribe_expect([], write_value="64", current_value="00", scene_type="网关单点控制")

    engine.send_did("WRITE", "电机转动0A04", 电机状态='正转')
    engine.expect_did("WRITE", "电机转动0A04", 电机状态='正转')
    engine.wait(1)
    engine.expect_cross_zero_status(0, 0)
    engine.expect_cross_zero_status(1, 0)

    engine.send_did('WRITE', '单轨窗帘目标开度0A03', 开度=100)
    engine.expect_did('WRITE', '单轨窗帘目标开度0A03', 开度=100)
    engine.wait(1)
    engine.expect_cross_zero_status(0, 0)
    engine.expect_cross_zero_status(1, 0)

    engine.send_did("WRITE", "电机转动0A01", '00 02 FF FF')
    engine.expect_did("WRITE", "电机转动0A01", '00 02 FF FF')
    engine.wait(1)
    engine.expect_cross_zero_status(0, 0)
    engine.expect_cross_zero_status(1, 0)

    engine.add_doc_info('（4）初始开度为100%时，开度控制反转，5s后发送时间控制正转，继电器动作正常')
    engine.send_did('WRITE', '单轨窗帘目标开度0A03', 开度=0)
    engine.expect_did('WRITE', '单轨窗帘目标开度0A03', 开度=0)
    engine.wait(1)
    engine.expect_cross_zero_status(0, 0)
    engine.expect_cross_zero_status(1, 1)
    engine.wait(5, tips='5s后发送开度控制正转')

    engine.send_did("WRITE", "电机转动0A01", '00 02 FF FF')
    engine.expect_did("WRITE", "电机转动0A01", '00 02 FF FF')
    engine.wait(2)
    engine.expect_cross_zero_status(0, 1)
    engine.expect_cross_zero_status(1, 0)

    engine.wait(30, tips='预留10s测试间隔')

    engine.add_doc_info('5、进行时间控制的过程中，发送开度控制的报文；')
    engine.add_doc_info('在步骤4的基础上进行测试，当前开度为100%')

    engine.add_doc_info('（1）初始开度为100%时，时间控制反转，5s后发送开度控制正转，继电器动作正常')
    engine.send_did("WRITE", "电机转动0A01", '00 03 FF FF')
    engine.expect_did("WRITE", "电机转动0A01", '00 03 FF FF')
    engine.wait(1)
    engine.expect_cross_zero_status(0, 0)
    engine.expect_cross_zero_status(1, 1)
    engine.wait(5, tips='5s后发送开度控制正转')
    engine.send_did('WRITE', '单轨窗帘目标开度0A03', 开度=100)
    engine.expect_did('WRITE', '单轨窗帘目标开度0A03', 开度=100)
    engine.wait(2)
    engine.expect_cross_zero_status(0, 1)
    engine.expect_cross_zero_status(1, 0)

    engine.wait(30, tips='预留30s测试间隔')

    engine.add_doc_info('（2）将窗帘开度重新设置为0')
    report_subscribe_expect([], write_value="00", current_value="64", scene_type="网关单点控制")

    engine.add_doc_info('（3）初始开度为0时，时间控制正转，5s后发送开度控制反转，继电器动作正常')
    engine.send_did("WRITE", "电机转动0A01", '00 02 FF FF')
    engine.expect_did("WRITE", "电机转动0A01", '00 02 FF FF')
    engine.wait(1)
    engine.expect_cross_zero_status(0, 1)
    engine.expect_cross_zero_status(1, 0)
    engine.wait(5, tips='5s后发送开度控制正转')
    engine.send_did('WRITE', '单轨窗帘目标开度0A03', 开度=0)
    engine.expect_did('WRITE', '单轨窗帘目标开度0A03', 开度=0)
    engine.wait(2)
    engine.expect_cross_zero_status(0, 0)
    engine.expect_cross_zero_status(1, 1)

    engine.wait(30, tips='预留30s测试间隔')

    engine.add_doc_info('6、窗口控制过程中发送停止命令，进行开度控制的过程中，发送控制暂停的报文；')
    engine.add_doc_info('测试开度控制窗帘上升或下降的过程中，进行开度控制暂停，通过输出端验证，暂停优先级高')
    engine.add_doc_info('测试开度控制窗帘上升或下降的过程中，进行时间控制暂停，通过输出端验证，暂停优先级高')
    for stop_type in ['开度控制暂停', '时间控制暂停']:
        for value in [100, 0]:
            engine.add_doc_info('测试前查询输出端，均无输出')
            engine.expect_cross_zero_status(0, 0)
            engine.expect_cross_zero_status(1, 0)
            engine.send_did('WRITE', '单轨窗帘目标开度0A03', 开度=value)
            engine.expect_did('WRITE', '单轨窗帘目标开度0A03', 开度=value)
            engine.wait(1)
            if value == 100:
                engine.expect_cross_zero_status(0, 1)
                engine.expect_cross_zero_status(1, 0)
            elif value == 0:
                engine.expect_cross_zero_status(0, 0)
                engine.expect_cross_zero_status(1, 1)
            engine.wait(10, tips='开度控制10s后，进行暂停操作')
            if stop_type == '开度控制暂停':
                engine.send_did("WRITE", "电机转动0A04", 电机状态='暂停')
                engine.expect_did("WRITE", "电机转动0A04", 电机状态='暂停')
            elif stop_type == '时间控制暂停':
                engine.send_did("WRITE", "电机转动0A01", '00 01 FF FF')
                engine.expect_did("WRITE", "电机转动0A01", '00 01 FF FF')
            engine.wait(1)
            engine.expect_cross_zero_status(0, 0)
            engine.expect_cross_zero_status(1, 0)

            engine.wait(30, tips='预留30s测试间隔')

    engine.add_doc_info('7、窗口控制过程中发送停止命令，进行时间控制的过程中，发送控制暂停的报文；')
    engine.add_doc_info('测试时间控制窗帘上升或下降的过程中，进行开度控制暂停，通过输出端验证，暂停优先级高')
    engine.add_doc_info('测试时间控制窗帘上升或下降的过程中，进行时间控制暂停，通过输出端验证，暂停优先级高')

    for stop_type in ['开度控制暂停', '时间控制暂停']:
        for value in ['时间控制正转', '时间控制反转']:
            engine.add_doc_info('测试前查询输出端，均无输出')
            engine.expect_cross_zero_status(0, 0)
            engine.expect_cross_zero_status(1, 0)
            if value == '时间控制正转':
                engine.send_did("WRITE", "电机转动0A01", '00 02 FF FF')
                engine.expect_did("WRITE", "电机转动0A01", '00 02 FF FF')
                engine.wait(1)
                engine.expect_cross_zero_status(0, 1)
                engine.expect_cross_zero_status(1, 0)
            elif value == '时间控制反转':
                engine.send_did("WRITE", "电机转动0A01", '00 03 FF FF')
                engine.expect_did("WRITE", "电机转动0A01", '00 03 FF FF')
                engine.wait(1)
                engine.expect_cross_zero_status(0, 0)
                engine.expect_cross_zero_status(1, 1)
            engine.wait(10, tips='开度控制10s后，进行暂停操作')
            if stop_type == '开度控制暂停':
                engine.send_did("WRITE", "电机转动0A04", 电机状态='暂停')
                engine.expect_did("WRITE", "电机转动0A04", 电机状态='暂停')
            elif stop_type == '时间控制暂停':
                engine.send_did("WRITE", "电机转动0A01", '00 01 FF FF')
                engine.expect_did("WRITE", "电机转动0A01", '00 01 FF FF')
            engine.wait(1)
            engine.expect_cross_zero_status(0, 0)
            engine.expect_cross_zero_status(1, 0)

            engine.wait(30, tips='预留30s测试间隔')

    engine.report_check_enable_all(False)  # 关闭上报检测


def test_开度控制多次后的复位测试():
    """
    02_开度控制多次后的复位测试
    本部分测试需要观察窗帘的实际动作，通过人工进行测试；
    开度控制多次后的复位原因：开度控制存在累计误差，动作一定次数后必须通过复位来消除该误差。
    1、目前的机制是：当窗帘上升时间<26秒，则开度控制每动作8次时，复位一次；
    2、当上升时间在≧26s和<34s时，开度控制每动作8次时，复位一次;
    3、当上升时间在≧34s和<42s时，开度控制每动作11次时，复位一次;
    4、当上升时间在≧42s时,开度控制每动作14次时，复位一次。
    5、若设备已设置行程，则开关超过行程时间，则视为校准或复位操作；
    """

    engine.report_check_enable_all(True)  # 打开上报检测
    engine.add_doc_info('本部分测试需要观察窗帘的实际动作，通过人工进行测试；')
    engine.report_check_enable_all(False)  # 关闭上报检测


def test_窗帘模块停上电后的状态测试():
    """
    03_窗帘模块停上电后的状态测试
    1、窗帘模块静止状态，停上电后的参数验证和控制验证
    2、窗帘模块运行状态，停上电后的参数验证和控制验证
    3、设备上电无论是否已设置行程时间，均不进行开度校准动作
    （若上电即进行开度校准动作，向上校准容易产生因电机未调节上限位而导致的过圈问题发生，向下校准容易引起用户不解，
    尤其是在宾馆等某些特定应用场合，半夜上电后窗帘自己校准动作容易使顾客产生恐慌。）
    """

    engine.report_check_enable_all(True)  # 打开上报检测
    report_power_on_expect(wait_times=[68], ack=True, wait_enable=False)
    engine.add_doc_info('1、窗帘模块静止状态，停上电后的参数验证和控制验证')
    engine.add_doc_info('窗帘处于静止状态，分别测试窗帘位于开度=0和开度=100的情况下，上电上报正常，'
                        '开度控制也正常，在上电上报模块中已进行验证，不再重复测试')

    engine.add_doc_info('2、窗帘模块运行状态，停上电后的参数验证和控制验证')
    engine.add_doc_info('窗帘正转或者反转过程中断电重启，开度丢失，上电上报开度为FF未知，'
                        '此时测试控制正常，控制后，窗帘先反转至底部，然后在正转至正确位置上')
    for value in ['正转', '反转']:
        if value == '正转':
            engine.add_doc_info('初始状态开度为0，发送正转命令进行断电测试')
        elif value == '反转':
            engine.add_doc_info('初始状态开度为60，发送反转命令进行断电测试')
        engine.send_did("WRITE", "电机转动0A04", 电机状态=value)
        engine.expect_did("WRITE", "电机转动0A04", 电机状态=value)
        engine.wait(5, tips='正转5s后发送进行断电重启测试')
        report_power_on_expect(wait_times=[68], ack=True, wait_enable=False, expect_value="FF")
        engine.wait(10, tips='上电上报成功后，进行设置开度=60测试，窗帘先反转25s，再正转12s至指定位置')
        engine.send_did('WRITE', '单轨窗帘目标开度0A03', 开度=60)
        engine.expect_did('WRITE', '单轨窗帘目标开度0A03', 开度=60)
        engine.expect_cross_zero_status(0, 0)
        engine.expect_cross_zero_status(1, 0)
        engine.wait(1, tips='断电重启后首次控制，窗帘先反转20*1.25s')
        engine.expect_cross_zero_status(0, 0)
        engine.expect_cross_zero_status(1, 1)
        engine.wait(25 - 1, tips='反转持续20*1.25s')
        engine.expect_cross_zero_status(0, 0)
        engine.expect_cross_zero_status(1, 1)
        engine.wait(2, tips='然后再正转12s')
        engine.expect_cross_zero_status(0, 1)
        engine.expect_cross_zero_status(1, 0)
        engine.wait(12 - 1, tips='正转持续12s')
        engine.expect_cross_zero_status(0, 1)
        engine.expect_cross_zero_status(1, 0)
        engine.wait(2, tips='窗帘动作结束，检测此时无输出')
        engine.expect_cross_zero_status(0, 0)
        engine.expect_cross_zero_status(1, 0)

        engine.wait(30, tips='预留30s测试间隔')

    engine.add_doc_info('3、设备上电无论是否已设置行程时间，均不进行开度校准动作')
    engine.add_doc_info('行程时间为0时，断电重启，检测输出端无输出')
    engine.send_did('WRITE', '复位等待时间CD00', '00')
    engine.expect_did('WRITE', '复位等待时间CD00', '00')
    engine.wait(5, tips='通过复位等待时间CD00恢复出厂，预留充足时间')
    engine.send_did('READ', '单轨电机窗帘上升下降行程时间0A02', '')
    engine.expect_did('READ', '单轨电机窗帘上升下降行程时间0A02', '00 00 00 00')
    engine.add_doc_info("测试工装控制通断电")
    engine.wait(seconds=1, tips='保证和之前的测试存在1s间隔')
    engine.control_relay(0, 0)
    engine.wait(seconds=10, tips='保证被测设备充分断电')
    engine.control_relay(0, 1)
    engine.wait(1, tips='上电后立即查询输出端，无输出')
    engine.expect_cross_zero_status(0, 0)
    engine.expect_cross_zero_status(1, 0)
    engine.wait(1, tips='10s后查询输出端，也无输出')
    engine.expect_cross_zero_status(0, 0)
    engine.expect_cross_zero_status(1, 0)
    engine.wait(30, tips='预留30s测试间隔')

    engine.add_doc_info('行程时间不为0时，断电重启，检测输出端无输出，不进行开度校准')
    engine.send_did('WRITE', '单轨电机窗帘上升下降行程时间0A02', 上升行程=20 * 100, 下降行程=20 * 100)
    engine.expect_did('WRITE', '单轨电机窗帘上升下降行程时间0A02', 上升行程=20 * 100, 下降行程=20 * 100)
    engine.wait(30, tips='设置行程后，窗帘控制模块会主动下拉至开度0，预留充足的时间')
    engine.add_doc_info("测试工装控制通断电")
    engine.wait(seconds=1, tips='保证和之前的测试存在1s间隔')
    engine.control_relay(0, 0)
    engine.wait(seconds=10, tips='保证被测设备充分断电')
    engine.control_relay(0, 1)
    engine.wait(1, tips='上电后立即查询输出端，无输出')
    engine.expect_cross_zero_status(0, 0)
    engine.expect_cross_zero_status(1, 0)
    engine.wait(1, tips='10s后查询输出端，也无输出')
    engine.expect_cross_zero_status(0, 0)
    engine.expect_cross_zero_status(1, 0)
    engine.wait(30, tips='预留30s测试间隔')

    engine.report_check_enable_all(False)  # 关闭上报检测


def test_天空模型测试():
    """
    04_天空模型测试
    校准机制：当前复位次数>=强制校准次数，且触发下拉命令时，触发校准，并且复位次数清空；
    1、天空模型使能后，家庭复位校准机制失效，启用强制校准，进行相关验证；
    2、开天空模型使能后，设备动作后上报动作次数
    3、天空模型使能后，设置不同的强制校准次数，如10次,40次,30次，测试强制校准是否正常；
    4、测试完成后，将开度重新设置为0
    """
    pass
    engine.report_check_enable_all(True)  # 打开上报检测
    report_power_on_expect(wait_times=[68], ack=True, wait_enable=False)
    engine.add_doc_info('1、天空模型使能后，家庭复位校准机制失效，启用强制校准，进行相关验证；'
                        '启用天空模型使能，查询行程时间已经被设置为上升20s，下降20s和动作次数为0')

    engine.send_did('WRITE', '窗帘天空模型配置0A0A', 使能状态='使能')
    engine.expect_did('WRITE', '窗帘天空模型配置0A0A', 使能状态='使能')
    engine.send_did('READ', '单轨电机窗帘上升下降行程时间0A02', '')
    engine.expect_did('READ', '单轨电机窗帘上升下降行程时间0A02', 上升行程=20 * 100, 下降行程=20 * 100)
    engine.send_did('READ', '窗帘校准后动作次数0A0C', '')
    engine.expect_did('READ', '窗帘校准后动作次数0A0C', 动作次数=0)

    engine.add_doc_info('2、开天空模型使能后，设备动作后上报动作次数')
    report_subscribe_expect(devices=[], write_value="32", current_value="00", sky_model_enable=True, expect_reset=1)

    report_subscribe_expect(devices=[], write_value="00", current_value="32", sky_model_enable=True, expect_reset=2)

    engine.add_doc_info('3、天空模型使能后，设置不同的强制校准次数，如10次,41次,30次，测试强制校准是否正常；')
    for value in [10, 21, 30]:
        engine.add_doc_info('测试强制校准次数为{}次的情况'.format(value))
        engine.send_did('WRITE', '窗帘天空模型强制校准次数0A0B', 校准次数=value)
        engine.expect_did('WRITE', '窗帘天空模型强制校准次数0A0B', 校准次数=value)
        engine.send_did('READ', '窗帘天空模型强制校准次数0A0B', '')
        engine.expect_did('READ', '窗帘天空模型强制校准次数0A0B', 校准次数=value)

        for num in range(value):
            engine.add_doc_info('******第{}轮开度控制测试******'.format(num + 1))
            if num % 2 == 0:
                engine.send_did('WRITE', '单轨窗帘目标开度0A03', 开度=40)
                engine.expect_did('WRITE', '单轨窗帘目标开度0A03', 开度=40)
            elif num % 2 == 1:
                engine.send_did('WRITE', '单轨窗帘目标开度0A03', 开度=60)
                engine.expect_did('WRITE', '单轨窗帘目标开度0A03', 开度=60)
            if num == 0:
                engine.wait(10, tips='首次测试，开度从0至40%，预留10s间隔')
            engine.wait(7, tips='每次开度控制操作，预留5s间隔')
        if value % 2 == 0:
            engine.send_did('READ', '窗帘校准后动作次数0A0C', '')
            engine.expect_did('READ', '窗帘校准后动作次数0A0C', 动作次数=value)
            engine.add_doc_info('当满足动作次数后，最后一次窗帘控制是上拉的时候，不触发强制复位机制，'
                                '需要等待下一次的下拉触发复位机制')
            engine.send_did('WRITE', '单轨窗帘目标开度0A03', 开度=30)
            engine.expect_did('WRITE', '单轨窗帘目标开度0A03', 开度=30)
            engine.wait(30, tips='预留30s测试间隔')
            engine.send_did('READ', '窗帘校准后动作次数0A0C', '')
            engine.expect_did('READ', '窗帘校准后动作次数0A0C', 动作次数=1)
        elif value % 2 == 1:
            engine.wait(30, tips='当满足动作次数后，最后一次窗帘控制是下拉的时候，触发强制复位机制，等待30s')
            engine.send_did('READ', '窗帘校准后动作次数0A0C', '')
            engine.expect_did('READ', '窗帘校准后动作次数0A0C', 动作次数=1)

    engine.add_doc_info('4、测试完成后，将开度重新设置为0')
    engine.send_did('WRITE', '单轨窗帘目标开度0A03', 开度=0)
    engine.expect_did('WRITE', '单轨窗帘目标开度0A03', 开度=0)
    engine.wait(30, tips='预留30s测试间隔')
    engine.report_check_enable_all(False)  # 关闭上报检测


def test_保险栓测试():
    """
    05_保险栓测试
    1、测试4种不同的组合方式：保险栓使能/禁用和保险栓开/关组合，
    在保险栓使能+保险栓开的情况下，网关单点控制、网关情景模式、面板情景模式控制均无法控制，面板单点控制可以正常控制；
    其他情况下，网关单点控制、网关情景模式、面板单点控制、面板情景模式控制均可以正常控制；
    """
    engine.add_doc_info('在保险栓使能+保险栓开的情况下，网关单点控制、网关情景模式、面板情景模式控制均无法控制，面板单点控制可以正常控制；'
                        '其他情况下，网关单点控制、网关情景模式、面板单点控制、面板情景模式控制均可以正常控制')
    engine.report_check_enable_all(True)  # 打开上报检测
    report_power_on_expect(wait_times=[68], ack=True, wait_enable=False)
    engine.send_did('READ', '单轨窗帘目标开度0A03', '')
    engine.expect_did('READ', '单轨窗帘目标开度0A03', 开度=0)

    # 配置订阅者3个
    panel01 = set_subscriber("订阅者1", 21)
    panel02 = set_subscriber("订阅者2", 22)
    panel03 = set_subscriber("订阅者3", 23)

    def fuse_test(fuse_enable=True, fuse_switch=True):
        if fuse_enable:
            engine.send_did('WRITE', '保险栓功能使能标识0A30', 使能状态='使能')
            engine.expect_did('WRITE', '保险栓功能使能标识0A30', 使能状态='使能')
        else:
            engine.send_did('WRITE', '保险栓功能使能标识0A30', 使能状态='禁能')
            engine.expect_did('WRITE', '保险栓功能使能标识0A30', 使能状态='禁能')

        if fuse_switch:
            engine.send_did('WRITE', '保险栓开关状态0A06', 开关状态='01')
            engine.expect_did('WRITE', '保险栓开关状态0A06', 开关状态='01')
        else:
            engine.send_did('WRITE', '保险栓开关状态0A06', 开关状态='00')
            engine.expect_did('WRITE', '保险栓开关状态0A06', 开关状态='00')

        if fuse_enable and fuse_switch:
            engine.add_doc_info('保险栓使能+保险栓开关打开时，网关单点控制和情景模式控制均被禁用')
            engine.add_doc_info('网关单点控制开至50%')
            engine.send_did('WRITE', '单轨窗帘目标开度0A03', '32')
            engine.expect_did('WRITE', '单轨窗帘目标开度0A03', '20 00')
            for panel in [panel01, panel02, panel03]:
                panel.expect_multi_dids("NOTIFY",
                                        None, None, "单轨窗帘目标开度0A03", '00',
                                        None, None, "单轨窗帘当前开度0A05", '00', )
            engine.expect_multi_dids("REPORT",
                                     "单轨窗帘目标开度0A03", '00',
                                     "单轨窗帘当前开度0A05", '00',
                                     "导致状态改变的控制设备AIDC01A", config["抄控器默认源地址"], ack=True)
            engine.wait(10, tips='10s后再次查询窗帘开度为0，说明窗帘此时不受网关控制')
            engine.send_did('READ', '单轨窗帘目标开度0A03', '')
            engine.expect_did('READ', '单轨窗帘目标开度0A03', 开度=0)

            engine.add_doc_info('网关情景模式控制开至50%')
            engine.send_did("WRITE", "单轨窗帘目标开度0A03", '32', gids=[7, 8, 9, 10, 11], gid_type="BIT1")
            engine.expect_multi_dids("REPORT",
                                     "保险栓功能使能标识0A30", '01',
                                     "保险栓开关状态0A06", '01',
                                     '导致状态改变的控制设备AIDC01A', config["抄控器默认源地址"], ack=True, timeout=4)
            engine.wait(10, tips='10s后再次查询窗帘开度为0，说明窗帘此时不受网关控制')
            engine.send_did('READ', '单轨窗帘目标开度0A03', '')
            engine.expect_did('READ', '单轨窗帘目标开度0A03', 开度=0)
        else:
            engine.add_doc_info('网关单点控制开至50%')
            report_subscribe_expect([panel01, panel02, panel03], write_value="32", current_value="00",
                                    scene_type="网关单点控制")
            engine.add_doc_info('网关情景模式控制关至0')
            report_subscribe_expect([panel01, panel02, panel03], write_value="00", current_value="32",
                                    first_timeout=3.3, scene_type="网关情景模式控制")

        engine.add_doc_info('面板单点控制开至50%')
        report_subscribe_expect([panel01, panel02, panel03], write_value="32", current_value="00",
                                scene_type="订阅者01单点控制")
        engine.add_doc_info('面板情景模式控制关至0')
        if fuse_enable and fuse_switch:
            engine.add_doc_info('保险栓使能+保险栓开关打开时，面板类设备情景模式控制也被禁用')
            panel01.send_did("WRITE", "单轨窗帘目标开度0A03", '00', gids=[7, 8, 9, 10, 11], gid_type="BIT1")
            panel01.expect_multi_dids("NOTIFY",
                                      None, None, "保险栓功能使能标识0A30", '01',
                                      None, None, "保险栓开关状态0A06", '01', timeout=4)
            engine.expect_multi_dids("REPORT",
                                     "保险栓功能使能标识0A30", '01',
                                     "保险栓开关状态0A06", '01',
                                     '导致状态改变的控制设备AIDC01A', panel01.said, ack=True)
            engine.add_doc_info('因为保险栓使能+保险栓开关打开时，不受广播报文控制，所以通过面板单点控制开至0%')
            engine.add_doc_info('面板单点控制开至0')
            report_subscribe_expect([panel01, panel02, panel03], write_value="00", current_value="32",
                                    scene_type="订阅者01单点控制")
        else:
            report_subscribe_expect([panel01, panel02, panel03], write_value="00", current_value="32",
                                    first_timeout=3.3, scene_type="订阅者01情景模式控制")

    engine.add_doc_info('（1）测试保险栓使能+保险栓开的情况，网关单点控制、网关情景模式均无法控制，面板单点控制、面板情景模式控制可以正常控制')
    fuse_test(fuse_enable=True, fuse_switch=True)

    engine.add_doc_info('（2）测试保险栓使能+保险栓关的情况，网关单点控制、网关情景模式、面板单点控制、面板情景模式控制均可以正常控制')
    fuse_test(fuse_enable=True, fuse_switch=False)

    engine.add_doc_info('（3）测试保险栓禁能+保险栓开的情况，网关单点控制、网关情景模式、面板单点控制、面板情景模式控制均可以正常控制')
    fuse_test(fuse_enable=False, fuse_switch=True)

    engine.add_doc_info('（4）测试保险栓禁能+保险栓关的情况，网关单点控制、网关情景模式、面板单点控制、面板情景模式控制均可以正常控制')
    fuse_test(fuse_enable=False, fuse_switch=False)

    engine.report_check_enable_all(False)  # 关闭上报检测


def test_测试结束后恢复默认参数():
    """
    06_测试结束后恢复默认参数
    """
    engine.add_doc_info('升级测试结束后发送CD00清除参数，使被测设备恢复出厂参数')

    return_to_factory()
