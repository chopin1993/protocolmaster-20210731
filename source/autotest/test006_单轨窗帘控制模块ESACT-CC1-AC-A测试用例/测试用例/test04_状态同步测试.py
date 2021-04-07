# encoding:utf-8
# 导入测试引擎
from .常用测试模块 import *

测试组说明 = "状态同步测试"
"""
参数说明	                    原时间参数（单位：s）|优化后时间参数（单位：100ms）
状态改变等待时间	                    5	       |        13
订阅者间间隔	                        1	       |        2
情景模式控制各设备上报间隔	            2          |  	    5
"""
config = engine.get_config()


def test_添加上报():
    """
    01_添加上报测试
    1、窗帘控制模块不支持添加上报功能，本项暂不测试；
    """
    engine.add_doc_info('1、窗帘控制模块不支持添加上报功能，本项暂不测试；')


def test_上电上报():
    """
    02_上电上报测试
    上电上报计算公式：延时时间1分钟（网关重启组网时间）+ rand 秒，其中rand=sid% 100。
    窗帘控制模块首次设置行程时间，窗帘会下拉至底部，然后上报当前开度0；窗帘控制模块首次设置行程时间，立即断电重启，上报当前开度为FF；其他情况窗帘运动过程中断电重启，上报当前开度为FF，其余情况下仍是正常的开度；
    1、测试测试sid > 100的情况，sid = 320的情况下，测试网关正常应答的情况(行程为0时不进行上电上报，行程不为0时，上电上报正常)
    2、测试测试sid < 100的情况，sid = 8的情况下，测试网关正常应答的情况(行程为0时不进行上电上报，行程不为0时，上电上报正常)
    3、测试上报重发机制，收不到网关应答，进行10s、100s重试，重试结束则本次上电上报
    4、如果10s重试上报过程中，收到网关应答，不再进行100重试上报
    5、测试上电上报前的过程中，是否可以正常被控制通断（控制正常，被控制后，本产品状态同步正常，添加上报被打断，不再重试）
    6、测试上电上报重试的过程中，是否可以正常被控制通断（控制正常，被控制后，本产品状态同步正常，添加上报被打断，不再重试）
    7、窗帘控制模块开度为0的情况，上述已验证，再次测试窗帘控制模块开度为100%的情况，进行上电上报测试；
    """
    engine.report_check_enable_all(True)  # 打开上报检测

    engine.add_doc_info("1、测试测试sid > 100的情况，sid = 320的情况下，测试网关正常应答的情况")
    set_gw_info(panid=1100, sid=320)
    engine.wait(15, allowed_message=False)
    engine.add_doc_info('(1)当前行程时间为00 00 00 00的情况下，不进行上电上报')
    engine.send_did('READ', '单轨电机窗帘上升下降行程时间0A02', '')
    engine.expect_did('READ', '单轨电机窗帘上升下降行程时间0A02', '00 00 00 00')
    report_power_on_expect(wait_times=[80], report_expect=False)

    engine.add_doc_info('(2)设置当前上行和下行行程时间为20s，为D0 07 D0 07的情况下，进行上电上报')
    engine.send_did('WRITE', '单轨电机窗帘上升下降行程时间0A02', 上升行程=20 * 100, 下降行程=20 * 100)
    engine.expect_did('WRITE', '单轨电机窗帘上升下降行程时间0A02', 上升行程=20 * 100, 下降行程=20 * 100)
    engine.wait(30, tips='设置行程后，窗帘控制模块会主动下拉至开度0，预留充足的时间')
    report_power_on_expect(wait_times=[80])

    engine.add_doc_info('本轮测试完毕，将行程时间恢复出厂参数 00 00 00 00')
    engine.send_did('WRITE', '复位等待时间CD00', '00')
    engine.expect_did('WRITE', '复位等待时间CD00', '00')
    engine.wait(5, tips='通过复位等待时间CD00恢复出厂，预留充足时间')

    engine.add_doc_info("2、测试sid < 100的情况，sid = 8的情况下，测试网关正常应答的情况")
    set_gw_info()
    engine.wait(15, allowed_message=False)

    engine.add_doc_info('(1)当前行程时间为00 00 00 00的情况下，不进行上电上报')
    engine.send_did('READ', '单轨电机窗帘上升下降行程时间0A02', '')
    engine.expect_did('READ', '单轨电机窗帘上升下降行程时间0A02', '00 00 00 00')
    report_power_on_expect(wait_times=[68], report_expect=False)

    engine.add_doc_info('(2)设置当前上行和下行行程时间为20s，为D0 07 D0 07的情况下，进行上电上报')
    engine.send_did('WRITE', '单轨电机窗帘上升下降行程时间0A02', 上升行程=20 * 100, 下降行程=20 * 100)
    engine.expect_did('WRITE', '单轨电机窗帘上升下降行程时间0A02', 上升行程=20 * 100, 下降行程=20 * 100)
    engine.wait(30, tips='设置行程后，窗帘控制模块会主动下拉至开度0，预留充足的时间')
    report_power_on_expect(wait_times=[68])

    engine.add_doc_info("3、测试上报重发机制，收不到网关应答，进行10s、100s重试，重试结束则本次添加上报结束")
    engine.add_doc_info('初次')
    report_power_on_expect(wait_times=[68, 10, 100], ack=False)

    engine.add_doc_info("4、如果10s重试上报过程中，收到网关应答，不再进行100重试上报")
    report_power_on_expect(wait_times=[68, 10], ack=True)

    engine.add_doc_info("5、测试上电上报前的过程中，是否可以正常被控制通断"
                        "（控制正常，被控制后，本产品状态同步正常，添加上报被打断，不再重试）"
                        "上电上报前被控制，设备记录订阅者正常，100s后测试状态同步正常。")
    # 前端工装断电重启，模拟上电上报
    passed_time01 = power_control()
    start_time = time.time()
    panel01 = set_subscriber("订阅者1", 21)
    panel02 = set_subscriber("订阅者2", 22)
    panel03 = set_subscriber("订阅者3", 23)
    engine.wait(3)
    engine.add_doc_info('此处需要进行状态同步验证，防止状态同步报文影响后续的上电上报验证')
    report_subscribe_expect(devices=[panel01, panel02, panel03], write_value="32", current_value="00")
    passed_time02 = time.time() - start_time
    engine.wait((68 - passed_time01 - passed_time02 - 1), allowed_message=False)
    engine.add_doc_info('上电上报前进行状态同步，上电上报被打断，不再上报')
    engine.wait(125, allowed_message=False)
    engine.add_doc_info('上电上报前被控制，设备记录订阅者正常，等待上电上报测试结束，测试状态同步正常。')
    report_subscribe_expect(devices=[panel01, panel02, panel03], write_value="00", current_value="32")

    engine.add_doc_info("6、测试上电上报重试的过程中，是否可以正常被控制通断"
                        "（控制正常，被控制后，本产品状态同步正常，添加上报被打断，不再重试）"
                        "上电上报重试过程中被控制，设备记录订阅者正常，100s后测试状态同步正常。")
    # sid = 8时，上电上报时间 = 60+sid% 100 =68s
    report_power_on_expect(wait_times=[68, 10], ack=False, wait_enable=False)
    # 上电上报100s重试前可以被正常控制通断，正常状态同步
    panel01 = set_subscriber("订阅者1", 21)
    panel02 = set_subscriber("订阅者2", 22)
    panel03 = set_subscriber("订阅者3", 23)
    engine.wait(3)
    engine.add_doc_info('此处需要进行状态同步验证，防止状态同步报文影响后续的上电上报验证')
    report_subscribe_expect(devices=[panel01, panel02, panel03], write_value="32", current_value="00")
    engine.wait(100, allowed_message=False, tips='上电上报100s重试前进行状态同步，上电上报重试被打断，不再上报')
    engine.add_doc_info('上电上报重试过程中被控制，设备记录订阅者正常，100s后测试状态同步正常')
    report_subscribe_expect(devices=[panel01, panel02, panel03], write_value="00", current_value="32")

    engine.add_doc_info("7、窗帘控制模块开度为0的情况，上述已验证，再次测试窗帘控制模块开度为100%的情况，进行上电上报测试；")
    engine.add_doc_info('将窗帘控制模块开度设置为100，验证上电上报正常')
    report_subscribe_expect(devices=[panel01, panel02, panel03], write_value="64", current_value="00")
    report_power_on_expect(expect_value="64", wait_times=[68], ack=True)

    engine.add_doc_info('断电重启后订阅者信息丢失，将窗帘控制模块开度设置为0')
    report_subscribe_expect(devices=[], write_value="00", current_value="64")

    engine.report_check_enable_all(False)  # 关闭上报检测


def test_配置订阅者():
    """
    04_配置订阅者信息
        本设备方案为STM8方案，断电重启，上电上报前和上电上报重试过程中，状态同步均正常，不受影响；
    1、配置无订阅者，测试开关控制模块是否有上报信息；
    2、配置1个订阅者，测试开关控制模块上报是否正常；
    3、配置2个订阅者，测试开关控制模块上报是否正常；
    4、配置3个订阅者，测试开关控制模块上报是否正常；
    5、测试断电后订阅者信息会丢失；
    6、对于开的设备，重复发开，或者对于关的设备，重复发关的命令，窗帘控制模块也会触发状态同步；
    """
    engine.report_check_enable_all(True)  # 打开上报检测
    # 上电配置无订阅者时：使用网关控制后，只回复网关，不上报其他设备
    engine.add_doc_info('本设备方案为STM8方案，断电重启，上电上报完成前，状态同步上报被中断，需要等待上电上报结束后，状态同步上报恢复正常；')
    engine.add_doc_info("1、上电配置无订阅者时：使用网关控制后，只回复网关，不上报其他设备")
    report_power_on_expect(wait_times=[68], ack=True, wait_enable=False)
    report_subscribe_expect(devices=[], write_value="32", current_value="00")
    report_subscribe_expect(devices=[], write_value="00", current_value="32")

    engine.add_doc_info("2、配置1个订阅者：使用网关控制后，立即回复网关，然后按顺序上报订阅者")
    report_power_on_expect(wait_times=[68], ack=True, wait_enable=False)
    panel01 = set_subscriber("订阅者1", 21)
    report_subscribe_expect(devices=[panel01], write_value="32", current_value="00")
    report_subscribe_expect(devices=[panel01], write_value="00", current_value="32")

    engine.add_doc_info("3、配置2个订阅者：使用网关控制后，立即回复网关，然后按顺序上报订阅者")
    report_power_on_expect(wait_times=[68], ack=True, wait_enable=False)
    panel01 = set_subscriber("订阅者1", 21)
    panel02 = set_subscriber("订阅者2", 22)
    report_subscribe_expect(devices=[panel01, panel02], write_value="32", current_value="00")
    report_subscribe_expect(devices=[panel01, panel02], write_value="00", current_value="32")

    engine.add_doc_info("4、配置3个订阅者：使用网关控制后，立即回复网关，然后按顺序上报订阅者")
    report_power_on_expect(wait_times=[68], ack=True, wait_enable=False)
    panel01 = set_subscriber("订阅者1", 21)
    panel02 = set_subscriber("订阅者2", 22)
    panel03 = set_subscriber("订阅者3", 23)
    report_subscribe_expect(devices=[panel01, panel02, panel03], write_value="32", current_value="00")
    report_subscribe_expect(devices=[panel01, panel02, panel03], write_value="00", current_value="32")

    engine.add_doc_info('5、测试断电后订阅者信息会丢失，在3个订阅者的基础上，进行断电重启，'
                        '网关再次控制设备，只上报网关，不上报订阅者；')
    report_power_on_expect(wait_times=[68], ack=True, wait_enable=False)
    report_subscribe_expect(devices=[], write_value="32", current_value="00")
    report_subscribe_expect(devices=[], write_value="00", current_value="32")

    engine.add_doc_info('6、对于开度0的设备，重复发开度0，或者对于开度100的设备，重复发开度100的命令，窗帘控制模块也会触发状态同步；')
    report_power_on_expect(wait_times=[68], ack=True, wait_enable=False)
    panel01 = set_subscriber("订阅者1", 21)
    panel02 = set_subscriber("订阅者2", 22)
    panel03 = set_subscriber("订阅者3", 23)
    engine.add_doc_info('将窗帘控制模块开度设置为100')
    report_subscribe_expect(devices=[panel01, panel02, panel03], write_value="64", current_value="00")
    engine.add_doc_info('对于开度100的设备，重复发开度100的命令，也会触发状态同步')
    report_subscribe_expect(devices=[panel01, panel02, panel03], write_value="64", current_value="64")
    engine.add_doc_info('将窗帘控制模块开度设置为0')
    report_subscribe_expect(devices=[panel01, panel02, panel03], write_value="00", current_value="64")
    engine.add_doc_info('对于开度0的设备，重复发开度0的命令，也会触发状态同步')
    report_subscribe_expect(devices=[panel01, panel02, panel03], write_value="00", current_value="00")

    engine.report_check_enable_all(False)  # 关闭上报检测


def test_订阅者上报顺序测试():
    """
    05_订阅者上报顺序测试
    当存在多个订阅者（大于3个订阅者时），新增的订阅者会替换最早添加的订阅者；
    以订阅1、订阅者2、订阅者3、订阅4进行测试验证
    """
    engine.report_check_enable_all(True)  # 打开上报检测
    engine.add_doc_info("1、订阅者1、订阅者2、订阅者3依次控制，发现上报的顺序为订阅者1、订阅者2、订阅者3")
    engine.add_doc_info("配置3个订阅者时：")
    report_power_on_expect(wait_times=[68], ack=True, wait_enable=False)
    panel01 = set_subscriber("订阅者1", 21)
    panel02 = set_subscriber("订阅者2", 22)
    panel03 = set_subscriber("订阅者3", 23)

    report_subscribe_expect([panel01, panel02, panel03], write_value="32", current_value="00")
    report_subscribe_expect([panel01, panel02, panel03], write_value="00", current_value="32")

    engine.add_doc_info("2、订阅者4控制一次，发现上报的顺序变成订阅者4、订阅者2、订阅者3")
    panel04 = set_subscriber("订阅者4", 24)
    report_subscribe_expect([panel04, panel02, panel03], write_value="32", current_value="00")
    report_subscribe_expect([panel04, panel02, panel03], write_value="00", current_value="32")

    engine.add_doc_info("3、订阅者1控制一次，发现上报的顺序变成订阅者4、订阅者1、订阅者3")
    panel01 = set_subscriber("订阅者1", 21)
    report_subscribe_expect([panel04, panel01, panel03], write_value="32", current_value="00")
    report_subscribe_expect([panel04, panel01, panel03], write_value="00", current_value="32")

    engine.add_doc_info("4、订阅者2控制一次，发现上报的顺序变成订阅者4、订阅者1、订阅者2")
    panel02 = set_subscriber("订阅者2", 22)
    report_subscribe_expect([panel04, panel01, panel02], write_value="32", current_value="00")
    report_subscribe_expect([panel04, panel01, panel02], write_value="00", current_value="32")

    engine.add_doc_info("5、订阅者3控制一次，发现上报的顺序变成订阅者3、订阅者1、订阅者2")
    panel03 = set_subscriber("订阅者3", 23)
    report_subscribe_expect([panel03, panel01, panel02], write_value="32", current_value="00")
    report_subscribe_expect([panel03, panel01, panel02], write_value="00", current_value="32")

    engine.report_check_enable_all(False)  # 关闭上报检测


def test_默认参数同时上报设备和网关():
    """
    06_默认参数同时上报设备和网关
    1、窗帘控制模块不支持本地控制；
    2、手机客户端单点控制（网关控制）——被控设备状态立即回复网关，1.3s后状态同步依次同步给订阅者和网关，到达指定位置后，再次同步给订阅者和网关；
    3、手机客户端情景模式控制（网关控制）——被控设备状态按组地址顺序上报，状态同步依次同步给订阅者和网关，到达指定位置后，再次同步给订阅者和网关；
    4、订阅者01单点控制——被控设备状态立即回复订阅者01，1.3s后状态同步依次同步给订阅者和网关，到达指定位置后，再次同步给订阅者和网关；
    5、订阅者01情景模式控制——被控设备状态按组地址顺序上报，状态同步依次同步给订阅者和网关，到达指定位置后，再次同步给订阅者和网关；
    """
    engine.report_check_enable_all(True)  # 打开上报检测
    report_power_on_expect(wait_times=[68], ack=True, wait_enable=False)

    engine.send_did("READ", "主动上报使能标志D005")
    engine.expect_did("READ", "主动上报使能标志D005", 传感器类型="未知", 上报命令="同时上报设备和网关")
    # 配置订阅者3个
    panel01 = set_subscriber("订阅者1", 21)
    panel02 = set_subscriber("订阅者2", 22)
    panel03 = set_subscriber("订阅者3", 23)

    engine.add_doc_info("1、窗帘控制模块不支持本地控制；")

    engine.add_doc_info("2、手机客户端单点控制（网关控制）——被控设备状态立即回复网关，1.3s后状态同步依次同步给订阅者和网关，到达指定位置后，再次同步给订阅者和网关；")
    report_subscribe_expect([panel01, panel02, panel03], write_value="32", current_value="00",
                            scene_type="网关单点控制")
    report_subscribe_expect([panel01, panel02, panel03], write_value="00", current_value="32",
                            scene_type="网关单点控制")

    engine.add_doc_info("3、手机客户端情景模式控制（网关控制）——被控设备状态按组地址顺序上报，状态同步依次同步给订阅者和网关，到达指定位置后，再次同步给订阅者和网关；")
    report_subscribe_expect([panel01, panel02, panel03], write_value="32", current_value="00",
                            first_timeout=3.3, scene_type="网关情景模式控制")
    report_subscribe_expect([panel01, panel02, panel03], write_value="00", current_value="32",
                            first_timeout=3.3, scene_type="网关情景模式控制")

    engine.add_doc_info("4、订阅者01单点控制——被控设备状态立即回复订阅者01，1.3s后状态同步依次同步给订阅者和网关，到达指定位置后，再次同步给订阅者和网关；")
    report_subscribe_expect([panel01, panel02, panel03], write_value="32", current_value="00",
                            scene_type="订阅者01单点控制")
    report_subscribe_expect([panel01, panel02, panel03], write_value="00", current_value="32",
                            scene_type="订阅者01单点控制")

    engine.add_doc_info("5、订阅者01情景模式控制——被控设备状态按组地址顺序上报，状态同步依次同步给订阅者和网关，到达指定位置后，再次同步给订阅者和网关；")
    report_subscribe_expect([panel01, panel02, panel03], write_value="32", current_value="00",
                            first_timeout=3.3, scene_type="订阅者01情景模式控制")
    report_subscribe_expect([panel01, panel02, panel03], write_value="00", current_value="32",
                            first_timeout=3.3, scene_type="订阅者01情景模式控制")

    engine.report_check_enable_all(False)  # 关闭上报检测


def test_不上报():
    """
    07_不上报
    1、窗帘控制模块不支持本地控制；
    2、手机客户端单点控制（网关控制）——被控设备状态立即回复网关，状态同步不上报订阅者；
    3、手机客户端情景模式控制（网关控制）——不上报订阅者和网关；
    4、订阅者01单点控制——被控设备状态立即回复订阅者01，不上报订阅者和网关；
    5、订阅者01情景模式控制——不上报订阅者和网关；
    """
    engine.report_check_enable_all(True)  # 打开上报检测
    report_power_on_expect(wait_times=[68], ack=True, wait_enable=False)
    # 设置为不上报模式
    engine.send_did("WRITE", "主动上报使能标志D005", 传感器类型="未知", 上报命令="无上报")
    engine.expect_did("WRITE", "主动上报使能标志D005", 传感器类型="未知", 上报命令="无上报")
    engine.send_did("READ", "主动上报使能标志D005")
    engine.expect_did("READ", "主动上报使能标志D005", 传感器类型="未知", 上报命令="无上报")

    # 配置订阅者3个
    panel01 = set_subscriber("订阅者1", 21)
    panel02 = set_subscriber("订阅者2", 22)
    panel03 = set_subscriber("订阅者3", 23)

    engine.add_doc_info("1、窗帘控制模块不支持本地控制；")

    engine.add_doc_info("2、手机客户端单点控制（网关控制）——被控设备状态立即回复网关，状态同步不上报订阅者")
    report_subscribe_expect([panel01, panel02, panel03], write_value="32", current_value="00",
                            report_subscribe=False, report_gateway=False, scene_type="网关单点控制")
    report_subscribe_expect([panel01, panel02, panel03], write_value="00", current_value="32",
                            report_subscribe=False, report_gateway=False, scene_type="网关单点控制")

    engine.add_doc_info("3、手机客户端情景模式控制（网关控制）——不上报订阅者和网关")
    report_subscribe_expect([panel01, panel02, panel03], write_value="32", current_value="00", first_timeout=3.3,
                            report_subscribe=False, report_gateway=False, scene_type="网关情景模式控制")
    report_subscribe_expect([panel01, panel02, panel03], write_value="00", current_value="32", first_timeout=3.3,
                            report_subscribe=False, report_gateway=False, scene_type="网关情景模式控制")

    engine.add_doc_info("4、订阅者01单点控制——被控设备状态立即回复订阅者01，不上报其他订阅者和网关")
    report_subscribe_expect([panel01, panel02, panel03], write_value="32", current_value="00",
                            report_subscribe=False, report_gateway=False, scene_type="订阅者01单点控制")
    report_subscribe_expect([panel01, panel02, panel03], write_value="00", current_value="32",
                            report_subscribe=False, report_gateway=False, scene_type="订阅者01单点控制")

    engine.add_doc_info("5、订阅者01情景模式控制——不上报订阅者和网关")
    report_subscribe_expect([panel01, panel02, panel03], write_value="32", current_value="00", first_timeout=3.3,
                            report_subscribe=False, report_gateway=False, scene_type="订阅者01情景模式控制")
    report_subscribe_expect([panel01, panel02, panel03], write_value="00", current_value="32", first_timeout=3.3,
                            report_subscribe=False, report_gateway=False, scene_type="订阅者01情景模式控制")

    engine.report_check_enable_all(False)  # 关闭上报检测


def test_只上报网关():
    """
    08_只上报网关
    1、窗帘控制模块不支持本地控制；
    2、手机客户端单点控制（网关控制）——被控设备状态立即回复网关，1.3s后状态同步不上报订阅者，上报网关，到达指定位置后，再次上报网关；
    3、手机客户端情景模式控制（网关控制）——被控设备状态按组地址顺序上报，状态同步不上报订阅者，只上报网关，到达指定位置后，再次上报网关；
    4、订阅者01单点控制——被控设备状态立即回复订阅者01，1.3s后状态同步不上报订阅者，上报网关，到达指定位置后，再次上报网关；
    5、订阅者01情景模式控制——被控设备状态按组地址顺序上报，状态同步不上报订阅者，只上报网关，到达指定位置后，再次上报网关；
    """
    engine.report_check_enable_all(True)  # 打开上报检测
    report_power_on_expect(wait_times=[68], ack=True, wait_enable=False)
    # 设置为只上报网关模式
    engine.send_did("WRITE", "主动上报使能标志D005", 传感器类型="未知", 上报命令="上报网关")
    engine.expect_did("WRITE", "主动上报使能标志D005", 传感器类型="未知", 上报命令="上报网关")
    engine.send_did("READ", "主动上报使能标志D005")
    engine.expect_did("READ", "主动上报使能标志D005", 传感器类型="未知", 上报命令="上报网关")

    # 配置订阅者3个
    panel01 = set_subscriber("订阅者1", 21)
    panel02 = set_subscriber("订阅者2", 22)
    panel03 = set_subscriber("订阅者3", 23)

    engine.add_doc_info("1、窗帘控制模块不支持本地控制；")

    engine.add_doc_info("2、手机客户端单点控制（网关控制）——被控设备状态立即回复网关，1.3s后状态同步不上报订阅者，上报网关，到达指定位置后，再次上报网关；")
    report_subscribe_expect([panel01, panel02, panel03], write_value="32", current_value="00",
                            report_subscribe=False, report_gateway=True, scene_type="网关单点控制")
    report_subscribe_expect([panel01, panel02, panel03], write_value="00", current_value="32",
                            report_subscribe=False, report_gateway=True, scene_type="网关单点控制")

    engine.add_doc_info("3、手机客户端情景模式控制（网关控制）——被控设备状态按组地址顺序上报，状态同步不上报订阅者，只上报网关，到达指定位置后，再次上报网关；")
    report_subscribe_expect([panel01, panel02, panel03], write_value="32", current_value="00", first_timeout=3.3,
                            report_subscribe=False, report_gateway=True, scene_type="网关情景模式控制")
    report_subscribe_expect([panel01, panel02, panel03], write_value="00", current_value="32", first_timeout=3.3,
                            report_subscribe=False, report_gateway=True, scene_type="网关情景模式控制")

    engine.add_doc_info("4、订阅者01单点控制——被控设备状态立即回复订阅者01，1.3s后状态同步不上报订阅者，上报网关，到达指定位置后，再次上报网关；")
    report_subscribe_expect([panel01, panel02, panel03], write_value="32", current_value="00",
                            report_subscribe=False, report_gateway=True, scene_type="订阅者01单点控制")
    report_subscribe_expect([panel01, panel02, panel03], write_value="00", current_value="32",
                            report_subscribe=False, report_gateway=True, scene_type="订阅者01单点控制")

    engine.add_doc_info("5、订阅者01情景模式控制——被控设备状态按组地址顺序上报，状态同步不上报订阅者，只上报网关，到达指定位置后，再次上报网关；")
    report_subscribe_expect([panel01, panel02, panel03], write_value="32", current_value="00", first_timeout=3.3,
                            report_subscribe=False, report_gateway=True, scene_type="订阅者01情景模式控制")
    report_subscribe_expect([panel01, panel02, panel03], write_value="00", current_value="32", first_timeout=3.3,
                            report_subscribe=False, report_gateway=True, scene_type="订阅者01情景模式控制")

    engine.report_check_enable_all(False)  # 关闭上报检测


def test_只上报设备():
    """
    09_只上报设备
    1、窗帘控制模块不支持本地控制；
    2、手机客户端单点控制（网关控制）——被控设备状态立即回复网关，状态同步只上报订阅者，不上报网关，到达指定位置后，再次只上报订阅者；
    3、手机客户端情景模式控制（网关控制）——被控设备状态按组地址顺序上报，状态同步只上报订阅者，不上报网关，到达指定位置后，再次只上报订阅者；
    4、订阅者01单点控制——被控设备状态立即回复订阅者01，状态同步只上报订阅者，不上报网关，到达指定位置后，再次只上报订阅者；
    5、订阅者01情景模式控制——被控设备状态按组地址顺序上报，状态同步只上报订阅者，不上报网关，到达指定位置后，再次只上报订阅者；
    """
    engine.report_check_enable_all(True)  # 打开上报检测
    report_power_on_expect(wait_times=[68], ack=True, wait_enable=False)
    # 设置为只上报网关模式
    engine.add_doc_info("设置为只上报网关模式")
    engine.send_did("WRITE", "主动上报使能标志D005", 传感器类型="未知", 上报命令="上报设备")
    engine.expect_did("WRITE", "主动上报使能标志D005", 传感器类型="未知", 上报命令="上报设备")
    engine.send_did("READ", "主动上报使能标志D005")
    engine.expect_did("READ", "主动上报使能标志D005", 传感器类型="未知", 上报命令="上报设备")
    # 配置订阅者3个
    panel01 = set_subscriber("订阅者1", 21)
    panel02 = set_subscriber("订阅者2", 22)
    panel03 = set_subscriber("订阅者3", 23)

    engine.add_doc_info("1、窗帘控制模块不支持本地控制；")

    engine.add_doc_info("2、手机客户端单点控制（网关控制）——被控设备状态立即回复网关，状态同步只上报订阅者，不上报网关，到达指定位置后，再次只上报订阅者；")
    report_subscribe_expect([panel01, panel02, panel03], write_value="32", current_value="00",
                            report_subscribe=True, report_gateway=False, scene_type="网关单点控制")
    report_subscribe_expect([panel01, panel02, panel03], write_value="00", current_value="32",
                            report_subscribe=True, report_gateway=False, scene_type="网关单点控制")

    engine.add_doc_info("3、手机客户端情景模式控制（网关控制）——被控设备状态按组地址顺序上报，状态同步只上报订阅者，不上报网关，到达指定位置后，再次只上报订阅者；")
    report_subscribe_expect([panel01, panel02, panel03], write_value="32", current_value="00", first_timeout=3.3,
                            report_subscribe=True, report_gateway=False, scene_type="网关情景模式控制")
    report_subscribe_expect([panel01, panel02, panel03], write_value="00", current_value="32", first_timeout=3.3,
                            report_subscribe=True, report_gateway=False, scene_type="网关情景模式控制")

    engine.add_doc_info("4、订阅者01单点控制——被控设备状态立即回复订阅者01，状态同步只上报订阅者，不上报网关，到达指定位置后，再次只上报订阅者；")
    report_subscribe_expect([panel01, panel02, panel03], write_value="32", current_value="00",
                            report_subscribe=True, report_gateway=False, scene_type="订阅者01单点控制")
    report_subscribe_expect([panel01, panel02, panel03], write_value="00", current_value="32",
                            report_subscribe=True, report_gateway=False, scene_type="订阅者01单点控制")

    engine.add_doc_info("5、订阅者01情景模式控制——被控设备状态按组地址顺序上报，状态同步只上报订阅者，不上报网关，到达指定位置后，再次只上报订阅者；")
    report_subscribe_expect([panel01, panel02, panel03], write_value="32", current_value="00", first_timeout=3.3,
                            report_subscribe=True, report_gateway=False, scene_type="订阅者01情景模式控制")
    report_subscribe_expect([panel01, panel02, panel03], write_value="00", current_value="32", first_timeout=3.3,
                            report_subscribe=True, report_gateway=False, scene_type="订阅者01情景模式控制")

    engine.report_check_enable_all(False)  # 关闭上报检测


def test_网关无应答时设备上报的重试机制():
    """
    10_网关无应答时设备上报的重试机制
    在默认参数同时上报设备和网关情况下测试：
    1、测试正常情况，网关正常应答
    2、测试网关不应答异常情况，进行10s、100s重试，重试结束则本次添加上报结束
    3、如果10s重试上报过程中，收到网关应答，不再进行100重试上报
    4、上报过程中，收到新的控制命令，本次重试上报结束，开始新的上报流程
    5、如果10s重试上报过程中，收到新的控制命令，本次重试上报结束，开始新的上报流程
    6、如果100s重试上报过程中，收到新的控制命令，本次重试上报结束，开始新的上报流程
    """
    engine.report_check_enable_all(True)  # 打开上报检测
    report_power_on_expect(wait_times=[68], ack=True, wait_enable=False)
    # 设置为同时上报设备和网关模式
    engine.add_doc_info("设置为同时上报设备和网关模式")
    engine.send_did("WRITE", "主动上报使能标志D005", 传感器类型="未知", 上报命令="同时上报设备和网关")
    engine.expect_did("WRITE", "主动上报使能标志D005", 传感器类型="未知", 上报命令="同时上报设备和网关")
    engine.send_did("READ", "主动上报使能标志D005")
    engine.expect_did("READ", "主动上报使能标志D005", 传感器类型="未知", 上报命令="同时上报设备和网关")
    # 配置订阅者3个
    panel01 = set_subscriber("订阅者1", 21)
    panel02 = set_subscriber("订阅者2", 22)
    panel03 = set_subscriber("订阅者3", 23)
    engine.add_doc_info("1、测试正常情况，网关正常应答")
    report_subscribe_expect([panel01, panel02, panel03], write_value="32", current_value="00",
                            scene_type="网关单点控制")
    report_subscribe_expect([panel01, panel02, panel03], write_value="00", current_value="32",
                            scene_type="订阅者01单点控制")

    engine.add_doc_info("2、测试网关不应答异常情况，进行10s、100s重试，重试结束则本次添加上报结束")
    report_subscribe_expect([panel01, panel02, panel03], write_value="32", current_value="00",
                            scene_type="订阅者01单点控制", ack=False, wait_enable=False)
    engine.wait(9, allowed_message=False)
    engine.expect_multi_dids("REPORT",
                             "单轨窗帘目标开度0A03", '32',
                             "单轨窗帘当前开度0A05", '32',
                             "导致状态改变的控制设备AIDC01A", panel01.said, timeout=2)
    engine.wait(99, allowed_message=False)
    engine.expect_multi_dids("REPORT",
                             "单轨窗帘目标开度0A03", '32',
                             "单轨窗帘当前开度0A05", '32',
                             "导致状态改变的控制设备AIDC01A", panel01.said, timeout=2)
    engine.wait(100, allowed_message=False)

    report_subscribe_expect([panel01, panel02, panel03], write_value="00", current_value="32",
                            scene_type="订阅者01单点控制", ack=False, wait_enable=False)
    engine.wait(9, allowed_message=False)
    engine.expect_multi_dids("REPORT",
                             "单轨窗帘目标开度0A03", '00',
                             "单轨窗帘当前开度0A05", '00',
                             "导致状态改变的控制设备AIDC01A", panel01.said, timeout=2)
    engine.wait(99, allowed_message=False)
    engine.expect_multi_dids("REPORT",
                             "单轨窗帘目标开度0A03", '00',
                             "单轨窗帘当前开度0A05", '00',
                             "导致状态改变的控制设备AIDC01A", panel01.said, timeout=2)
    engine.wait(100, allowed_message=False)

    engine.add_doc_info("3、如果10s重试上报过程中，收到网关应答，不再进行100重试上报")
    report_subscribe_expect([panel01, panel02, panel03], write_value="32", current_value="00",
                            scene_type="订阅者01单点控制", ack=False, wait_enable=False)
    engine.wait(9, allowed_message=False)
    engine.expect_multi_dids("REPORT",
                             "单轨窗帘目标开度0A03", '32',
                             "单轨窗帘当前开度0A05", '32',
                             "导致状态改变的控制设备AIDC01A", panel01.said, timeout=2, ack=True)
    engine.wait(120, allowed_message=False)

    report_subscribe_expect([panel01, panel02, panel03], write_value="00", current_value="32",
                            scene_type="订阅者01单点控制", ack=False, wait_enable=False)
    engine.wait(9, allowed_message=False)
    engine.expect_multi_dids("REPORT",
                             "单轨窗帘目标开度0A03", '00',
                             "单轨窗帘当前开度0A05", '00',
                             "导致状态改变的控制设备AIDC01A", panel01.said, timeout=2, ack=True)
    engine.wait(120, allowed_message=False)

    engine.add_doc_info("4、上报过程中，收到新的控制命令，本次上报结束，开始新的上报流程")
    write_value = '32'
    current_value = '00'
    engine.add_doc_info("订阅者01单点控制")
    panel01.send_did("WRITE", "单轨窗帘目标开度0A03", '32')
    panel01.expect_did("WRITE", "单轨窗帘目标开度0A03", '32')

    panel01.expect_multi_dids("NOTIFY",
                              None, None, "单轨窗帘目标开度0A03", '32',
                              None, None, "单轨窗帘当前开度0A05", '00',
                              timeout=2)
    engine.add_doc_info("上报订阅者后，被控制，本次上报结束，开始新的上报流程")
    report_subscribe_expect([panel01, panel02, panel03], write_value="00", current_value="**",
                            scene_type="订阅者01单点控制")

    engine.add_doc_info('5、如果10s重试上报过程中，收到新的控制命令，本次重试上报结束，开始新的上报流程')
    report_subscribe_expect([panel01, panel02, panel03], write_value="32", current_value="00",
                            scene_type="订阅者01单点控制", ack=False, wait_enable=False)
    engine.wait(5, allowed_message=False)
    engine.add_doc_info("如果10s重试上报过程中，收到新的控制命令，本次重试上报结束，开始新的上报流程")
    report_subscribe_expect([panel01, panel02, panel03], write_value="00", current_value="32",
                            scene_type="订阅者01单点控制", ack=True)

    engine.add_doc_info("6、如果100s重试上报过程中，收到新的控制命令，本次重试上报结束，开始新的上报流程")
    report_subscribe_expect([panel01, panel02, panel03], write_value="32", current_value="00",
                            scene_type="订阅者01单点控制", ack=False, wait_enable=False)
    engine.wait(9, allowed_message=False)
    engine.expect_multi_dids("REPORT",
                             "单轨窗帘目标开度0A03", '32',
                             "单轨窗帘当前开度0A05", '32',
                             "导致状态改变的控制设备AIDC01A", panel01.said, timeout=2)
    engine.wait(50, allowed_message=False)
    engine.add_doc_info("如果100s重试上报过程中，收到新的控制命令，本次重试上报结束，开始新的上报流程")
    report_subscribe_expect([panel01, panel02, panel03], write_value="00", current_value="32",
                            scene_type="订阅者01单点控制", ack=True)

    engine.report_check_enable_all(False)  # 关闭上报检测


def test_广播报文控制测试():
    """
    11_广播报文控制测试
    1、组地址按位组合
    2、组地址按单字节组合
    3、组地址按双字节组合
    4、存在多个组地址的情况，组地址在前
    5、存在多个组地址的情况，组地址在后
    6、不同组地址混合 按单字节+按双字节+按位组合
    7、模拟220字节超长情景模式报文测试
    8、验证sid大于255的情况，sid=280情况下，按位、按双字节情景模式模式控制
    9、设置回常用的网关和PANID
    """
    engine.report_check_enable_all(True)  # 打开上报检测
    report_power_on_expect(wait_times=[68], ack=True, wait_enable=False)
    engine.add_doc_info("测试前准备工作，配置3个订阅者")
    # 配置订阅者3个
    panel01 = set_subscriber("订阅者1", 21)
    panel02 = set_subscriber("订阅者2", 22)
    panel03 = set_subscriber("订阅者3", 23)

    engine.add_doc_info("1、组地址按位组合")
    # 情景模式控制后，第一次上报时间为1.3+0.5*2=2.3s，允许1s误差存在
    report_broadcast_expect([panel01, panel02, panel03], write_value="32", current_value="00",
                            first_timeout=3.3, scene_type="组地址按位组合")
    report_broadcast_expect([panel01, panel02, panel03], write_value="00", current_value="32",
                            first_timeout=3.3, scene_type="组地址按位组合")

    engine.add_doc_info("2、组地址按单字节组合")
    # 情景模式控制后，第一次上报时间为1.3+0.5*2=2.3s，允许1s误差存在
    report_broadcast_expect([panel01, panel02, panel03], write_value="32", current_value="00",
                            first_timeout=3.3, scene_type="组地址按单字节组合")
    report_broadcast_expect([panel01, panel02, panel03], write_value="00", current_value="32",
                            first_timeout=3.3, scene_type="组地址按单字节组合")

    engine.add_doc_info("3、组地址按双字节组合")
    # 情景模式控制后，第一次上报时间为1.3+0.5*2=2.3s，允许1s误差存在
    report_broadcast_expect([panel01, panel02, panel03], write_value="32", current_value="00",
                            first_timeout=3.3, scene_type="组地址按双字节组合")
    report_broadcast_expect([panel01, panel02, panel03], write_value="00", current_value="32",
                            first_timeout=3.3, scene_type="组地址按双字节组合")

    engine.add_doc_info("4、存在多个组地址的情况，组地址在前")
    # 情景模式控制后，第一次上报时间为1.3+0.5*2=2.3s，允许1s误差存在
    report_broadcast_expect([panel01, panel02, panel03], write_value="32", current_value="00",
                            first_timeout=3.3, scene_type="存在多个组地址的情况，组地址在前")
    report_broadcast_expect([panel01, panel02, panel03], write_value="00", current_value="32",
                            first_timeout=3.3, scene_type="存在多个组地址的情况，组地址在前")

    engine.add_doc_info("5、存在多个组地址的情况，组地址在后")
    # 情景模式控制后，第一次上报时间为1.3+0.5*12=7.3s，允许1s误差存在
    report_broadcast_expect([panel01, panel02, panel03], write_value="32", current_value="00",
                            first_timeout=8.3, scene_type="存在多个组地址的情况，组地址在后")
    report_broadcast_expect([panel01, panel02, panel03], write_value="00", current_value="32",
                            first_timeout=8.3, scene_type="存在多个组地址的情况，组地址在后")

    engine.add_doc_info("6、不同组地址混合 按单字节+按双字节+按位组合")
    # 情景模式控制后，第一次上报时间为1.3+0.5*2=2.3s，允许1s误差存在
    report_broadcast_expect([panel01, panel02, panel03], write_value="32", current_value="00",
                            first_timeout=3.3, scene_type="不同组地址混合 按单字节+按双字节+按位组合")
    report_broadcast_expect([panel01, panel02, panel03], write_value="00", current_value="32",
                            first_timeout=3.3, scene_type="不同组地址混合 按单字节+按双字节+按位组合")

    engine.add_doc_info("7、模拟220字节超长情景模式报文测试")
    # 网关发送情景模式报文，最长为220个字节，使报文长度接近220个字节，下列为219个字节
    # 情景模式控制后，第一次上报时间为1.3+0.5*76=39.3s，允许1s误差存在
    engine.add_doc_info('超长报文控制时，如果设置的开度较小，在上报前窗帘控制模块动作完成，就会出现窗帘上报第一轮不上报，只上报第二轮最终结果的现象，'
                        '为了统一测试流程，此时将开度设置为100，便于统一测试')
    report_broadcast_expect([panel01, panel02, panel03], write_value="64", current_value="00",
                            first_timeout=40.3, scene_type="模拟220字节超长情景模式报文测试")
    report_broadcast_expect([panel01, panel02, panel03], write_value="00", current_value="64",
                            first_timeout=40.3, scene_type="模拟220字节超长情景模式报文测试")

    engine.add_doc_info("8、验证sid大于255的情况，sid=280情况下，按位、按双字节情景模式模式控制")
    engine.add_doc_info('sid大于255时，超出单字节范围，单字节无法表示，所以不需要验证按单字节情景模式控制')

    set_gw_info(panid=1100, sid=280)
    engine.wait(15, allowed_message=False)
    engine.add_doc_info('重新入网后，订阅者信息被清除，需要重新控制，添加3个订阅者')
    # 配置订阅者3个
    panel01 = set_subscriber("订阅者1", 21)
    panel02 = set_subscriber("订阅者2", 22)
    panel03 = set_subscriber("订阅者3", 23)

    # 情景模式控制后，第一次上报时间为1.3+0.5*4=3.3s，允许1s误差存在
    report_broadcast_expect([panel01, panel02, panel03], write_value="32", current_value="00",
                            first_timeout=4.3, scene_type="sid大于255，组地址按位组合")
    report_broadcast_expect([panel01, panel02, panel03], write_value="00", current_value="32",
                            first_timeout=4.3, scene_type="sid大于255，组地址按位组合")

    report_broadcast_expect([panel01, panel02, panel03], write_value="32", current_value="00",
                            first_timeout=4.3, scene_type="sid大于255，组地址按双字节组合")
    report_broadcast_expect([panel01, panel02, panel03], write_value="00", current_value="32",
                            first_timeout=4.3, scene_type="sid大于255，组地址按双字节组合")

    engine.add_doc_info('9、设置回常用的网关信息和PANID')
    set_gw_info()
    engine.report_check_enable_all(False)  # 关闭上报检测


def test_状态同步干扰测试():
    """
    12_状态同步干扰测试
    1、干扰报文为广播报文，报文中的sid不包含被测设备的sid。窗帘控制模块状态同步过程中，收到干扰报文，上报的C01A 不受干扰报文影响；
    :return:
    """
    engine.report_check_enable_all(True)  # 打开上报检测
    report_power_on_expect(wait_times=[68], ack=True, wait_enable=False)
    engine.add_doc_info("测试前准备工作，配置3个订阅者")
    # 配置订阅者3个
    panel01 = set_subscriber("订阅者1", 21)
    panel02 = set_subscriber("订阅者2", 22)
    panel03 = set_subscriber("订阅者3", 23)

    engine.add_doc_info('1、干扰报文为广播报文，报文中的sid不包含被测设备的sid。窗帘控制模块状态同步过程中，收到干扰报文，上报的C01A 不受干扰报文影响；')
    # 情景模式控制后，第一次上报时间为1.3+0.5*2=2.3s，允许1s误差存在
    report_broadcast_expect([panel01, panel02, panel03], write_value="32", current_value="00",
                            first_timeout=3.3, scene_type="组地址按位组合", interfere_enable=True)
    report_broadcast_expect([panel01, panel02, panel03], write_value="00", current_value="32",
                            first_timeout=3.3, scene_type="组地址按位组合", interfere_enable=True)

    engine.report_check_enable_all(False)  # 关闭上报检测


def test_超长报文频繁干扰测试():
    """
    13_超长报文频繁干扰测试
    1、连续频繁发送超长广播干扰报文，连续发送500次，间隔1s，模拟载波环境复杂，报文较多的情况；
    2、发送完毕，抄读窗帘控制模块软件版本，控制窗帘控制模块动作，要求查询正常，控制测试正常；

    :return:
    """

    engine.report_check_enable_all(True)  # 打开上报检测
    report_power_on_expect(wait_times=[68], ack=True, wait_enable=False)
    engine.add_doc_info("测试前准备工作，配置3个订阅者")
    # 配置订阅者3个
    panel01 = set_subscriber("订阅者1", 21)
    panel02 = set_subscriber("订阅者2", 22)
    panel03 = set_subscriber("订阅者3", 23)

    engine.add_doc_info('1、连续频繁发送超长广播干扰报文，包括被测设备sid=8，连续发送500次，间隔1s，模拟载波环境复杂，报文较多的情况，'
                        '测试被测设备不会因为载波报文过多导致死机，仍保持正常工作；')
    for i in range(500):
        engine.broadcast_send_multi_dids("WRITE",
                                         [6, 7, 9, 10, 11, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171,
                                          180, 181, 182, 183, 184, 185, 186, 187], "U16", "通断操作C012", "88",
                                         [6, 7, 9, 10, 11, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171,
                                          180, 181, 182, 183, 184, 185, 186, 187, 188], "U16", "通断操作C012", "84",
                                         [6, 7, 9, 10, 11, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171,
                                          180, 181, 182, 183, 184, 185, 186, 187, 188], "U16", "通断操作C012", "82",
                                         [7, 8, 9, 10, 11, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171,
                                          180, 181, 182, 183, 184, 185, 186, 187, 188], "U16", "单轨窗帘目标开度0A03",
                                         '00')
        engine.wait(1, tips='发送广播报文第{}轮结束，不需要考虑回复，发送频率为1s/每次'.format(i + 1))

    engine.add_doc_info('2、发送完毕，抄读窗帘控制模块软件版本，控制窗帘控制模块动作，要求查询正常，控制测试正常；')
    engine.send_did("READ", "设备描述信息设备制造商0003")
    engine.expect_did("READ", "设备描述信息设备制造商0003", config["设备描述信息设备制造商0003"])
    report_broadcast_expect([panel01, panel02, panel03], write_value="32", current_value="00",
                            first_timeout=3.3, scene_type="组地址按位组合")
    report_broadcast_expect([panel01, panel02, panel03], write_value="00", current_value="32",
                            first_timeout=3.3, scene_type="组地址按位组合")

    engine.report_check_enable_all(False)  # 关闭上报检测
