#encoding:utf-8
import os
import logging
logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s', level=logging.DEBUG)
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QApplication
import sys
from engine.case_editor import CaseEditor
import re
from engine.public_case import FunCaseAdapter
from tools.filetool import get_file_list
import importlib
import time
from .test_engine import TestEngine


def set_output_dir(path):
    import os
    def to_source_dir(path):
        ret = re.search(r"(.*)autotest.*",path)
        if ret is None:
            return None
        return ret.group(1)
    source_path = to_source_dir(path)
    if source_path is not None:
        os.chdir(source_path)
    TestEngine.instance().set_output_dir(path)


def create_role(name, address):
    return TestEngine.instance().get_default_device().create_role(name,address)


def add_fail_test(tag, msg):
    TestEngine.add_fail_test(msg)


def add_doc_info(msg):
    TestEngine.instance().add_normal_operation("", "doc", msg)
    logging.info(msg)


def wait(seconds, expect_no_message=False, tips=""):
    msg ="we will wait {0}s, {1}".format(seconds, tips)
    logging.info(msg)
    role = TestEngine.instance().get_default_role()
    role.wait(seconds, expect_no_message)


def create_test_case(fun, *args, **kwargs):
    from functools import partial
    test_case = partial(fun, *args, **kwargs)
    test_case.__doc__ = fun.__doc__
    return test_case


def config(infos):
    TestEngine.instance().config = infos
    TestEngine.instance().config_test_program_name(infos["测试程序名称"])
    com = TestEngine.instance().create_com_device(infos["串口"])
    def init_func():
        nonlocal com
        com.config_com(port=infos["串口"], baudrate=infos["波特率"], parity=infos["校验位"])
        com.create_role("monitor", infos["抄控器默认源地址"])
    TestEngine.instance().group_begin("测试配置信息", init_func,None)


def get_config():
    return TestEngine.instance().config


def send_did(cmd, did, value=None,dst=None, **kwargs):
    """
    发送7e报文
    :param cmd:支持“READ”,"WRITE","REPORT
    :param did:可以使用数字，也可以使用《数据表示分类表格》的中文名称
    :param value:可是数字,也可以是类似于“00 34 78”的字符串
    :param dst:目标地址
    :param kwargs:如果数据标识中有多个数据单元，可以使用key,value的方式赋值
    """
    role = TestEngine.instance().get_default_role()
    role.send_did(cmd, did, value=value,dst=dst, **kwargs)

def expect_multi_dids(cmd, *args, timeout=2, ack=False):
    role = TestEngine.instance().get_default_role()
    role.expect_multi_dids(cmd, *args, timeout=timeout, ack=ack)


def expect_did(cmd, did, value=None, timeout=2, ack=False, **kwargs):
    role = TestEngine.instance().get_default_role()
    role.expect_did(cmd, did, value=value, timeout=timeout, ack=ack, **kwargs)


def send_multi_dids(cmd, *args, dst=None):
    role = TestEngine.instance().get_default_role()
    role.send_multi_dids(cmd, *args, dst=dst)


def send_local_msg(cmd, value=None, **kwargs):
    role = TestEngine.instance().get_default_device()
    role.send_local_msg(cmd, value, **kwargs)


def expect_local_msg(cmd, value=None, **kwargs):
    role = TestEngine.instance().get_default_device()
    role.expect_local_msg(cmd, value, **kwargs)


def update(file_name, func=None, expect_seqs=None):
    """
    升级程序
    :param file_name:程序升级名称
    :param func:控制程序。func的参数是请求的包，返回的是要发送的包。返回None表示不予回复。
    :param expect_seq:期望收到设备的seq。
    :return:
    """
    add_doc_info("升级程序文件："+file_name)
    role = TestEngine.instance().get_default_device()


def _parse_doc_string(doc_string):
    if doc_string is None:
        doc_string = "默认"
    doc_string = doc_string.strip()
    names = doc_string.split("\n")
    brief = None
    if len(names) >= 2:
        briefs = [data.lstrip() for data in names[1:]]
        brief = "\n".join(briefs)
    return names[0],brief


def gather_all_test(variables):
    tests = []
    for key, value in variables.items():
        if key.startswith("test"):
            tests.append(value)
    return tests


def _parse_func_testcase():
    public_dir = os.path.join(TestEngine.instance().output_dir, "测试用例")
    files = get_file_list(public_dir)
    for name in files:
        name = os.path.splitext(name)[0]
        if name.startswith("__"):
            continue
        file = os.path.split(TestEngine.instance().output_dir)[-1]
        mod = importlib.import_module("autotest." + file +".测试用例." + name)
        group_brief = getattr(mod, "测试组说明", None)
        tests = gather_all_test(mod.__dict__)
        TestEngine.instance().group_begin(name, None, group_brief)
        for test in tests:
            case_name, case_brief = _parse_doc_string(test.__doc__)
            test = FunCaseAdapter(test)
            TestEngine.instance().test_begin(case_name, test, case_brief)


def _parse_public_test_case():
    public_dir = os.path.join(TestEngine.instance().output_dir, "..", "公共用例")
    files = get_file_list(public_dir)
    for name in files:
        name = os.path.splitext(name)[0]
        if name.startswith("__"):
            continue
        mod = importlib.import_module("autotest.公共用例." + name)
        group_brief = getattr(mod, "测试组说明", None)
        tests = gather_all_test(mod.__dict__)
        TestEngine.instance().group_begin(name, None, group_brief)
        for test in tests:
            case_name, case_brief = _parse_doc_string(test.__doc__)
            test = FunCaseAdapter(test)
            TestEngine.instance().test_begin(case_name, test, case_brief)


def run_all_tests(gui=False):
    """
    自动扫描公共用例和项目文件夹下测试用例中所有的测试用例，并执行。
    :param gui: True: 显示gui界面 False：自动执行保存的配置
    """
    _parse_public_test_case()
    _parse_func_testcase()
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
