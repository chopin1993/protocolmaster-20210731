# encoding:utf-8
# 导入测试引擎
from .常用测试模块 import *

测试组说明 = "状态同步测试"

config = engine.get_config()


def test_添加上报():
    """
    01_添加上报测试
    1、设备收到网关发送的注册帧后等15s（允许1s误差）以后开始上报
    2、设备添加上报后，收不到网关应答，进行10s、100s重试，重试结束则本次添加上报结束
    3、如果10s重试上报过程中，收到网关应答，不再进行100s重试上报
    4、测试添加网关后，添加上报前，是否可以正常被查询或设置参数（查询或设置参数正常，添加上报仍继续）
    5、测试添加上报重试的过程中，是否可以正常被查询或设置参数（查询或设置参数正常，添加上报仍继续）
    6、传感器处于无人低光照的状态上述已验证，再次测试传感器处于有人高光照状态，进行添加上报测试；
    """
    engine.report_check_enable_all(True)  # 打开上报检测
    engine.add_doc_info("1、设备收到网关发送的注册帧后等15s（允许1s误差）以后开始上报")
    report_gateway_expect(wait_times=[15], ack=True, quit_net=True)

    engine.add_doc_info("2、设备添加上报后，收不到网关应答，进行10s、100s重试，重试结束则本次添加上报结束")
    report_gateway_expect(wait_times=[15, 10, 100], ack=False, quit_net=True)

    engine.add_doc_info("3、如果10s重试上报过程中，收到网关应答，不再进行100s重试上报")
    report_gateway_expect(wait_times=[15, 10], ack=True, quit_net=True)

    engine.add_doc_info("4、测试添加网关后，添加上报前，是否可以正常被查询或设置参数（查询或设置参数正常，添加上报仍继续）")
    set_gw_info()  # 模拟设备入网
    passed_time = read_write_test()
    engine.wait((15 - passed_time - 1), allowed_message=False)
    engine.expect_multi_dids("REPORT",
                             "读传感器数据B701", "09 00",
                             "读传感器数据B701", '0B ** **', ack=True)
    engine.wait(125, allowed_message=False)
    engine.send_did("WRITE", "退网通知060B", 退网设备=config["测试设备地址"])

    engine.add_doc_info("5、测试添加上报重试的过程中，是否可以正常被查询或设置参数（查询或设置参数正常，添加上报仍继续）")
    report_gateway_expect(wait_times=[15], ack=False, wait_enable=False)
    engine.wait(3, allowed_message=False)
    passed_time = read_write_test()
    engine.wait((10 - passed_time - 3 - 1), allowed_message=False)
    engine.expect_multi_dids("REPORT",
                             "读传感器数据B701", "09 00",
                             "读传感器数据B701", '0B ** **', ack=True)
    engine.wait(125, allowed_message=False)
    engine.send_did("WRITE", "退网通知060B", 退网设备=config["测试设备地址"])

    engine.add_doc_info("6、传感器处于无人低光照的状态上述已验证，再次测试传感器处于有人高光照状态，进行添加上报测试；")
    engine.add_doc_info('因为人体红外感应器不支持SWB协议，所以无法设置传感器有无人参数和光照度参数。'
                        '目前该情况无法自动测试，需要人为补充测试。')
    # report_gateway_expect(expect_value="01", wait_times=[15], ack=True)

    engine.report_check_enable_all(False)  # 关闭上报检测


def test_上电上报():
    """
    02_上电上报测试
    上电上报计算公式：上电上报等待时间（以下简称T）：T=A min + X s，其中A为传感器无效时间（以下简称A），
    X = sid%min(100，freq1，freq2)。req1、freq2是0B、09的上报频率。
    1、测试默认上报频率为0时，测试sid < 100的情况，sid = 8的情况下，测试网关正常上报的情况
    2、测试默认上报频率为0时，测试sid > 100的情况，sid = 320的情况下，测试网关正常上报的情况
    3、测试上报重发机制，收不到网关应答，进行10s、100s重试，重试结束则本次上电上报
    4、如果10s重试上报过程中，收到网关应答，不再进行100重试上报
    5、测试上电上报前的过程中，是否可以正常被查询或设置参数（查询或设置参数正常，上电上报仍继续）
    6、测试上电上报重试的过程中，是否可以正常被查询或设置参数（查询或设置参数正常，上电上报仍继续）
    7、传感器处于无人低光照的状态上述已验证，再次测试传感器处于有人高光照状态，进行上电上报测试；
    8、设置传感器无效时间120s，定频上报均关闭，验证sid=320的情况下，测试网关正常上报的情况;
    9、设置传感器无效时间120s，照度定频上报和有无人定频均小于100，验证sid=320的情况下，测试网关正常上报的情况;
    10、设置传感器无效时间60s，照度定频上报和有无人定频均大于100，验证sid=320的情况下，测试网关正常上报的情况;
    11、设置传感器无效时间60s，照度定频上报大于100和有无人定频小于100，验证sid=320的情况下，测试网关正常上报的情况;
    12、设置传感器无效时间60s，定频上报均关闭，测试添加上报发生在上电上报之前；
    （添加上报正常，上电上报也按照以前机制进行上报，后期建议优化，添加上报成功后，中止上电上报）
    """
    engine.report_check_enable_all(True)  # 打开上报检测

    engine.add_doc_info("1、测试默认上报频率为0时，测试sid < 100的情况，sid = 8的情况下，测试网关正常上报的情况")
    engine.add_doc_info('本次测试等待时间T=A+sid%min(100，freq1，freq2)=60+8%100=68s')
    report_gateway_expect(wait_times=[15], ack=True, wait_enable=False)
    engine.wait(5, tips='保持5s的测试间隔')
    report_power_on_expect(wait_times=[68], ack=True)
    engine.add_doc_info("2、测试默认上报频率为0时，测试sid > 100的情况，sid = 320的情况下，测试网关正常上报的情况")
    engine.add_doc_info('本次测试等待时间T=A+sid%min(100，freq1，freq2)=60+320%100=80s')

    set_gw_info(panid=1100, sid=320)
    engine.wait(14, allowed_message=False)
    engine.expect_multi_dids("REPORT",
                             "读传感器数据B701", '09 00',
                             "读传感器数据B701", '0B ** **', ack=True)

    report_power_on_expect(wait_times=[80], ack=True)

    engine.add_doc_info("3、测试上报重发机制，收不到网关应答，进行10s、100s重试，重试结束则本次添加上报结束")
    engine.add_doc_info('本次测试等待时间T=A+sid%min(100，freq1，freq2)=60+320%100=80s')
    report_power_on_expect(wait_times=[80, 10, 100], ack=False)

    engine.add_doc_info("4、如果10s重试上报过程中，收到网关应答，不再进行100重试上报")
    engine.add_doc_info('本次测试等待时间T=A+sid%min(100，freq1，freq2)=60+320%100=80s')
    report_power_on_expect(wait_times=[80, 10], ack=True)

    engine.add_doc_info("5、测试上电上报前的过程中，是否可以正常被查询或设置参数（查询或设置参数正常，上电上报仍继续）")
    engine.add_doc_info('本次测试等待时间T=A+sid%min(100，freq1，freq2)=60+320%100=80s')
    # 前端工装断电重启，模拟上电上报
    passed_time01 = power_control()
    passed_time02 = read_write_test()
    engine.wait((80 - passed_time01 - passed_time02 - 1), allowed_message=False)
    engine.expect_multi_dids("REPORT",
                             "读传感器数据B701", '09 00',
                             "读传感器数据B701", '0B ** **', ack=True)
    engine.wait(125, allowed_message=False)

    engine.add_doc_info("6、测试上电上报重试的过程中，是否可以正常被查询或设置参数（查询或设置参数正常，上电上报仍继续）")
    engine.add_doc_info('本次测试等待时间T=A+sid%min(100，freq1，freq2)=60+320%100=80s')

    report_power_on_expect(wait_times=[80], ack=False, wait_enable=False)
    # 上电上报10s重试前可以被正常控制通断
    passed_time = read_write_test()
    engine.wait(10 - passed_time - 1, allowed_message=False)
    engine.expect_multi_dids("REPORT",
                             "读传感器数据B701", '09 00',
                             "读传感器数据B701", '0B ** **', ack=True)
    engine.wait(125, allowed_message=False)

    engine.add_doc_info("7、传感器处于无人低光照的状态上述已验证，再次测试传感器处于有人高光照状态，进行上电上报测试；")
    engine.add_doc_info('本次测试等待时间T=A+sid%min(100，freq1，freq2)=60+320%100=80s')

    engine.add_doc_info('因为人体红外感应器不支持SWB协议，所以无法设置传感器有无人参数和光照度参数。'
                        '目前该情况无法自动测试，需要人为补充测试。')
    # report_power_on_expect(expect_value='01', wait_times=[80], ack=True)

    engine.add_doc_info("8、设置传感器无效时间120s，定频上报均关闭，验证sid=320的情况下，测试网关正常上报的情况;")
    engine.send_did('WRITE', '传感器无效时间D702', 无效时间=120)
    engine.expect_did('WRITE', '传感器无效时间D702', 无效时间=120)
    for sensor_type in ['人体红外移动', '照度']:
        engine.send_did('WRITE', '上报频率D104', 传感器类型=sensor_type, 定频=0)
        engine.expect_did('WRITE', '上报频率D104', 传感器类型=sensor_type, 定频=0)
    engine.add_doc_info('本次测试等待时间T=A+sid%min(100，freq1，freq2)=120+320%100=140s')
    report_power_on_expect(wait_times=[140], ack=True, wait_enable=False)

    engine.add_doc_info("9、设置传感器无效时间120s，照度定频上报和有无人定频均小于100，验证sid=320的情况下，测试网关正常上报的情况;")
    engine.send_did('WRITE', '传感器无效时间D702', 无效时间=120)
    engine.expect_did('WRITE', '传感器无效时间D702', 无效时间=120)
    engine.send_did('WRITE', '上报频率D104', 传感器类型='人体红外移动', 定频=66)
    engine.expect_did('WRITE', '上报频率D104', 传感器类型='人体红外移动', 定频=66)
    engine.send_did('WRITE', '上报频率D104', 传感器类型='照度', 定频=77)
    engine.expect_did('WRITE', '上报频率D104', 传感器类型='照度', 定频=77)
    engine.add_doc_info('本次测试等待时间T=A+sid%min(100，freq1，freq2)=120+320%66=176s')
    report_power_on_expect(wait_times=[176], ack=True, wait_enable=False)

    engine.add_doc_info("10、设置传感器无效时间60s，照度定频上报和有无人定频均大于100，验证sid=320的情况下，测试网关正常上报的情况;")
    engine.send_did('WRITE', '传感器无效时间D702', 无效时间=60)
    engine.expect_did('WRITE', '传感器无效时间D702', 无效时间=60)
    engine.send_did('WRITE', '上报频率D104', 传感器类型='人体红外移动', 定频=166)
    engine.expect_did('WRITE', '上报频率D104', 传感器类型='人体红外移动', 定频=166)
    engine.send_did('WRITE', '上报频率D104', 传感器类型='照度', 定频=177)
    engine.expect_did('WRITE', '上报频率D104', 传感器类型='照度', 定频=177)
    engine.add_doc_info('本次测试等待时间T=A+sid%min(100，freq1，freq2)=60+320%100=80s')
    report_power_on_expect(wait_times=[80], ack=True, wait_enable=False)

    engine.add_doc_info("11、设置传感器无效时间60s，照度定频上报大于100和有无人定频小于100，验证sid=320的情况下，测试网关正常上报的情况;")
    engine.send_did('WRITE', '传感器无效时间D702', 无效时间=60)
    engine.expect_did('WRITE', '传感器无效时间D702', 无效时间=60)
    engine.send_did('WRITE', '上报频率D104', 传感器类型='人体红外移动', 定频=66)
    engine.expect_did('WRITE', '上报频率D104', 传感器类型='人体红外移动', 定频=66)
    engine.send_did('WRITE', '上报频率D104', 传感器类型='照度', 定频=177)
    engine.expect_did('WRITE', '上报频率D104', 传感器类型='照度', 定频=177)
    engine.add_doc_info('本次测试等待时间T=A+sid%min(100，freq1，freq2)=60+320%66=116s')
    report_power_on_expect(wait_times=[116], ack=True, wait_enable=False)

    engine.add_doc_info('12、设置传感器无效时间60s，定频上报均关闭，测试添加上报发生在上电上报之前；'
                        '（添加上报正常，上电上报也按照以前机制进行上报，后期建议优化，添加上报成功后，中止上电上报）')
    engine.send_did('WRITE', '传感器无效时间D702', 无效时间=60)
    engine.expect_did('WRITE', '传感器无效时间D702', 无效时间=60)
    engine.send_did('READ', '传感器无效时间D702', '')
    engine.expect_did('READ', '传感器无效时间D702', 无效时间=60)
    for sensor_type in ['人体红外移动', '照度']:
        engine.send_did('WRITE', '上报频率D104', 传感器类型=sensor_type, 定频=0)
        engine.expect_did('WRITE', '上报频率D104', 传感器类型=sensor_type, 定频=0)
        engine.send_did('READ', '上报频率D104', 传感器类型=sensor_type)
        engine.expect_did('READ', '上报频率D104', 传感器类型=sensor_type, 定频=0)

    engine.add_doc_info('测试完毕，将网关PANID设置回常用信息 panid=1000,sid=8,上次的上电上报时间为T=60+320%100=80s')
    engine.add_doc_info('（测试添加上报发生在上电上报之前,添加上报正常，上电上报仍按照以前机制进行上报，后期建议优化，添加上报成功后，中止上电上报）')
    passed_time1 = power_control()
    start_time = time.time()
    engine.wait(20, tips='上电上报前进行添加入网')
    report_gateway_expect(wait_times=[15], ack=True, wait_enable=False)
    passed_time2 = time.time() - start_time
    engine.wait(80 - passed_time1 - passed_time2 - 1, allowed_message=False)
    engine.expect_multi_dids("REPORT",
                             "读传感器数据B701", '09 00',
                             "读传感器数据B701", '0B ** **', ack=True)
    engine.wait(25, allowed_message=False)
    engine.add_doc_info('本次测试等待时间T=A+sid%min(100，freq1，freq2)=60+8%100=68s，再次上电上报，按照新机制运行')
    report_power_on_expect(wait_times=[68], ack=True)

    engine.report_check_enable_all(False)  # 关闭上报检测


def test_网关无应答时设备上报的重试机制():
    """
    03_网关无应答时设备上报的重试机制
    1、添加上报网关无应答重试机制，添加上报用例已测试，不再重复；
    2、上电上报网关无应答重试机制，上电上报用例已测试，不再重试；
    3、频率上报，频率小于110s，网关无应答重试机制，按照10s，100s重试上报；
    4、频率上报，频率小于110s，网关无应答重试机制，按照10s上报重试过程中，网关回复，不再进行100s重试上报；
    5、频率上报，频率大于110s，网关无应答重试机制，按照10s，100s重试上报；
    6、频率上报，频率大于110s，网关无应答重试机制，按照10s上报重试过程中，网关回复，不再进行100s重试上报；
    7、有无人步长上报，网关无应答重试机制，按照10s，100s重试上报；
    8、有无人步长上报，网关无应答重试机制，按照10s上报重试过程中，网关回复，不再进行100s重试上报；
    9、照度步长上报，网关无应答重试机制，按照10s，100s重试上报；
    10、照度步长上报，网关无应答重试机制，按照10s上报重试过程中，网关回复，不再进行100s重试上报；
    """
    engine.report_check_enable_all(True)  # 打开上报检测
    engine.add_doc_info("1、添加上报网关无应答重试机制，添加上报用例已测试，不再重复；")
    engine.add_doc_info("2、上电上报网关无应答重试机制，上电上报用例已测试，不再重试；")

    engine.add_doc_info("3、频率上报，频率小于110s，网关无应答重试机制，按照10s，100s重试上报；")
    engine.add_doc_info('频率上报，是以有无人传感器和照度传感器中频率最小的进行上报，设置有无人频率为60s，照度频率为70s，所以实际上报频率为60s')
    engine.send_did('WRITE', '上报频率D104', 传感器类型='人体红外移动', 定频=60)
    engine.expect_did('WRITE', '上报频率D104', 传感器类型='人体红外移动', 定频=60)
    engine.send_did('WRITE', '上报频率D104', 传感器类型='照度', 定频=70)
    engine.expect_did('WRITE', '上报频率D104', 传感器类型='照度', 定频=70)
    engine.add_doc_info('本次测试等待时间T=A+sid%min(100，freq1，freq2)=60+8%60=68s，再次上电上报，按照新机制运行')
    report_power_on_expect(wait_times=[68], ack=True, wait_enable=False)
    engine.add_doc_info('因为定频上报频率为60s，小于重试时间10+100=110s，所以会出现重试上报过程中，打断旧上报，开启新的上报的现象')
    for i in range(3):
        engine.add_doc_info('第{}轮重试上报测试'.format(i + 1))
        if i == 0:
            report_power_on_expect(wait_times=[60, 10], ack=False, wait_enable=False, power_on=False)
        else:
            report_power_on_expect(wait_times=[60 - 10, 10], ack=False, wait_enable=False, power_on=False)

    engine.add_doc_info("4、频率上报，频率小于110s，网关无应答重试机制，按照10s上报重试过程中，网关回复，不再进行100s重试上报；")
    report_power_on_expect(wait_times=[68], ack=True, wait_enable=False)
    for i in range(2):
        engine.add_doc_info('第{}轮重试上报测试'.format(i + 1))
        if i == 0:
            report_power_on_expect(wait_times=[60, 10], ack=True, wait_enable=False, power_on=False)
        else:
            report_power_on_expect(wait_times=[60 - 10, 10], ack=True, wait_enable=False, power_on=False)

    engine.add_doc_info("5、频率上报，频率大于110s，网关无应答重试机制，按照10s，100s重试上报；")
    engine.add_doc_info('频率上报，是以有无人传感器和照度传感器中频率最小的进行上报，设置有无人频率为150s，照度频率为130s，所以实际上报频率为130s')
    engine.send_did('WRITE', '上报频率D104', 传感器类型='人体红外移动', 定频=150)
    engine.expect_did('WRITE', '上报频率D104', 传感器类型='人体红外移动', 定频=150)
    engine.send_did('WRITE', '上报频率D104', 传感器类型='照度', 定频=130)
    engine.expect_did('WRITE', '上报频率D104', 传感器类型='照度', 定频=130)
    engine.add_doc_info('本次测试等待时间T=A+sid%min(100，freq1，freq2)=60+8%100=68s，再次上电上报，按照新机制运行')
    report_power_on_expect(wait_times=[68], ack=True, wait_enable=False)
    engine.add_doc_info('因为定频上报频率为130s，大于重试时间10+100=110s，所以测试过程中可以看到完整的上报重试过程')
    for i in range(3):
        engine.add_doc_info('第{}轮重试上报测试'.format(i + 1))
        if i == 0:
            report_power_on_expect(wait_times=[130, 10, 100], ack=False, wait_enable=False, power_on=False)
        else:
            report_power_on_expect(wait_times=[130 - 110, 10, 100], ack=False, wait_enable=False, power_on=False)

    engine.add_doc_info("6、频率上报，频率大于110s，网关无应答重试机制，按照10s上报重试过程中，网关回复，不再进行100s重试上报；")
    report_power_on_expect(wait_times=[68], ack=True, wait_enable=False)

    for i in range(3):
        engine.add_doc_info('第{}轮重试上报测试'.format(i + 1))
        if i == 0:
            report_power_on_expect(wait_times=[130, 10], ack=True, wait_enable=False, power_on=False)
        else:
            report_power_on_expect(wait_times=[130 - 10, 10], ack=True, wait_enable=False, power_on=False)

    engine.add_doc_info("7、有无人步长上报，网关无应答重试机制，按照10s，100s重试上报；")
    engine.add_doc_info("8、有无人步长上报，网关无应答重试机制，按照10s上报重试过程中，网关回复，不再进行100s重试上报；")
    engine.add_doc_info("9、照度步长上报，网关无应答重试机制，按照10s，100s重试上报；")
    engine.add_doc_info("10、照度步长上报，网关无应答重试机制，按照10s上报重试过程中，网关回复，不再进行100s重试上报；")

    engine.add_doc_info('测试步骤7至步骤10，因为人体红外感应器不支持SWB协议，所以无法设置传感器有无人参数和光照度参数。'
                        '目前该情况无法自动测试，需要人为补充测试。')

    engine.add_doc_info("测试完成后，将频率上报参数重置为默认参数；")
    for sensor_type in ['人体红外移动', '照度']:
        engine.send_did('WRITE', '上报频率D104', 传感器类型=sensor_type, 定频=0)
        engine.expect_did('WRITE', '上报频率D104', 传感器类型=sensor_type, 定频=0)
        engine.send_did('READ', '上报频率D104', 传感器类型=sensor_type)
        engine.expect_did('READ', '上报频率D104', 传感器类型=sensor_type, 定频=0)
    engine.report_check_enable_all(False)  # 关闭上报检测


def test_上报平台模式():
    """
    04_上报平台模式
    1、查询各项参数配置，确认正常；
    2、在默认配置下，测试有无人传感器从无人到有人、从有人到无人等2种情况，是否正常上报；
    3、在默认配置下，测试照度传感器光照变化值大于、等于、小于步长等多种情况，是否正常上报；
    4、修改默认配置，关闭步长上报，测试触发有无人上报和照度步长上报，是否不上报；
    5、修改默认配置，开启频率上报，分别测试人体红外移动传感器频率大于、等于、小于照度传感器等多种情况，是否按照频率最小值正常上报；
    6、修改默认配置，关闭频率上报，设置不同的滑差时间，测试从无人到有人、从有人到无人等多种情况，是否正常上报；
    7、修改默认配置，开启步长上报和频率上报，分别测试在滑差时间内，触发照度步长上报或者频率上报，是否正常上报；
    8、修改默认配置，开启步长上报和频率上报，测试频率上报过程中，发生步长上报干扰情况；
    9、将本轮测试修改的参数，恢复至默认参数；
    """

    engine.report_check_enable_all(True)  # 打开上报检测
    return_to_factory()
    engine.add_doc_info('1、查询各项参数配置，确认正常；')
    engine.send_did('READ', '主动上报使能标志D005', '')
    engine.expect_did('READ', '主动上报使能标志D005', '09 01')
    engine.send_did('READ', '上报间隔设置D004', '09')
    engine.expect_did('READ', '上报间隔设置D004', '09 05 00')
    engine.send_did('READ', '上报步长D103', '09')
    engine.expect_did('READ', '上报步长D103', '09 01')
    engine.send_did('READ', '上报步长D103', '0B')
    engine.expect_did('READ', '上报步长D103', '0B 20 00')
    engine.send_did('READ', '上报频率D104', '09')
    engine.expect_did('READ', '上报频率D104', '09 00 00')
    engine.send_did('READ', '上报频率D104', '0B')
    engine.expect_did('READ', '上报频率D104', '0B 00 00')

    engine.add_doc_info('2、在默认配置下，测试有无人传感器从无人到有人、从有人到无人等2种情况，是否正常上报；')
    engine.add_doc_info('3、在默认配置下，测试照度传感器光照变化值大于、等于、小于步长等多种情况，是否正常上报；')
    engine.add_doc_info('4、修改默认配置，关闭步长上报，测试触发有无人上报和照度步长上报，是否不上报；')

    engine.add_doc_info('测试步骤2至步骤4，因为人体红外感应器不支持SWB协议，所以无法设置传感器有无人参数和光照度参数。'
                        '目前该情况无法自动测试，需要人为补充测试。')

    engine.add_doc_info('5、修改默认配置，开启频率上报，分别测试人体红外移动传感器频率大于、等于、小于照度传感器等多种情况，是否按照频率最小值正常上报；')

    def report_expect_test(wait_time=60, num=3):
        for i in range(num):
            engine.add_doc_info('第{}轮上报测试'.format(i + 1))
            if i == 0:
                engine.expect_multi_dids("REPORT",
                                         "读传感器数据B701", '09 **',
                                         "读传感器数据B701", '0B ** **', ack=True, timeout=(wait_time + 1))
            else:
                engine.wait((wait_time - 1), allowed_message=False)
                engine.expect_multi_dids("REPORT",
                                         "读传感器数据B701", '09 **',
                                         "读传感器数据B701", '0B ** **', ack=True)

    engine.add_doc_info('（1）测试人体红外移动传感器频率大于照度传感器的情况，按照频率最小值60s进行上报')
    engine.send_did('WRITE', '上报频率D104', 传感器类型='人体红外移动', 定频=120)
    engine.expect_did('WRITE', '上报频率D104', 传感器类型='人体红外移动', 定频=120)
    engine.send_did('WRITE', '上报频率D104', 传感器类型='照度', 定频=60)
    engine.expect_did('WRITE', '上报频率D104', 传感器类型='照度', 定频=60)

    report_expect_test(wait_time=60, num=3)

    engine.add_doc_info('（2）测试人体红外移动传感器频率等于照度传感器的情况，按照频率最小值150s进行上报')
    engine.send_did('WRITE', '上报频率D104', 传感器类型='人体红外移动', 定频=150)
    engine.expect_did('WRITE', '上报频率D104', 传感器类型='人体红外移动', 定频=150)
    engine.send_did('WRITE', '上报频率D104', 传感器类型='照度', 定频=150)
    engine.expect_did('WRITE', '上报频率D104', 传感器类型='照度', 定频=150)
    report_expect_test(wait_time=150, num=3)

    engine.add_doc_info('（3）测试人体红外移动传感器频率小于照度传感器的情况，按照频率最小值300s进行上报')
    engine.send_did('WRITE', '上报频率D104', 传感器类型='人体红外移动', 定频=300)
    engine.expect_did('WRITE', '上报频率D104', 传感器类型='人体红外移动', 定频=300)
    engine.send_did('WRITE', '上报频率D104', 传感器类型='照度', 定频=360)
    engine.expect_did('WRITE', '上报频率D104', 传感器类型='照度', 定频=360)
    report_expect_test(wait_time=300, num=3)

    engine.add_doc_info('6、修改默认配置，关闭频率上报，设置不同的滑差时间，测试从无人到有人、从有人到无人等多种情况，是否正常上报；')
    engine.add_doc_info('7、修改默认配置，开启步长上报和频率上报，分别测试在滑差时间内，触发照度步长上报或者频率上报，是否正常上报；')
    engine.add_doc_info('8、修改默认配置，开启步长上报和频率上报，测试频率上报过程中，发生步长上报干扰情况；')
    engine.add_doc_info('测试步骤6至步骤8，因为人体红外感应器不支持SWB协议，所以无法设置传感器有无人参数和光照度参数。'
                        '目前该情况无法自动测试，需要人为补充测试。')
    engine.add_doc_info('9、将本轮测试修改的参数，恢复至默认参数；')
    engine.send_did('WRITE', '上报频率D104', 传感器类型='人体红外移动', 定频=0)
    engine.expect_did('WRITE', '上报频率D104', 传感器类型='人体红外移动', 定频=0)
    engine.send_did('WRITE', '上报频率D104', 传感器类型='照度', 定频=0)
    engine.expect_did('WRITE', '上报频率D104', 传感器类型='照度', 定频=0)

    engine.report_check_enable_all(False)  # 关闭上报检测


def test_设备联动模式():
    """
    05_设备联动模式
    1、模式切换测试，设置本地设备联动模式后，人体红外感应器的光照度上报频率、光照度上报步长被自动设置为0，并且平台端相关光照度配置按钮隐藏，不再支持配置。
    2、本地联动模式测试，将其配置为单设备单通道联动，并对联动重复机制进行验证；
    3、本地联动模式测试，将其配置为多设备多通道联动，并对联动重复机制进行验证；
    4、本地联动模式测试，将其配置为多设备多通道联动，多设备最长40个字节长度进行验证；
    5、本地联动模式测试，无人变有人情况下，联动逻辑测试；
    6、本地联动模式测试，维持一直有人情况下，联动逻辑测试；
    7、本地联动模式测试，有人变无人情况下，联动逻辑测试；
    8、修改默认配置，关闭有无人步长上报，测试触发有无人上报，是否不上报；
    9、修改默认配置，开启有无人频率上报，测试上报是否正常；
    10、修改默认配置，关闭频率上报，设置不同的滑差时间，测试从无人到有人、从有人到无人等多种情况，是否正常上报；
    11、修改默认配置，开启步长上报和频率上报，分别测试在滑差时间内，触发频率上报，是否正常上报；
    12、修改默认配置，开启步长上报和频率上报，测试频率上报过程中，发生步长上报干扰情况；
    13、将本轮测试修改的参数，恢复至默认参数；
    """
    engine.report_check_enable_all(True)  # 打开上报检测
    engine.add_doc_info('1、模式切换测试，设置本地设备联动模式后，人体红外感应器的光照度上报频率、光照度上报步长被自动设置为0，并且平台端相关光照度配置按钮隐藏，不再支持配置。')

    engine.add_doc_info('（1）模式切换前，重新设置参数与默认值不一致，并查询相关的参数')
    engine.send_did('WRITE', '主动上报使能标志D005', 传感器类型='人体红外移动', 上报命令='上报网关')
    engine.expect_did('WRITE', '主动上报使能标志D005', 传感器类型='人体红外移动', 上报命令='上报网关')
    engine.send_did('WRITE', '上报间隔设置D004', 传感器类型='人体红外移动', 滑差时间=1800)
    engine.expect_did('WRITE', '上报间隔设置D004', 传感器类型='人体红外移动', 滑差时间=1800)
    for sensor_type in ['人体红外移动', '照度']:
        engine.send_did('WRITE', '上报频率D104', 传感器类型=sensor_type, 定频=300)
        engine.expect_did('WRITE', '上报频率D104', 传感器类型=sensor_type, 定频=300)
    engine.send_did('WRITE', '上报步长D103', 传感器类型='人体红外移动', 步长='01')
    engine.expect_did('WRITE', '上报步长D103', 传感器类型='人体红外移动', 步长='01')
    engine.send_did('WRITE', '上报步长D103', '0B 50 00')
    engine.expect_did('WRITE', '上报步长D103', '0B 50 00')
    engine.send_did('WRITE', '传感器直接操作设备阀值D003', '0B 32 50')
    engine.expect_did('WRITE', '传感器直接操作设备阀值D003', '0B 32 50')

    engine.add_doc_info('（2）模式切换后，再次查询相关的参数，光照度上报频率、光照度上报步长被自动设置为0')
    engine.send_did('WRITE', '主动上报使能标志D005', '09 02')
    engine.expect_did('WRITE', '主动上报使能标志D005', '09 02')

    engine.send_did('READ', '主动上报使能标志D005', '')
    engine.expect_did('READ', '主动上报使能标志D005', '09 02')
    engine.send_did('READ', '上报间隔设置D004', 传感器类型='人体红外移动')
    engine.expect_did('READ', '上报间隔设置D004', 传感器类型='人体红外移动', 滑差时间=1800)
    engine.send_did('READ', '上报频率D104', 传感器类型='人体红外移动')
    engine.expect_did('READ', '上报频率D104', 传感器类型='人体红外移动', 定频=300)
    engine.send_did('READ', '上报频率D104', 传感器类型='照度')
    engine.expect_did('READ', '上报频率D104', 传感器类型='照度', 定频=0)
    engine.send_did('READ', '上报步长D103', '09')
    engine.expect_did('READ', '上报步长D103', '09 01')
    engine.send_did('READ', '上报步长D103', '0B')
    engine.expect_did('READ', '上报步长D103', '0B 00 00')
    engine.send_did('READ', '传感器直接操作设备阀值D003', '0B')
    engine.expect_did('READ', '传感器直接操作设备阀值D003', '0B 32 50')

    engine.add_doc_info('（3）平台端相关光照度步长、频率配置按钮隐藏，不再支持配置，通过抄控器仍可以进行设置，建议此处优化')
    for value in [300, 0]:
        engine.send_did('WRITE', '上报频率D104', 传感器类型='照度', 定频=value)
        engine.expect_did('WRITE', '上报频率D104', 传感器类型='照度', 定频=value)
        engine.send_did('READ', '上报频率D104', 传感器类型='照度')
        engine.expect_did('READ', '上报频率D104', 传感器类型='照度', 定频=value)
    for value in ['99 02', '00 00']:
        engine.send_did('WRITE', '上报步长D103', '0B ' + value)
        engine.expect_did('WRITE', '上报步长D103', '0B ' + value)
        engine.send_did('READ', '上报步长D103', '0B')
        engine.expect_did('READ', '上报步长D103', '0B ' + value)

    engine.add_doc_info('（4）将配置参数，配置为设备联动模式默认参数。'
                        '默认参数：滑差时间60s，开灯阈值40，关灯阈值60，被控设备为空，'
                        '有无人定频上报步长上报均关闭，光照度定频上报步长上报均关闭')
    engine.send_did('WRITE', '主动上报使能标志D005', '09 02')
    engine.expect_did('WRITE', '主动上报使能标志D005', '09 02')
    engine.send_did('WRITE', '上报间隔设置D004', 传感器类型='人体红外移动', 滑差时间=60)
    engine.expect_did('WRITE', '上报间隔设置D004', 传感器类型='人体红外移动', 滑差时间=60)
    engine.send_did('WRITE', '传感器直接操作设备阀值D003', '0B 28 3C')
    engine.expect_did('WRITE', '传感器直接操作设备阀值D003', '0B 28 3C')
    engine.send_did('WRITE', '控制目的设备地址D006', '00 01 FF FF FF FF 00')
    engine.expect_did('WRITE', '控制目的设备地址D006', '00 01 FF FF FF FF 00')
    for sensor_type in ['人体红外移动', '照度']:
        engine.send_did('WRITE', '上报频率D104', 传感器类型=sensor_type, 定频=0)
        engine.expect_did('WRITE', '上报频率D104', 传感器类型=sensor_type, 定频=0)
    engine.send_did('WRITE', '上报步长D103', 传感器类型='人体红外移动', 步长='00')
    engine.expect_did('WRITE', '上报步长D103', 传感器类型='人体红外移动', 步长='00')
    engine.send_did('WRITE', '上报步长D103', '0B 00 00')
    engine.expect_did('WRITE', '上报步长D103', '0B 00 00')

    engine.add_doc_info('2、本地联动模式测试，将其配置为单设备单通道联动，并对联动重复机制进行验证；')
    engine.add_doc_info('将其配置为单设备单通道联动，分别测试有人开灯、无人关灯的情况')
    engine.send_did('WRITE', '控制目的设备地址D006', '00 01 14 00 00 00 01')
    engine.expect_did('WRITE', '控制目的设备地址D006', '00 01 14 00 00 00 01')
    engine.wait(5)
    engine.send_did('READ', '控制目的设备地址D006', '')
    engine.expect_did('READ', '控制目的设备地址D006', '00 01 14 00 00 00 01')
    engine.add_doc_info('测试有人开灯的情况')

    engine.add_doc_info('测试无人关灯的情况')

    engine.add_doc_info('对联动重复机制进行验证'
                        '单设备控制时，传感器发送控制命令后，如果被控设备回复后，不在重发。如果设备在2s内没有回复则进行重发，重试2次，控制结束。')
    engine.add_doc_info('该部分测试，因为人体红外感应器不支持SWB协议，所以无法设置传感器有无人参数和光照度参数。'
                        '目前该情况无法自动测试，需要人为补充测试。')

    engine.add_doc_info('3、本地联动模式测试，将其配置为多设备多通道联动，并对联动重复机制进行验证；')
    engine.add_doc_info('将其配置为多设备多通道联动，分别测试有人开灯、无人关灯的情况')
    engine.send_did('WRITE', '控制目的设备地址D006', '01 01 01 42 17 01 01 02 42 17 01 01 04 42 17 01 01 08 42 17 01')
    engine.expect_did('WRITE', '控制目的设备地址D006', '01 01 01 42 17 01 01 02 42 17 01 01 04 42 17 01 01 08 42 17 01')
    engine.wait(5)
    engine.send_did('READ', '控制目的设备地址D006', '')
    engine.expect_did('READ', '控制目的设备地址D006', '01 01 01 42 17 01 01 02 42 17 01 01 04 42 17 01 01 08 42 17 01')
    engine.add_doc_info('测试有人开灯的情况')

    engine.add_doc_info('测试无人关灯的情况')

    engine.add_doc_info('对联动重复机制进行验证'
                        '多设备时，传感器间隔300ms发3次控制命令，不接收回复。')
    engine.add_doc_info('该部分测试，因为人体红外感应器不支持SWB协议，所以无法设置传感器有无人参数和光照度参数。'
                        '目前该情况无法自动测试，需要人为补充测试。')

    engine.add_doc_info('4、本地联动模式测试，将其配置为多设备多通道联动，多设备最长40个字节长度进行验证；')
    engine.add_doc_info('测试DID D006，数据域超长41个字节，无法设置成功，数据域保持之前的配置不变')
    engine.send_did('WRITE', '控制目的设备地址D006',
                    '01 01 01 08 01 04 C6 03 02 05 05 06 01 02 08 01 04 C4 03 02 05 05 06 01 04 06 01 00 C0 03 05 05 01 08 06 01 00 C0 03 05 05')
    engine.expect_did('WRITE', '控制目的设备地址D006', '03 00')
    engine.send_did('READ', '控制目的设备地址D006', '')
    engine.expect_did('READ', '控制目的设备地址D006', '01 01 01 42 17 01 01 02 42 17 01 01 04 42 17 01 01 08 42 17 01')

    engine.add_doc_info('测试DID D006，数据域40个字节，无法设置成功，数据域保持之前的配置不变')
    engine.send_did('WRITE', '控制目的设备地址D006',
                    '01 01 01 08 01 04 C6 03 02 05 05 06 01 02 07 01 04 C4 03 02 05 05 01 04 06 01 00 C0 03 05 05 01 08 06 01 00 C0 03 05 05')
    engine.expect_did('WRITE', '控制目的设备地址D006', '03 00')
    engine.send_did('READ', '控制目的设备地址D006', '')
    engine.expect_did('READ', '控制目的设备地址D006', '01 01 01 42 17 01 01 02 42 17 01 01 04 42 17 01 01 08 42 17 01')

    engine.add_doc_info('测试DID D006，数据域39个字节，可以设置成功')
    engine.send_did('WRITE', '控制目的设备地址D006',
                    '01 01 01 08 01 04 C6 03 02 05 05 06 01 02 06 01 04 C4 03 02 05 01 04 06 01 00 C0 03 05 05 01 08 06 01 00 C0 03 05 05')
    engine.expect_did('WRITE', '控制目的设备地址D006',
                      '01 01 01 08 01 04 C6 03 02 05 05 06 01 02 06 01 04 C4 03 02 05 01 04 06 01 00 C0 03 05 05 01 08 06 01 00 C0 03 05 05')
    engine.wait(5)
    engine.send_did('READ', '控制目的设备地址D006', '')
    engine.expect_did('READ', '控制目的设备地址D006',
                      '01 01 01 08 01 04 C6 03 02 05 05 06 01 02 06 01 04 C4 03 02 05 01 04 06 01 00 C0 03 05 05 01 08 06 01 00 C0 03 05 05')
    engine.add_doc_info('上述测试说明，DID D006，数据域最长支持39个字节，小于40个字节长度')

    engine.add_doc_info('5、本地联动模式测试，无人变有人情况下，联动逻辑测试；')
    engine.add_doc_info('（1）无人变有人&光照百分比大于关灯阈值60，连续监控2min，不触发设备联动')
    engine.add_doc_info('（2）无人变有人&光照百分比大于开灯阈值40小于关灯阈值60，连续监控2min，不触发设备联动')
    engine.add_doc_info('（3）无人变有人&光照百分比小于开灯阈值40，实时触发设备联动')
    engine.add_doc_info('结论：综上测试验证，有人且光照百分比低于开灯阈值的时候，才能正常联动开灯；')

    engine.add_doc_info('6、本地联动模式测试，维持一直有人情况下，联动逻辑测试；')
    engine.add_doc_info('（1）有人环境下&光照百分比由大于40变为小于40，满足开灯条件后，实时触发设备联动')
    engine.add_doc_info('（2）有人环境下&光照百分比由小于40变为大于40小于60,连续监控3min，维持设备联动开灯状态', )
    engine.add_doc_info('（3）有人环境下&光照百分比由小于40变为大于60，有人且高于关灯阈值的连续一段时间，会触发节能保护关灯，持续时间与滑差时间的低字节有关；')

    engine.add_doc_info('7、本地联动模式测试，有人变无人情况下，联动逻辑测试；')
    engine.add_doc_info('（1）有人变无人时&光照百分比小于开灯阈值40，联动设备是开启状态，设备感应无人后，马上进行关灯操作')
    engine.add_doc_info('（2）有人变无人时&光照百分比大于开灯阈值40小于关灯阈值60，联动设备是开启状态，设备感应无人后，马上进行关灯操作')

    engine.add_doc_info('8、修改默认配置，关闭有无人步长上报，测试触发有无人上报，是否不上报；')
    engine.add_doc_info('9、修改默认配置，开启有无人频率上报，测试上报是否正常；')
    engine.add_doc_info('10、修改默认配置，关闭频率上报，设置不同的滑差时间，测试从无人到有人、从有人到无人等多种情况，是否正常上报；')
    engine.add_doc_info('11、修改默认配置，开启步长上报和频率上报，分别测试在滑差时间内，触发频率上报，是否正常上报；')
    engine.add_doc_info('12、修改默认配置，开启步长上报和频率上报，测试频率上报过程中，发生步长上报干扰情况；')
    engine.add_doc_info('测试步骤5至步骤12，因为人体红外感应器不支持SWB协议，所以无法设置传感器有无人参数和光照度参数。'
                        '目前该情况无法自动测试，需要人为补充测试。')
    engine.add_doc_info('13、将本轮测试修改的参数，恢复至默认参数；')

    engine.report_check_enable_all(False)  # 关闭上报检测


def test_报警模式():
    """
    06_报警模式
    1、模式切换测试，设置为报警模式后，人体红外感应器的有无人上报步长、光照度上报频率、光照度上报步长被自动设置为0，并且平台端相关光照度配置按钮隐藏，不再支持配置。
    2、设置为报警模式后，默认配置，上报频率大于滑差时间，测试上报是否正常；
    3、修改默认配置，关闭频率上报，设置不同的滑差时间，测试从无人到有人、从有人到无人等多种情况，是否正常上报；
    4、修改默认配置，开启频率上报，，上报频率小于滑差时间，测试在滑差时间内，触发频率上报，是否正常上报；
    5、将本轮测试修改的参数，恢复至默认参数；
    """
    engine.report_check_enable_all(True)  # 打开上报检测
    engine.add_doc_info('1、模式切换测试，设置为报警模式后，人体红外感应器的有无人上报步长、光照度上报频率、光照度上报步长被自动设置为0，并且平台端相关光照度配置按钮隐藏，不再支持配置。')

    engine.add_doc_info('（1）模式切换前，重新设置参数与默认值不一致，并查询相关的参数')
    engine.send_did('WRITE', '主动上报使能标志D005', 传感器类型='人体红外移动', 上报命令='上报网关')
    engine.expect_did('WRITE', '主动上报使能标志D005', 传感器类型='人体红外移动', 上报命令='上报网关')
    engine.send_did('WRITE', '上报间隔设置D004', 传感器类型='人体红外移动', 滑差时间=1800)
    engine.expect_did('WRITE', '上报间隔设置D004', 传感器类型='人体红外移动', 滑差时间=1800)
    for sensor_type in ['人体红外移动', '照度']:
        engine.send_did('WRITE', '上报频率D104', 传感器类型=sensor_type, 定频=300)
        engine.expect_did('WRITE', '上报频率D104', 传感器类型=sensor_type, 定频=300)
    engine.send_did('WRITE', '上报步长D103', 传感器类型='人体红外移动', 步长='01')
    engine.expect_did('WRITE', '上报步长D103', 传感器类型='人体红外移动', 步长='01')
    engine.send_did('WRITE', '上报步长D103', '0B 50 00')
    engine.expect_did('WRITE', '上报步长D103', '0B 50 00')
    engine.send_did('WRITE', '传感器直接操作设备阀值D003', '0B 32 50')
    engine.expect_did('WRITE', '传感器直接操作设备阀值D003', '0B 32 50')

    engine.add_doc_info('（2）模式切换后，再次查询相关的参数，人体红外感应器的有无人上报步长、光照度上报频率、光照度上报步长被自动设置为0')
    engine.send_did('WRITE', '主动上报使能标志D005', '09 05')
    engine.expect_did('WRITE', '主动上报使能标志D005', '09 05')

    engine.send_did('READ', '主动上报使能标志D005', '')
    engine.expect_did('READ', '主动上报使能标志D005', '09 05')
    engine.send_did('READ', '上报间隔设置D004', 传感器类型='人体红外移动')
    engine.expect_did('READ', '上报间隔设置D004', 传感器类型='人体红外移动', 滑差时间=1800)
    engine.send_did('READ', '上报频率D104', 传感器类型='人体红外移动')
    engine.expect_did('READ', '上报频率D104', 传感器类型='人体红外移动', 定频=300)
    engine.send_did('READ', '上报频率D104', 传感器类型='照度')
    engine.expect_did('READ', '上报频率D104', 传感器类型='照度', 定频=0)
    engine.send_did('READ', '上报步长D103', '09')
    engine.expect_did('READ', '上报步长D103', '09 00')
    engine.send_did('READ', '上报步长D103', '0B')
    engine.expect_did('READ', '上报步长D103', '0B 00 00')
    engine.send_did('READ', '传感器直接操作设备阀值D003', '0B')
    engine.expect_did('READ', '传感器直接操作设备阀值D003', '0B 32 50')

    engine.add_doc_info('（3）平台端相关有无人&光照度步长、光照度频率配置按钮隐藏，不再支持配置，通过抄控器仍可以进行设置，建议此处优化')
    for value in [300, 0]:
        engine.send_did('WRITE', '上报频率D104', 传感器类型='照度', 定频=value)
        engine.expect_did('WRITE', '上报频率D104', 传感器类型='照度', 定频=value)
        engine.send_did('READ', '上报频率D104', 传感器类型='照度')
        engine.expect_did('READ', '上报频率D104', 传感器类型='照度', 定频=value)
    for value in ['01', '00']:
        engine.send_did('WRITE', '上报步长D103', 传感器类型='人体红外移动', 步长=value)
        engine.expect_did('WRITE', '上报步长D103', 传感器类型='人体红外移动', 步长=value)
        engine.send_did('READ', '上报步长D103', 传感器类型='人体红外移动')
        engine.expect_did('READ', '上报步长D103', 传感器类型='人体红外移动', 步长=value)
    for value in ['99 02', '00 00']:
        engine.send_did('WRITE', '上报步长D103', '0B ' + value)
        engine.expect_did('WRITE', '上报步长D103', '0B ' + value)
        engine.send_did('READ', '上报步长D103', '0B')
        engine.expect_did('READ', '上报步长D103', '0B ' + value)

    engine.add_doc_info('（4）将配置参数，配置为设备联动模式默认参数。'
                        '默认参数：滑差时间5s，有无人定频上报10s，'
                        '有无人步长上报关闭，光照度定频上报步长上报均关闭')
    engine.send_did('WRITE', '主动上报使能标志D005', '09 05')
    engine.expect_did('WRITE', '主动上报使能标志D005', '09 05')
    engine.send_did('WRITE', '上报间隔设置D004', 传感器类型='人体红外移动', 滑差时间=5)
    engine.expect_did('WRITE', '上报间隔设置D004', 传感器类型='人体红外移动', 滑差时间=5)
    engine.send_did('WRITE', '传感器直接操作设备阀值D003', '0B 28 3C')
    engine.expect_did('WRITE', '传感器直接操作设备阀值D003', '0B 28 3C')
    engine.send_did('WRITE', '控制目的设备地址D006', '00 01 FF FF FF FF 00')
    engine.expect_did('WRITE', '控制目的设备地址D006', '00 01 FF FF FF FF 00')
    engine.send_did('WRITE', '上报频率D104', 传感器类型='人体红外移动', 定频=10)
    engine.expect_did('WRITE', '上报频率D104', 传感器类型='人体红外移动', 定频=10)
    engine.send_did('WRITE', '上报频率D104', 传感器类型='照度', 定频=0)
    engine.expect_did('WRITE', '上报频率D104', 传感器类型='照度', 定频=0)
    engine.send_did('WRITE', '上报步长D103', 传感器类型='人体红外移动', 步长='00')
    engine.expect_did('WRITE', '上报步长D103', 传感器类型='人体红外移动', 步长='00')
    engine.send_did('WRITE', '上报步长D103', '0B 00 00')
    engine.expect_did('WRITE', '上报步长D103', '0B 00 00')
    engine.add_doc_info('2、设置为报警模式后，默认配置，上报频率大于滑差时间，测试上报是否正常；')
    engine.add_doc_info('测试无人变有人后，触发报警上报；有人变无人后，不触发上报')

    engine.add_doc_info('测试传感器维持一直有人的情况下，是否按照设定的频率进行上报')

    engine.add_doc_info('3、修改默认配置，关闭频率上报，设置不同的滑差时间，测试从无人到有人、从有人到无人等多种情况，是否正常上报；')
    engine.add_doc_info('4、修改默认配置，开启频率上报，上报频率小于滑差时间，测试在滑差时间内，触发频率上报，是否正常上报；')

    engine.add_doc_info('测试步骤2至步骤4，因为人体红外感应器不支持SWB协议，所以无法设置传感器有无人参数和光照度参数。'
                        '目前该情况无法自动测试，需要人为补充测试。')
    engine.add_doc_info('5、将本轮测试修改的参数，恢复至默认参数；')
    return_to_factory()

    engine.report_check_enable_all(False)  # 关闭上报检测
