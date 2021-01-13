import engine

测试组说明="设备功能测试，主要进行开关测试"

def test_onoff():
    """
    设备开关测试
    测试设备的通断功能是否正常。本测试首先控制通道1开启，然后在控制通道1关闭
    """
    engine.add_doc_info("bit7 bit6(on off) bit5-bit0选中通道")
    engine.add_doc_info("打开继电器 第一通道")
    engine.send_did("WRITE", "通断操作C012", "81")
    engine.expect_did("WRITE", "通断操作C012","01")
    engine.add_doc_info("关闭继电器 第一通道")
    engine.send_did("WRITE", "通断操作C012", "01")
    engine.expect_did("WRITE", "通断操作C012","00")


def test_配置情景模式():
    """
    03_配置情景模式
    """
    engine.add_doc_info('03_配置情景模式')
    engine.add_doc_info('普通长度报文测试')
    engine.send_did("WRITE", "情景模式帧体FC29",
                    '01 01 13 41 49 03 0A 01 64 02 32 08 13 E0 01 01 41 4B 12 C0 01 81')
    engine.expect_did("WRITE", "情景模式帧体FC29",
                      '01 01 13 41 49 03 0A 01 64 02 32 08 13 E0 01 01 41 4B 12 C0 01 81')


    engine.add_doc_info('模拟点击控制按键，进行相关的测试')
    engine.set_device_sensor_status("按键输入", "短按")
    engine.broadcast_expect_multi_dids('WRITE',
                                       [73],'U8','单轨窗帘目标开度0A03','64',
                                       [2,5,6,12],'BIT1','开关机E013','01',
                                       [75],'U8','通断操作C012','81')
    engine.wait(2)
    engine.set_device_sensor_status("按键输入", "短按")
    engine.broadcast_expect_multi_dids('WRITE',
                                       [73],'U8','单轨窗帘目标开度0A03','64',
                                       [2,5,6,12],'BIT1','开关机E013','01',
                                       [75],'U8','通断操作C012','81')