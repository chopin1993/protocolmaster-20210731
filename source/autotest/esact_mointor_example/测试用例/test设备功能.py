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