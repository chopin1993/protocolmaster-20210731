# encoding:utf-8
# 导入测试引擎
from .常用测试模块 import *
#engine.wait("室外机工作状态E060",allowed_message=False)
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
    01 _添加上报测试
    1、设备收到网关发送的注册帧后等15s（允许1s误差）以后开始上报
    2、设备添加上报后，收不到网关应答，进行10s、100s重试，重试结束则本次添加上报结束
    3、如果10s重试上报过程中，收到网关应答，不再进行100重试上报
    4、测试添加网关后，添加上报前，是否可以正常被控制通断（控制正常，被控制通断后，新的上报取代添加上报，添加上报中止）
    5、测试添加上报重试的过程中，是否可以正常被控制通断（控制正常，被控制通断后，新的上报取代添加上报，添加上报中止）
    6、继电器处于断开的状态上述已验证，再次测试继电器处于闭合的状态，进行添加上报测试；
    """

    engine.report_check_enable_all(True)  # 打开上报检测
    engine.send_did("WRITE", "室外机工作状态E060",
                    "4E 9F 06 00 13 E0 01 01 12 E0 01 00 00 E0 02 00 12 00 E0 02 01 45 01 B7 03 03 23 00 01 B7 03 04 37 00 01 B7 03 05 10 01 01 B7 03 06 10 01 01 B7 03 0F 34 02 5C E0 03 01 02 03 51 E0 01 01 09 D1 02 01 00 0A D1 02 01 00 05 D1 02 06 00 05 D1 02 07 00 05 D1 02 08 00 05 D1 02 09 00 05 E0 04 07 35 20 60")
    engine.expect_did("WRITE", "室外机工作状态E060",
                      "4E 9F 06 00 13 E0 01 01 12 E0 01 00 00 E0 02 00 12 00 E0 02 01 45 01 B7 03 03 23 00 01 B7 03 04 37 00 01 B7 03 05 10 01 01 B7 03 06 10 01 01 B7 03 0F 34 02 5C E0 03 01 02 03 51 E0 01 01 09 D1 02 01 00 0A D1 02 01 00 05 D1 02 06 00 05 D1 02 07 00 05 D1 02 08 00 05 D1 02 09 00 05 E0 04 07 35 20 60")

    engine.send_did("WRITE", "开关机E013", "01")
    engine.expect_did("WRITE", "开关机E013", "01")
    engine.add_doc_info("1、设备收到网关发送的注册帧后等15s（允许1s误差）以后开始上报")
    report_gateway_expect(wait_times=[15], ack=True, quit_net=True)

    engine.add_doc_info("2、设备添加上报后，收不到网关应答，进行10s、100s重试，重试结束则本次添加上报结束")
    report_gateway_expect(wait_times=[15, 10, 100], ack=False, quit_net=True)

    engine.send_did("WRITE", "开关机E013", "01")
    engine.expect_did("WRITE", "开关机E013", "01")
    engine.add_doc_info("3、如果10s重试上报过程中，收到网关应答，不再进行100s")
    report_gateway_expect(wait_times=[15, 10], ack=True, quit_net=True)

    
    engine.add_doc_info("4、测试添加网关后，添加上报前，是否可以正常被控制开关机"
                        "（控制正常，被控制开关机后，新的上报不会取代添加上报，添加上报继续）")

    set_gw_info()  # 设置网关PANID信息，模拟设备入网
    # 在入网15s内进行通断控制，均可以正常工作，被控制开关机后，新的上报取代添加上报，添加上报继续
    read_write_test()


    engine.wait(125, allowed_message=True)
    engine.send_did("WRITE", "退网通知060B", 退网设备=config["测试设备地址"])

    #engine.add_doc_info("5、测试添加上报重试的过程中，是否可以正常被控制读取")


    # 被控制通断后，新的上报不会取代添加上报，添加上报继续
    # report_gateway_expect(wait_times=[15, 10], ack=False, quit_net=False,wait_enable=False)
    # read_write_test()
    # engine.wait(100-read_write_test()+1,allowed_message=True)
    # engine.expect_multi_dids("REPORT",
    #                          "读传感器数据B701", "03 ** **",
    #                          "读传感器数据B701", "04 ** **",
    #                          "读传感器数据B701", "0F ** **",
    #                          "上报告警信息D105", "00 **",
    #                          "上报告警信息D105", "02 **",
    #                          "阀门开关地暖阀或风机阀E051", "**",
    #                          "开关机E013", "**",
    #                          "运行模式E012", "**",
    #                          "风机控制E011", "**",
    #                          "按键解锁/锁定E01E", "** ** **",
    #                          "设置温度1E002", "**",
    #                          "导致状态改变的控制设备AIDC01A", config["测试设备地址"], ack=True, timeout=2)
    #
    # engine.send_did("WRITE", "退网通知060B", 退网设备=config["测试设备地址"])





    #将设备通断状态设置回默认状态
    engine.report_check_enable_all(False)  # 关闭上报检测




def test_定频上报():

    """
    02_温湿度定频上报测试
    1、温度定频上报：上报频率D104 03,
    2、湿度定频上报：上报频率D104 04；
    """

    engine.add_doc_info('上电上报')
    report_power_on_expect(expect_value="00", wait_times=[125], ack=True, wait_enable=True)
    engine.add_doc_info('开机')
    engine.send_did("WRITE", "开关机E013", "01")
    engine.expect_did("WRITE", "开关机E013", "01")
    timeout=2
    engine.send_multi_dids("WRITE", "室外机工作状态E060",
                           "4E 9F 06 00 13 E0 01 01 12 E0 01 00 00 E0 02 00 12 00 E0 02 01 45 01 B7 03 03 23 00 01 B7 03 04 37 00 01 B7 03 05 10 01 01 B7 03 06 10 01 01 B7 03 0F 34 02 5C E0 03 01 02 03 51 E0 01 01 09 D1 02 01 00 0A D1 02 01 00 05 D1 02 06 00 05 D1 02 07 00 05 D1 02 08 00 05 D1 02 09 00 05 E0 04 07 35 20 60")
    engine.expect_multi_dids("WRITE", "室外机工作状态E060",
                             "4E 9F 06 00 13 E0 01 01 12 E0 01 00 00 E0 02 00 12 00 E0 02 01 45 01 B7 03 03 23 00 01 B7 03 04 37 00 01 B7 03 05 10 01 01 B7 03 06 10 01 01 B7 03 0F 34 02 5C E0 03 01 02 03 51 E0 01 01 09 D1 02 01 00 0A D1 02 01 00 05 D1 02 06 00 05 D1 02 07 00 05 D1 02 08 00 05 D1 02 09 00 05 E0 04 07 35 20 60")

    # engine.expect_multi_dids("READ", "室外机工作状态E060",
    #                          "4E 9F 06 00 13 E0 01 01 12 E0 01 00 00 E0 02 00 12 00 E0 02 01 45 01 B7 03 03 23 00 01 B7 03 04 37 00 01 B7 03 05 10 01 01 B7 03 06 10 01 01 B7 03 0F 34 02 5C E0 03 01 02 03 51 E0 01 01 09 D1 02 01 00 0A D1 02 01 00 05 D1 02 06 00 05 D1 02 07 00 05 D1 02 08 00 05 D1 02 09 00 05 E0 04 07 35 20 60",
    #                          timeout=10, ack=True)


    engine.add_doc_info('温度定频上报')
    engine.report_check_enable_all(True)  # 打开上报检测
    engine.expect_multi_dids("READ", "室外机工作状态E060",
                             "4E 9F 06 00 13 E0 01 01 12 E0 01 00 00 E0 02 00 12 00 E0 02 01 45 01 B7 03 03 23 00 01 B7 03 04 37 00 01 B7 03 05 10 01 01 B7 03 06 10 01 01 B7 03 0F 34 02 5C E0 03 01 02 03 51 E0 01 01 09 D1 02 01 00 0A D1 02 01 00 05 D1 02 06 00 05 D1 02 07 00 05 D1 02 08 00 05 D1 02 09 00 05 E0 04 07 35 20 60",
                             timeout=11, ack=True)

    # 温度定频上报
    # 查询温度定频
    engine.send_did("READ", "上报频率D104", "03")
    engine.expect_did("READ", "上报频率D104", "03 00 00")
    # 设定温度定频为10s
    engine.add_doc_info('温度定频上报10s')
    engine.send_did("WRITE", "上报频率D104", "03 0A 00")
    engine.expect_did("WRITE", "上报频率D104", "03 0A 00")

    # 查询温度定频
    engine.send_did("READ", "上报频率D104", "03")
    engine.expect_did("READ", "上报频率D104", "03 0A 00")

    # 等待10s，让其上报
    wait_time = 10
    #range(i)，i就是循环几次
    for i in range(3):
        engine.add_doc_info("第{}轮上报测试".format(i + 1))
        # engine.expect_did("READ", "室外机工作状态E060", "04 FF FF FF FF")
        engine.expect_multi_dids("READ", "室外机工作状态E060",
                                 "4E 9F 06 00 13 E0 01 01 12 E0 01 00 00 E0 02 00 12 00 E0 02 01 45 01 B7 03 03 23 00 01 B7 03 04 37 00 01 B7 03 05 10 01 01 B7 03 06 10 01 01 B7 03 0F 34 02 5C E0 03 01 02 03 51 E0 01 01 09 D1 02 01 00 0A D1 02 01 00 05 D1 02 06 00 05 D1 02 07 00 05 D1 02 08 00 05 D1 02 09 00 05 E0 04 07 35 20 60",
                                 timeout=11, ack=True)

        if i == 0:
            engine.expect_multi_dids("REPORT",
                                     "读传感器数据B701", "03 ** **",
                                     "读传感器数据B701", "04 ** **",
                                     "读传感器数据B701", "0F ** **",
                                     ack=True, timeout=(wait_time + 1)
                                     )
        else:
            engine.wait((wait_time - 1), allowed_message=False)
            engine.expect_multi_dids("REPORT",
                                     "读传感器数据B701", "03 ** **",
                                     "读传感器数据B701", "04 ** **",
                                     "读传感器数据B701", "0F ** **", ack=True)

    #关闭温度定频上报
    engine.send_did("WRITE", "上报频率D104", "03 00 00")
    engine.expect_did("WRITE", "上报频率D104", "03 00 00")

    #
    # 设定温度定频为15s
    engine.send_did("WRITE", "上报频率D104", "03 0F 00")
    engine.expect_did("WRITE", "上报频率D104", "03 0F 00")

    # 查询温度定频
    engine.send_did("READ", "上报频率D104", "03")
    engine.expect_did("READ", "上报频率D104", "03 0F 00")

    wait_time = 15
    for i in range(3):
        engine.add_doc_info("第{}轮上报测试".format(i + 1))
        engine.expect_multi_dids("READ", "室外机工作状态E060",
                                 "4E 9F 06 00 13 E0 01 01 12 E0 01 00 00 E0 02 00 12 00 E0 02 01 45 01 B7 03 03 23 00 01 B7 03 04 37 00 01 B7 03 05 10 01 01 B7 03 06 10 01 01 B7 03 0F 34 02 5C E0 03 01 02 03 51 E0 01 01 09 D1 02 01 00 0A D1 02 01 00 05 D1 02 06 00 05 D1 02 07 00 05 D1 02 08 00 05 D1 02 09 00 05 E0 04 07 35 20 60",
                                 timeout=11, ack=True)

        if i == 0:
          engine.expect_multi_dids("REPORT",
                                         "读传感器数据B701", "03 ** **",
                                         "读传感器数据B701", "04 ** **",
                                         "读传感器数据B701", "0F ** **",
                                         ack=True, timeout=(wait_time + 1)
                                         )
        else:
          engine.wait((wait_time - 1), allowed_message=False)
          engine.expect_multi_dids("REPORT",
                                         "读传感器数据B701", "03 ** **",
                                         "读传感器数据B701", "04 ** **",
                                         "读传感器数据B701", "0F ** **", ack=True)

    #关闭温度定频上报
    engine.send_did("WRITE", "上报频率D104", "03 00 00")
    engine.expect_did("WRITE", "上报频率D104", "03 00 00")


    # 查询温度定频
    engine.send_did("READ", "上报频率D104", "03")
    engine.expect_did("READ", "上报频率D104", "03 00 00")


    # 湿度定频上报
    # 查询湿度定频
    engine.add_doc_info('湿度定频上报10s')
    engine.send_did("READ", "上报频率D104", "04")
    engine.expect_did("READ", "上报频率D104", "04 ** **")
    # 设定湿度定频为10s
    engine.send_did("WRITE", "上报频率D104", "04 0A 00")
    engine.expect_did("WRITE", "上报频率D104", "04 0A 00")

    # 查询湿度定频
    engine.send_did("READ", "上报频率D104", "04")
    engine.expect_did("READ", "上报频率D104", "04 0A 00")
    # 上报
    # engine.expect_did("REPORT", "上报频率D104", "04 ** **", )
    wait_time = 10
    # range(i)，i就是循环几次
    for i in range(3):
        engine.add_doc_info("第{}轮上报测试".format(i + 1))
        engine.expect_multi_dids("READ", "室外机工作状态E060",
                                 "4E 9F 06 00 13 E0 01 01 12 E0 01 00 00 E0 02 00 12 00 E0 02 01 45 01 B7 03 03 23 00 01 B7 03 04 37 00 01 B7 03 05 10 01 01 B7 03 06 10 01 01 B7 03 0F 34 02 5C E0 03 01 02 03 51 E0 01 01 09 D1 02 01 00 0A D1 02 01 00 05 D1 02 06 00 05 D1 02 07 00 05 D1 02 08 00 05 D1 02 09 00 05 E0 04 07 35 20 60",
                                 timeout=11, ack=True)

        if i == 0:
            engine.expect_multi_dids("REPORT",
                                     "读传感器数据B701", "03 ** **",
                                     "读传感器数据B701", "04 ** **",
                                     "读传感器数据B701", "0F ** **",
                                     ack=True, timeout=(wait_time + 1)
                                     )
        else:
            engine.wait((wait_time - 1), allowed_message=False)
            engine.expect_multi_dids("REPORT",
                                     "读传感器数据B701", "03 ** **",
                                     "读传感器数据B701", "04 ** **",
                                     "读传感器数据B701", "0F ** **", ack=True)

    engine.add_doc_info('关闭湿度定频上报')
    engine.send_did("WRITE", "上报频率D104", "04 00 00")
    engine.expect_did("WRITE", "上报频率D104", "04 00 00")

    #上报

    #engine.expect_did("REPORT","上报频率D104", "04 0A 00")

    # 设定湿度定频为15s
    engine.add_doc_info('湿度定频上报15s')
    engine.send_did("WRITE", "上报频率D104", "04 0F 00")
    engine.expect_did("WRITE", "上报频率D104", "04 0F 00")

    # 查询湿度定频
    engine.send_did("READ", "上报频率D104", "04")
    engine.expect_did("READ", "上报频率D104", "04 0F 00")
    # 上报
    # engine.expect_did("REPORT", "上报频率D104", "04 ** **", )
    wait_time = 16
    for i in range(3):
        engine.add_doc_info("第{}轮上报测试".format(i + 1))
        engine.expect_multi_dids("READ", "室外机工作状态E060",
                                 "4E 9F 06 00 13 E0 01 01 12 E0 01 00 00 E0 02 00 12 00 E0 02 01 45 01 B7 03 03 23 00 01 B7 03 04 37 00 01 B7 03 05 10 01 01 B7 03 06 10 01 01 B7 03 0F 34 02 5C E0 03 01 02 03 51 E0 01 01 09 D1 02 01 00 0A D1 02 01 00 05 D1 02 06 00 05 D1 02 07 00 05 D1 02 08 00 05 D1 02 09 00 05 E0 04 07 35 20 60",
                                 timeout=11, ack=True)

        if i == 0:
            engine.expect_multi_dids("REPORT",
                                     "读传感器数据B701", "03 ** **",
                                     "读传感器数据B701", "04 ** **",
                                     "读传感器数据B701", "0F ** **",
                                     ack=True, timeout=(wait_time + 1)
                                     )
        else:
            engine.wait((wait_time - 1), allowed_message=False)
            engine.expect_multi_dids("REPORT",
                                     "读传感器数据B701", "03 ** **",
                                     "读传感器数据B701", "04 ** **",
                                     "读传感器数据B701", "0F ** **", ack=True)
    # 关闭湿度定频上报
    engine.send_did("WRITE", "上报频率D104", "04 00 00")
    engine.expect_did("WRITE", "上报频率D104", "04 00 00")

    # 查询湿度定频
    engine.send_did("READ", "上报频率D104", "04")
    engine.expect_did("READ", "上报频率D104", "04 00 00")



    # 温湿度定频上报
    # 设定温度定频为20s，湿度定频为30s
    engine.add_doc_info('温度定频为20s，湿度定频为30s')
    engine.send_did("WRITE", "上报频率D104", "03 14 00")
    engine.expect_did("WRITE", "上报频率D104", "03 14 00")
    engine.send_did("WRITE", "上报频率D104", "04 1E 00")
    engine.expect_did("WRITE", "上报频率D104", "04 1E 00")

    # 查询温湿度定频
    engine.send_did("READ", "上报频率D104", "03")
    engine.expect_did("READ", "上报频率D104", "03 14 00")
    engine.send_did("READ", "上报频率D104", "04")
    engine.expect_did("READ", "上报频率D104", "04 1E 00")

    wait_time = 31
    for i in range(3):
        engine.add_doc_info("第{}轮上报测试".format(i + 1))
        engine.expect_multi_dids("READ", "室外机工作状态E060",
                                 "4E 9F 06 00 13 E0 01 01 12 E0 01 00 00 E0 02 00 12 00 E0 02 01 45 01 B7 03 03 23 00 01 B7 03 04 37 00 01 B7 03 05 10 01 01 B7 03 06 10 01 01 B7 03 0F 34 02 5C E0 03 01 02 03 51 E0 01 01 09 D1 02 01 00 0A D1 02 01 00 05 D1 02 06 00 05 D1 02 07 00 05 D1 02 08 00 05 D1 02 09 00 05 E0 04 07 35 20 60",
                                 timeout=11, ack=True)

        if i == 0:
            engine.expect_multi_dids("REPORT",
                                     "读传感器数据B701", "03 ** **",
                                     "读传感器数据B701", "04 ** **",
                                     "读传感器数据B701", "0F ** **",
                                     ack=True, timeout=(wait_time + 1)
                                     )
        else:
            engine.wait((wait_time - 1), allowed_message=False)
            engine.expect_multi_dids("REPORT",
                                     "读传感器数据B701", "03 ** **",
                                     "读传感器数据B701", "04 ** **",
                                     "读传感器数据B701", "0F ** **", ack=True)


    # 关闭温度步长上报
    engine.send_did("WRITE", "上报频率D104", "03 00 00")
    engine.expect_did("WRITE", "上报频率D104", "03 00 00")
    # 关闭湿度步长上报
    engine.send_did("WRITE", "上报频率D104", "04 00 00")
    engine.expect_did("WRITE", "上报频率D104", "04 00 00")

    # 查询温湿度定频
    engine.send_did("READ", "上报频率D104", "03")
    engine.expect_did("READ", "上报频率D104", "03 00 00")
    engine.send_did("READ", "上报频率D104", "04")
    engine.expect_did("READ", "上报频率D104", "04 00 00")

    engine.report_check_enable_all(False)  # 关闭上报检测











