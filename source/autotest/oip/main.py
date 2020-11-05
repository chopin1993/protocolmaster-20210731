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
config["panid"] = 22

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
    engine.send_did("READ", "读传感器数据", "10") #人体存在数据读取
    engine.expect_did("READ", "读传感器数据", "10 **") #10 + 任意一个字节
    engine.send_did("READ", "读传感器数据", "0d") #红外数据读取
    engine.expect_did("READ", "读传感器数据", "0d ** **") #0d + 任意一个字节

def sensor_data2_test():
    """
     _.照度数据读取
    读取照度数据，并判断返回数据为0b 和任意两个字节
    """
    # PERSON_CAMERA = 0x10
    # PERSON_IR = 0x0d
    # ILLUMINACE = 0x0b
    engine.send_did("READ", "读传感器数据", "0b") #照度数据读取读取
    engine.expect_did("READ", "读传感器数据", "0b ** **") #0b +任意两个字节


def status_step_sync_test():
    """
    状态同步.步长设置、读取
    1. 读取步长
    2. 改变步长
    3. 读取步长，确认步长被改变
    """
    engine.add_doc_info("读取人体存在上报步长，确认默认开启")
    engine.send_did("READ", "上报步长", "10")
    engine.expect_did("READ", "上报步长", "10 01")
    engine.add_doc_info("修改默认步长为0，并读取确认修改成功")
    engine.send_did("WRITE", "上报步长", "10 00")
    engine.expect_did("WRITE", "上报步长", "10 00")
    engine.send_did("READ", "上报步长", "10")
    engine.expect_did("READ", "上报步长", "10 00")
    engine.add_doc_info("恢复设备默认状态")
    engine.send_did("WRITE", "上报步长", "10 01")
    engine.expect_did("WRITE", "上报步长", "10 01")

def para_save_test():
    "断电参数保存"
    engine.add_doc_info("设置确认参数信息")
    engine.send_did("WRITE", "上报步长", "10 00")
    engine.expect_did("WRITE", "上报步长", "10 00")

    engine.add_doc_info("设备复位")
    engine.add_doc_info(" 00： 复位  01： 恢复出厂设置")
    engine.send_did("WRITE", "测试命令", "00")
    engine.expect_did("WRITE", "测试命令", "00")
    engine.wait(90)
    engine.add_doc_info("读取参数，确保参数保持一致")
    engine.send_did("READ", "上报步长", "10")
    engine.expect_did("READ", "上报步长", "10 00")
    engine.add_doc_info("恢复默认参数")
    engine.send_did("WRITE", "上报步长", "10 01")
    engine.expect_did("WRITE", "上报步长", "10 01")


def report_test():
    """
    上报测试.组网上报测试
    """
    r"4aid+2panid+2pw+4gid+2sid"
    engine.send_local_msg("设置PANID", config["panid"])
    engine.expect_local_msg("确认")

    engine.send_did("WRITE", "载波芯片注册信息",
                    aid=config["测试设备地址"],
                    panid=config["panid"],
                    pw=config["设备密码"],
                    gid=1,
                    sid=1)
    engine.expect_did("WRITE", "载波芯片注册信息", "** ** ** ** ** **")

    engine.add_doc_info("设备组网会启动组网上报，上报一次，重发三次，总共四次")
    engine.expect_did("REPORT", "读传感器数据", "10 **", timeout=3)
    engine.expect_did("REPORT", "读传感器数据", "10 **", timeout=3)
    engine.expect_did("REPORT", "读传感器数据", "10 **", timeout=10)
    engine.expect_did("REPORT", "读传感器数据", "10 **", timeout=15)

    engine.add_doc_info("上报收到回复之后，便不会重发")
    engine.send_did("WRITE", "载波芯片注册信息", aid=config["测试设备地址"], panid=config["panid"], pw=config["设备密码"], gid=1, sid=1)
    engine.expect_did("WRITE", "载波芯片注册信息", "** ** ** ** ** **")
    engine.expect_did("REPORT", "读传感器数据", "10 **", timeout=3, ack=True)
    engine.wait(20, expect_no_message=True,tips="确保20s之内不会收到上报信息")

# def master_test():
#     """
#     主从机测试.从机设备管理
#     group:从机设置主机ID，从机会自动向主机上报信息，主机收到上报信息之后，会将从机id记住，从而完成主从机自动适配的问题。
#     case:主机设备管理逻辑
#     """
#     engine.add_doc_info("1. 确定主机当前没有从机")
#     engine.send_1_did("READ", "读取从机信息", "03")
#     engine.expect_1_did("READ", "读取从机信息", "00")
#
#     engine.add_doc_info("2. 从机向主机上报人体存在信息，主机会记录")
#     salve = engine.create_device("从机1", 2)
#     salve.send_1_did("REPORT","传感器信息", "10 01")
#     salve.expect_1_did("REPORT", "传感器信息", "10 01")
#
#     engine.add_doc_info("3. 读取从机列表，确认从机信息被更新")
#     engine.send_1_did("READ", "读取从机信息", "03")
#     engine.expect_1_did("READ", "读取从机信息", "0 00 000 00 00 0 0")
#
#     engine.add_doc_info("4. 断电重启，确认从机信息被保存")


if __name__ == "__main__":
    import os
    engine.set_output_dir(os.path.dirname(__file__))
    engine.run_all_tests(locals(), gui=True)