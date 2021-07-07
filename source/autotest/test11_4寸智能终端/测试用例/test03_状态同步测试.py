# encoding:utf-8
# 导入测试引擎
import engine
from autotest.oip.测试用例.常用测试模块 import report_gateway_expect, set_subscriber, report_boardcast_expect

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
    1、设备收到网关发送的注册帧后等15s（允许1s误差）以后开始上报
    2、设备添加上报后，收不到网关应答，进行10s、100s重试，重试结束则本次添加上报结束；
    """
    engine.report_check_enable_all(True)  # 打开上报检测
    engine.add_doc_info("1、设备收到网关发送的注册帧后等15s（允许1s误差）以后开始上报")
    report_gateway_expect(wait_times=[15], ack=True, quit_net=True)

    engine.add_doc_info("2、设备添加上报后，收不到网关应答，进行10s、100s重试，重试结束则本次添加上报结束")
    report_gateway_expect(wait_times=[15, 10, 100], ack=False)

    engine.report_check_enable_all(False)  # 关闭上报检测


def set_gw_info(panid, sid):
    pass


def test_广播报文控制测试():
    """
    02_广播报文控制测试
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
    engine.add_doc_info("测试前准备工作，配置3个订阅者")
    # 配置订阅者3个
    panel01 = set_subscriber("订阅者1", 21)
    panel02 = set_subscriber("订阅者2", 22)
    panel03 = set_subscriber("订阅者3", 23)

    engine.add_doc_info("1、组地址按位组合")
    # 情景模式控制后，第一次上报时间为1.3+0.5*2=2.3s，允许1s误差存在
    report_boardcast_expect([panel01, panel02, panel03], write_value="81", expect_value="01",
                            first_timeout=3.3, scene_type="组地址按位组合")
    report_boardcast_expect([panel01, panel02, panel03], write_value="01", expect_value="00",
                            first_timeout=3.3, scene_type="组地址按位组合")

    engine.add_doc_info("2、组地址按单字节组合")
    # 情景模式控制后，第一次上报时间为1.3+0.5*2=2.3s，允许1s误差存在
    report_boardcast_expect([panel01, panel02, panel03], write_value="81", expect_value="01",
                            first_timeout=3.3, scene_type="组地址按单字节组合")
    report_boardcast_expect([panel01, panel02, panel03], write_value="01", expect_value="00",
                            first_timeout=3.3, scene_type="组地址按单字节组合")

    engine.add_doc_info("3、组地址按双字节组合")
    # 情景模式控制后，第一次上报时间为1.3+0.5*2=2.3s，允许1s误差存在
    report_boardcast_expect([panel01, panel02, panel03], write_value="81", expect_value="01",
                            first_timeout=3.3, scene_type="组地址按双字节组合")
    report_boardcast_expect([panel01, panel02, panel03], write_value="01", expect_value="00",
                            first_timeout=3.3, scene_type="组地址按双字节组合")

    engine.add_doc_info("4、存在多个组地址的情况，组地址在前")
    # 情景模式控制后，第一次上报时间为1.3+0.5*2=2.3s，允许1s误差存在
    report_boardcast_expect([panel01, panel02, panel03], write_value="81", expect_value="01",
                            first_timeout=3.3, scene_type="存在多个组地址的情况，组地址在前")
    report_boardcast_expect([panel01, panel02, panel03], write_value="01", expect_value="00",
                            first_timeout=3.3, scene_type="存在多个组地址的情况，组地址在前")

    engine.add_doc_info("5、存在多个组地址的情况，组地址在后")
    # 情景模式控制后，第一次上报时间为1.3+0.5*12=7.3s，允许1s误差存在
    report_boardcast_expect([panel01, panel02, panel03], write_value="81", expect_value="01",
                            first_timeout=8.3, scene_type="存在多个组地址的情况，组地址在后")
    report_boardcast_expect([panel01, panel02, panel03], write_value="01", expect_value="00",
                            first_timeout=8.3, scene_type="存在多个组地址的情况，组地址在后")

    engine.add_doc_info("6、不同组地址混合 按单字节+按双字节+按位组合")
    # 情景模式控制后，第一次上报时间为1.3+0.5*2=2.3s，允许1s误差存在
    report_boardcast_expect([panel01, panel02, panel03], write_value="81", expect_value="01",
                            first_timeout=3.3, scene_type="不同组地址混合 按单字节+按双字节+按位组合")
    report_boardcast_expect([panel01, panel02, panel03], write_value="01", expect_value="00",
                            first_timeout=3.3, scene_type="不同组地址混合 按单字节+按双字节+按位组合")

    engine.add_doc_info("7、模拟220字节超长情景模式报文测试")
    # 网关发送情景模式报文，最长为220个字节，使报文长度接近220个字节，下列为219个字节
    # 情景模式控制后，第一次上报时间为1.3+0.5*76=49.3s，允许1s误差存在
    report_boardcast_expect([panel01, panel02, panel03], write_value="81", expect_value="01",
                            first_timeout=50.3, scene_type="模拟220字节超长情景模式报文测试")
    report_boardcast_expect([panel01, panel02, panel03], write_value="01", expect_value="00",
                            first_timeout=50.3, scene_type="模拟220字节超长情景模式报文测试")

    engine.add_doc_info("8、验证sid大于255的情况，sid=280情况下，按位、按双字节情景模式模式控制")
    engine.add_doc_info('sid大于255时，超出单字节范围，单字节无法表示，所以不需要验证按单字节情景模式控制')

    set_gw_info(panid=1100, sid=280)
    engine.wait(14, allowed_message=False)
    engine.expect_multi_dids("REPORT",
                             "通断操作C012", '00',
                             "导致状态改变的控制设备AIDC01A", config["测试设备地址"], ack=True)
    engine.add_doc_info('重新入网后，订阅者信息被清除，需要重新控制，添加3个订阅者')
    # 配置订阅者3个
    panel01 = set_subscriber("订阅者1", 21)
    panel02 = set_subscriber("订阅者2", 22)
    panel03 = set_subscriber("订阅者3", 23)

    # 情景模式控制后，第一次上报时间为1.3+0.5*4=3.3s，允许1s误差存在
    report_boardcast_expect([panel01, panel02, panel03], write_value="81", expect_value="01",
                            first_timeout=4.3, scene_type="sid大于255，组地址按位组合")
    report_boardcast_expect([panel01, panel02, panel03], write_value="01", expect_value="00",
                            first_timeout=4.3, scene_type="sid大于255，组地址按位组合")

    report_boardcast_expect([panel01, panel02, panel03], write_value="81", expect_value="01",
                            first_timeout=4.3, scene_type="sid大于255，组地址按双字节组合")
    report_boardcast_expect([panel01, panel02, panel03], write_value="01", expect_value="00",
                            first_timeout=4.3, scene_type="sid大于255，组地址按双字节组合")

    engine.add_doc_info('9、设置回常用的网关信息和PANID')
    report_gateway_expect(wait_times=[15], ack=True)

    engine.report_check_enable_all(False)  # 关闭上报检测