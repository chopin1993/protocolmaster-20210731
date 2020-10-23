# encoding:utf-8

def softversion_helper(monitor, software_version):
    "基本报文测试.软件版本"
    monitor.send_1_did("READ", "DIDSoftversion")
    monitor.expect_1_did("READ", "DIDSoftversion", software_version)


def plc_version_helper(monitor, plc_version):
    "_.PLC版本信息"
    monitor.send_1_did("READ", "DIDPlcVersion")
    monitor.expect_1_did("READ", "DIDPlcVersion", plc_version)


def device_type_helper(monitor, device_type):
    "_.设备类型"
    monitor.send_1_did("READ", "DIDDeviceType")
    monitor.expect_1_did("READ", "DIDDeviceType", device_type)