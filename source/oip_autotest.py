#encoding:utf-8
import engine

# 配置测试基本信息
engine.config_test_program_name(r"ESSN-OIP-A(v1.1)-20200901")
monitor = engine.create_role("Monitor")


def evnironment_init():
    "初始化测试环境"
    monitor.config_com(port="COM9", baudrate="9600", parity='None')
    monitor.config_address(src=1, dst=464148)


def plc_version_test():
    "基本报文测试.PLC版本信息"
    monitor.send_1_did("READ", "DIDPlcVersion")
    monitor.expect_1_did("READ", "DIDPlcVersion", "EASTSOFT(v1.0)")

def device_type_test():
    "-.设备类型"
    monitor.send_1_did("READ", "DIDDeviceType")
    monitor.expect_1_did("READ", "DIDDeviceType", "FF FF 0B 00 01 00 00 00")


if __name__ == "__main__":
    engine.run_all_tests(locals())
