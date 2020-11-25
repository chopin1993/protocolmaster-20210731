#encoding:utf-8
import os
import logging
logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s', level=logging.DEBUG)
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QApplication
import sys
from engine.case_editor import CaseEditor
from .interface_helper import *


def config(infos):
    """
    配置项目基本信息
    :param infos:字典，项目信息
    """
    TestEngine.instance().config = infos
    TestEngine.instance().config_test_program_name(infos["测试程序名称"])
    com = TestEngine.instance().create_com_device(infos["串口"])
    def init_func():
        nonlocal com
        com.config_com(port=infos["串口"], baudrate=infos["波特率"], parity=infos["校验位"])
        com.create_role("monitor", infos["抄控器默认源地址"])
    TestEngine.instance().group_begin("测试配置信息", init_func,None)


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
    :param dst:目标地址
    :param gids:组地址列表，可以是组地址列表。
    :param gid_type: 组地址编码类型，支持"BIT1","U8","U16"
    :param kwargs:如果数据标识中有多个数据单元，可以使用key,value的方式赋值
    """
    role = TestEngine.instance().get_default_role()
    role.send_did(cmd, did, value=value, taid=taid, gids=gids, gid_type=gid_type, **kwargs)


def expect_did(cmd, did, value=None, timeout=2, ack=False, said=None, gids=None, gid_type="U16",**kwargs):
    """
    :param cmd: 支持“READ”,"WRITE","REPORT","NOTIFY""
    :param did: 可以使用数字，也可以使用《数据表示分类表格》的中文名称
    :param value:可是数字,也可以是类似于“00 34 78”的字符串, 可以使用*作为占位符"** **",可以传入函数
    :param timeout:
    :param ack: 是否给与回复
    :param gids:广播地址列表
    :param gid_type:广播地址编码类型 支持"BIT1","U8","U16"
    :param kwargs: 如果did有多个数据项，可以使用key,value的方式传递数据
    """
    role = TestEngine.instance().get_default_role()
    role.expect_did(cmd,
                    did,
                    value=value,
                    timeout=timeout,
                    ack=ack,
                    said=said,
                    gids=None,
                    gid_type="U16",
                    **kwargs)


def send_multi_dids(cmd, *args, taid=None, gids=None, gid_type="U16"):
    """
    :param cmd:支持“READ”,"WRITE","REPORT","NOTIFY"
    :param args:did1,value1,did2,value2...did和value交替排列
    :param dst:目的低点至，默认是被测设备
    :param gids:广播地址列表
    :param gid_type:广播地址编码类型 支持"BIT1","U8","U16"
    """
    role = TestEngine.instance().get_default_role()
    role.send_multi_dids(cmd, *args, taid=taid, gids=gids, gid_type=gid_type)


def expect_multi_dids(cmd, *args, timeout=2, ack=False, said=None, gids=None,gid_type="U16"):
    """
    :param cmd:支持“READ”,"WRITE","REPORT","NOTIFY"
    :param args:did1,value1,did2,value2...did和value交替排列
    :param timeout:超时时间
    :param ack:是否给与回复，主要在上报的时候使用
    :param gids:广播地址列表
    :param gid_type:广播地址编码类型 支持"BIT1","U8","U16"
    :return:
    """
    role = TestEngine.instance().get_default_role()
    role.expect_multi_dids(cmd, *args, timeout=timeout, ack=ack, said=said,gids=gids, gid_type=gid_type)


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


def update(file_name,  control_func=None, block_size=128):
    """
    升级程序
    :param file_name:程序升级名称
    :param control_func:控制程序。func的参数是请求的包，返回的是要发送的包。返回None表示不予回复。
    :return 设备请求的seqs列表。
    """
    updater = TestEngine.instance().get_updater()
    file_name = os.path.join(TestEngine.instance().output_dir, file_name)
    return updater.update(file_name, block_size, control_func)


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
    return TestEngine.instance().get_default_device().create_role(name,address)


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
    logging.info(msg)


def wait(seconds, allowed_message=True, tips=""):
    """
    :param seconds:等待时间
    :param allowed_message:True:等待时无论是否收到报文测试都会成功  False:等待时收到报文测试失败，：
    :param tips:等待显示的提示信息
    :return:
    """
    msg ="we will wait {0}s {1}".format(seconds, tips)
    logging.info(msg)
    role = TestEngine.instance().get_default_role()
    role.wait(seconds, allowed_message)


def report_check_enable(enable):
    """
    使能/禁止检测上报报文
    :param enable: True: 检测上报报文 False:忽略上报报文。默认设备忽略上报报文
    """
    role = TestEngine.instance().get_default_role()
    role.report_check_enable(enable)