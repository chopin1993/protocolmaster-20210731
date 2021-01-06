#encoding:utf-8
from tools.esloging import *
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QApplication
import sys
from engine.case_editor import CaseEditor
from .interface_helper import *
from user_exceptions import MeidaException


def config(infos):
    """
    配置项目基本信息
    :param infos:字典，项目信息
    """
    TestEngine.instance().config = infos
    TestEngine.instance().config_test_program_name(infos["测试程序名称"])
    TestEngine.instance().create_com_device(infos["串口"])


def get_config():
    """
    获取全局项目配置信息
    :return 字典
    """
    return TestEngine.instance().config


def send_did(cmd, did, value=None, taid=None, gids=None, gid_type="U16", **kwargs):
    """
    发送7e报文
    :param cmd:支持“READ”,"WRITE","REPORT","NOTIFY"(不可靠上报)
    :param did:可以使用数字，也可以使用《数据表示分类表格》的中文名称
    :param value:可是数字,也可以是类似于“00 34 78”的字符串
    :param taid:目标地址
    :param gids:组地址列表，可以是组地址列表。
    :param gid_type: 组地址编码类型，支持"BIT1","U8","U16"
    :param kwargs:如果数据标识中有多个数据单元，可以使用key,value的方式赋值
    """
    role = TestEngine.instance().get_default_role()
    role.send_did(cmd, did, value=value, taid=taid, gids=gids, gid_type=gid_type, **kwargs)


def expect_did(cmd, did, value=None,
               timeout=2, ack=False, said=None,
               gids=None, gid_type="U16",
               check_seq=True,
               **kwargs):
    """
    :param cmd: 支持“READ”,"WRITE","REPORT","NOTIFY""
    :param did: 可以使用数字，也可以使用《数据表示分类表格》的中文名称
    :param value:可是数字,也可以是类似于“00 34 78”的字符串, 可以使用*作为占位符"** **",可以传入函数
    :param timeout:
    :param ack: 是否给与回复
    :param gids:广播地址列表
    :param gid_type:广播地址编码类型 支持"BIT1","U8","U16"
    :param check_seq: True:比对seq, False:忽略seq
    :param kwargs: 如果did有多个数据项，可以使用key,value的方式传递数据
    """
    role = TestEngine.instance().get_default_role()
    role.expect_did(cmd,
                    did,
                    value=value,
                    timeout=timeout,
                    ack=ack,
                    said=said,
                    gids=gids,
                    gid_type=gid_type,
                    check_seq=check_seq,
                    **kwargs)


def send_multi_dids(cmd, *args, taid=None):
    """
    :param cmd:支持“READ”,"WRITE","REPORT","NOTIFY"
    :param args:did1,value1,did2,value2...did和value交替排列
    :param taid:目的地址，默认是被测设备
    """
    role = TestEngine.instance().get_default_role()
    assert len(args)%2 == 0
    padding_args = []
    for i in range(0,len(args),2):
        padding_args.append(None)
        padding_args.append(None)
        padding_args.append(args[i])
        padding_args.append(args[i+1])
    role.send_multi_dids(cmd, *padding_args, taid=taid)


def expect_multi_dids(cmd, *args,
                      timeout=2, ack=False, said=None,
                      check_seq=True):
    """
    期望收到多个did
    :param cmd:支持“READ”,"WRITE","REPORT","NOTIFY"
    :param args:did1,value1,did2,value2...did和value交替排列
    :param timeout:超时时间
    :param ack:是否给与回复，主要在上报的时候使用
    :param said: 目标设备地址，默认发给被测设备
    :param check_seq: True:比对seq, False:忽略seq
    """
    padding_args = []
    for i in range(0, len(args), 2):
        padding_args.append(None)
        padding_args.append(None)
        padding_args.append(args[i])
        padding_args.append(args[i + 1])

    role = TestEngine.instance().get_default_role()
    role.expect_multi_dids(cmd, *padding_args, timeout=timeout, ack=ack,
                           said=said,
                           check_seq=check_seq)

def broadcast_send_multi_dids(cmd, *args):
    """
    :param cmd:支持“READ”,"WRITE","REPORT","NOTIFY"
    :param args:gid1, gidtyp1,did1,value1,gid2,gidtyp2 did2,value2...gid1,gidtyp1,did和value顺序排列
    """
    role = TestEngine.instance().get_default_role()
    role.send_multi_dids(cmd, *args, taid=0xffffffff)


def broadcast_expect_multi_dids(cmd, *args,
                                timeout=2, ack=False, said=None,
                                check_seq=True):
    """
    期望收到多个广播did
    :param cmd:支持“READ”,"WRITE","REPORT","NOTIFY"
    :param args:gid1, gidtyp1,did1,value1,gid2,gidtyp2 did2,value2...gid1,gidtyp1,did和value顺序排列
    :param said:目的地址，默认是被测设备
    :param timeout:超时时间
    :param ack:是否给与回复，主要在上报的时候使用
    :param check_seq: True:比对seq, False:忽略seq
    """
    role = TestEngine.instance().get_default_role()
    role.expect_multi_dids(cmd, *args, timeout=timeout, ack=ack,
                           said=said,
                           check_seq=check_seq)

def send_raw(fbd, taid=None):
    """
    发送组织帧
    :param fbd:自组fbd帧
    :taid:目标地址
    """
    role = TestEngine.instance().get_default_role()
    role.send_raw(fbd, taid=taid)


def expect_raw(fbd, said=None, timeout=2):
    """
    发送组织帧
    :param fbd:自组fbd帧
    :param said:源地址
    """
    role = TestEngine.instance().get_default_role()
    role.expect_raw(fbd, said, timeout=timeout)


def send_local_msg(cmd, value=None, **kwargs):
    """
    :param cmd: 查询数据标识分类.xls中中的localcmd数据表。
    :param value: 发送数据
    """
    role = TestEngine.instance().get_local_routine()
    role.send_local_msg(cmd, value, **kwargs)


def expect_local_msg(cmd, value=None, **kwargs):
    """
    :param cmd: 查询数据标识分类.xls中中的localcmd数据表。
    :param value：期望收到数据
    """
    role = TestEngine.instance().get_local_routine()
    role.expect_local_msg(cmd, value, **kwargs)


def update(file_name,  update_func=None, control_func=None, block_size=128):
    """
    升级程序
    :param file_name:程序升级名称
    :param update_func:控制程序。func的参数是请求的包，返回的是要发送的包。返回None表示不予回复。此函数不能发送和expect报文
    :param control_func:升级过程中发送报文的函数。参数是升级用的时间，此函数可以发送和expect报文。
    :return 设备请求的seqs列表。
    """
    from tools.filetool import get_config_file
    from protocol.smart7e_protocol import CMD
    files = []
    file_name = file_name + ".bin"
    updater = TestEngine.instance().get_updater()
    file_name1 = os.path.join(TestEngine.instance().output_dir, file_name)
    files.append(file_name1)
    if os.path.exists(file_name1):
        return updater.update(CMD.UPDATE, file_name1, block_size, update_func, control_func)
    file_name2 = get_config_file(os.path.join("升级文件",file_name))
    files.append(file_name2)
    if os.path.exists(file_name2):
        return updater.update(CMD.UPDATE_PLC, file_name2, block_size, update_func, control_func)
    raise FileNotFoundError(str(files))



def run_all_tests(gui=False):
    """
    自动扫描公共用例和项目文件夹下测试用例中所有的测试用例，并执行。
    :param gui: True: 显示gui界面 False：自动执行保存的配置
    """
    parse_func_testcase()
    parse_public_test_case()
    try:
        TestEngine.instance().load_config()
    except Exception as e:
        logging.exception(e)
        exit(0)
    if gui:
       app = QApplication(sys.argv)
       ui = CaseEditor(TestEngine.instance())
       ui.show()
       sys.exit(app.exec_())
    else:
        app = QCoreApplication(sys.argv)
        TestEngine.instance().run_all_test()
    exit(0)


def create_role(name, address):
    """
    创建陪测设备
    :param name:陪测设备名称
    :param address: 陪测设备地址
    """
    return TestEngine.instance().get_default_equiment().create_role(name, address)


def add_fail_test(msg):
    """
    手动设置测试失败
    :param msg: 测试失败的提示信息。
    """
    TestEngine.instance().add_fail_test("user",  "fail", msg=msg)


def add_doc_info(msg):
    """
    手动增加测试帮助信息
    :param msg: 测试辅助信息
    """
    TestEngine.instance().add_normal_operation("", "doc", msg)


def wait(seconds, allowed_message=True, said=None,tips=""):
    """
    :param seconds:等待时间
    :param allowed_message:True:等待时无论是否收到报文测试都会成功  False:等待时收到报文测试失败，：
    :param tips:等待显示的提示信息
    :return:
    """
    assert seconds > 0, "等待时间必须大于0"
    msg ="we will wait {0}s {1}".format(seconds, tips)
    logging.info(msg)
    role = TestEngine.instance().get_default_role()
    role.wait(seconds, allowed_message, said=said)


def report_check_enable_all(enable):
    """
    使能/禁止所有设备的上报检测
    :param enable: True: 检测上报报文 False:忽略上报报文。默认设备忽略上报报文
    """
    TestEngine.instance().report_enable = enable


def control_relay(channel, value):
    """
    控制工装继电器的开关
    :param channel:继电器通道
    :param status:继电器通道
    """
    add_doc_info("msg channel {} value {}".format(channel, value))
    equiment = TestEngine.instance().get_default_equiment()
    equiment.control_relay(channel, value)


def setting_uart(channel, baudrate, parity):
    """
    配置监控器的串口
    :param channel:通道
    :param baudrate:波特率
    :param parity:校验位 奇校验、偶校验、无校验
    """
    equiment = TestEngine.instance().get_default_equiment()
    config = get_config()
    equiment.config_com(port=config["串口"], baudrate=config["波特率"], parity=config["校验位"])
    equiment.setting_uart(channel, baudrate, parity)


def reset_swb_bus(channel=0):
    """
    复位监测口
    :param channel:监测口通道号
    """
    equiment = TestEngine.instance().get_default_equiment()
    equiment.reset_swb_bus(channel)


def expect_cross_zero_status(channel, value):
    """
    过零检测电路状态
    :param channel:过零通道
    :param value:期望过零电路状态
    """
    equiment = TestEngine.instance().get_default_equiment()
    equiment.expect_cross_zero_status(channel, value)


def set_device_sensor_status(sensor, value=bytes(), channel=0):
    """
    设置设备的传感器输入值
    :param senor:       以下类型是U32类型
                        温度 = 1
                        湿度 = 2
                        电压 = 3
                        电流 = 4
                        电阻 = 5
                        大量程照度 = 31
                        自然光照度 = 32
                        照度 = 33

                        以下传感器是U8类型
                        雷达人体存在 = 11
                        光学人体存在 = 12
                        红外传感器 = 13
                        插卡取电 = 21
                        继电器输出 = 41
                        光耦输出 = 42
                        可控硅输出 = 43
                        干节点输入 = 52
                        干簧管输入 = 53
                        二进制输入 = 61
                        二进制输出 = 62

                        枚举类型：
                        按键输入 = 51 1:短按 2:长按

                        字节类型 = 80
    :param value:  根据传感器类型赋值,使用默认值表示传感器状态
    :param channel: 传感器通道
    """
    equiment = TestEngine.instance().get_default_equiment()
    equiment.set_device_sensor_status(sensor, value, channel)

def expect_device_output_status(sensor, value, channel=0, wait_time=0):
    """
    通过监测器检查设备的状态
    :param sensor:
    :param senor:      以下类型是U32类型
                        温度 = 1
                        湿度 = 2
                        电压 = 3
                        电流 = 4
                        电阻 = 5
                        大量程照度 = 31
                        自然光照度 = 32
                        照度 = 33

                        以下传感器是U8类型
                        雷达人体存在 = 11
                        光学人体存在 = 12
                        红外传感器 = 13
                        插卡取电 = 21
                        继电器输出 = 41
                        光耦输出 = 42
                        可控硅输出 = 43
                        干节点输入 = 52
                        干簧管输入 = 53
                        二进制输入 = 61
                        二进制输出 = 62

                        枚举类型：
                        按键输入 = 51 1:短按 2:长按

                        字节类型 = 80
    :param value: 根据传感器类型赋值
    :param channel: 传感器通道
    :param wait_time:检测状态之前等待的时间
    """
    if wait_time > 0:
        wait(wait_time)
    equiment = TestEngine.instance().get_default_equiment()
    equiment.expect_device_output_status(sensor, value, channel)
