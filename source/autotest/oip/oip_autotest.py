#encoding:utf-8
import engine

# 配置测试基本参数
config = dict()
config["测试程序名称"] = r"ESSN-OIP-A(v1.1)-20200901"
config["串口"] = "COM9"
config["波特率"] = "9600"
config["校验位"] = 'None'
config["抄控器默认源地址"] = 1
config["测试设备地址"] = 464148
config["设备密码"] = 55013

engine.config(config)


def sensor_data_test():
    """
    传感器数据测试.人体和红外数据读取
    group:本测试主要测试传感器数据的读取
    case:读取人体存在并判断返回数据为10和任意一个字节
    """
    # PERSON_CAMERA = 0x10
    # PERSON_IR = 0x0d
    # ILLUMINACE = 0x0b
    engine.send_1_did("READ", "读传感器数据", "10") #人体存在数据读取
    engine.expect_1_did("READ", "读传感器数据", "10 **") #10 + 任意一个字节
    engine.send_1_did("READ", "读传感器数据", "0d") #红外数据读取
    engine.expect_1_did("READ", "读传感器数据", "0d ** **") #0d + 任意一个字节

def sensor_data2_test():
    """
     _.照度数据读取
    读取照度数据，并判断返回数据为0b 和任意两个字节
    """
    # PERSON_CAMERA = 0x10
    # PERSON_IR = 0x0d
    # ILLUMINACE = 0x0b
    engine.send_1_did("READ", "读传感器数据", "0b") #照度数据读取读取
    engine.expect_1_did("READ", "读传感器数据", "0b ** **") #0b +任意两个字节


def status_step_sync_test():
    """
    状态同步.步长设置、读取
    1. 读取步长
    2. 改变步长
    3. 读取步长，确认步长被改变
    """
    engine.add_doc_info("读取人体存在上报步长，确认默认开启")
    engine.send_1_did("READ", "上报步长","10")
    engine.expect_1_did("READ", "上报步长", "10 01")

    engine.add_doc_info("修改默认步长为0，并读取确认修改成功")
    engine.send_1_did("WRITE", "上报步长", "10 00")
    engine.expect_1_did("WRITE", "上报步长", "10 00")
    engine.send_1_did("READ", "上报步长","10")
    engine.expect_1_did("READ", "上报步长", "10 00")

    engine.add_doc_info("恢复设备默认状态")
    engine.send_1_did("WRITE", "上报步长", "10 01")
    engine.expect_1_did("WRITE", "上报步长", "10 01")

def para_save_test():
    "断电参数保存"
    engine.add_doc_info("设置确认参数信息")
    engine.send_1_did("WRITE", "上报步长", "10 00")
    engine.expect_1_did("WRITE", "上报步长", "10 00")

    engine.add_doc_info("设备复位")
    engine.add_doc_info(" 00： 复位  01： 恢复出厂设置")
    engine.send_1_did("WRITE", "测试命令", "00")
    engine.expect_1_did("WRITE", "测试命令", "00")
    engine.wait(90)
    engine.add_doc_info("读取参数，确保参数保持一致")
    engine.send_1_did("READ", "上报步长","10")
    engine.expect_1_did("READ", "上报步长", "10 00")
    engine.add_doc_info("恢复默认参数")
    engine.send_1_did("WRITE", "上报步长", "10 01")
    engine.expect_1_did("WRITE", "上报步长", "10 01")


def report_test():
    "上报测试.频率上报"
    r"4aid+2panid+2pw+4gid+2sid"
    engine.send_1_did("WRITE", "载波芯片注册信息", aid=config["测试设备地址"],  panid=22, pw=config["设备密码"],gid=1,sid=1)
    engine.expect_1_did("WRITE","载波芯片注册信息", "** ** ** ** ** **")



if __name__ == "__main__":
    import os
    engine.set_output_dir(os.path.dirname(__file__))
    engine.run_all_tests(locals(), gui=True)