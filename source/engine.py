#encoding:utf-8
import os
import logging

logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s', level=logging.DEBUG)

from docx_engine import DocxEngine
from media import Media
from protocol import Protocol
from session import SessionSuit
from protocol.smart7e_protocol import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
from validator import *
from tools.converter import *
from test_case import TestCaseInfo
from case_editor import CaseEditor
from copy import deepcopy
import json
import re
from public_case import PublicCase,FunCaseAdapter
import types
from tools.filetool import get_file_list
import importlib

class TestEngine(object):
    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = TestEngine()
        return cls._instance

    def __init__(self):
        self.doc_engine = DocxEngine()
        self.com_medias = []
        self.current_group = None
        self.current_test = None
        self.all_infos = []
        self.test_name = None
        self.output_dir = ""

    def get_default_role(self):
        return self.com_medias[0]

    def config_test_program_name(self, name):
        self.test_name = name

    def create_com_device(self, name):
        role = Role(name)
        self.com_medias.append(role)
        return role

    def group_begin(self, name, func, brief=None):
        logging.info("start test group %s", name)
        self.current_group = TestCaseInfo(name,func,brief)
        self.all_infos.append(self.current_group)
        self.current_test = self.current_group

    def group_end(self, name):
        self.current_group = None

    def test_begin(self, name, func, brief):
        logging.info("start test case %s", name)
        self.current_test = self.current_group.add_sub_case(name,func, brief)

    def test_end(self, name):
        self.current_test = None

    def add_fail_test(self,role, tag, msg):
        self.current_test.add_fail_test(role, tag, msg)
        logging.info("case %s fail, %s %s ", self.current_test.name, tag, msg)

    def add_normal_operation(self,role, tag, msg):
        self.current_test.add_normal_operation(role, tag, msg)

    def summary(self, infos):
        total, passed = 0,0
        fails = []
        for case in infos:
            case_total, case_passed ,fail = case.summary()
            passed += case_passed
            total += case_total
            fails.extend(fail)
        return total, passed, fails

    def generate_test_report(self, valids):
        self.doc_engine.write_doc_head(self.test_name)
        total, passed, failes = self.summary(valids)
        self.doc_engine.write_summary(total, passed, failes, valids)
        self.doc_engine.write_detail(valids)
        self.doc_engine.save_doc(self.output_dir)

    def get_valid_infos(self):
        valids = []
        for group in self.all_infos:
            if group.is_enable():
                valids.append(group)
        return valids

    def run_single_case(self,case):
        return self.run_all_test([self.all_infos[0], case])

    def run_all_test(self, valids=None):
        def run_test(case):
            func = case.func
            case.clear()
            try:
                func()
            except Exception as e:
                msg = e.__traceback__.tb_frame.f_globals["__file__"]
                msg += "  linenumber:{0}".format(e.__traceback__.tb_lineno)
                self.add_fail_test("engine", "exception", "测试运行异常_" + msg)
                logging.exception(e)
        if valids is None:
            valids = self.get_valid_infos()
        for group in valids:
            self.current_group = group
            self.current_test = group
            if self.current_group.func is None:
                for case in group.get_valid_sub_cases():
                    self.current_test = case
                    run_test(case)
            else:
                run_test(self.current_group)
        total, passed, fails = TestEngine.instance().summary(valids)
        if total == passed:
            logging.info("测试通过：totoal:%d  passed:%d", total, passed)
        else:
            logging.info("测试失败：totoal:%d  passed:%d", total, passed)
            for case in fails:
                logging.info("失败测试名称：%s 失败原因：%s", case.name, case.get_fail_msg())
        self.generate_test_report(valids)

    def is_exist_config(self):
        file_path = os.path.join(self.output_dir, "config.json")
        return os.path.exists(file_path)

    def save_config(self):
        outputs = {}
        for group in self.all_infos:
            outputs[group.name] = group.config_dict()
        file_path = os.path.join(self.output_dir, "config.json")
        with open(file_path, "w",encoding="utf-8") as handle:
            json.dump(outputs,handle,ensure_ascii=False,indent=4)

    def load_config(self):
        file_path = os.path.join(self.output_dir, "config.json")
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as handle:
                config = json.load(handle)
                for group in self.all_infos:
                    if group.name in config:
                        group.load_config(config[group.name])
                    else:
                        group.load_default()

    def set_output_dir(self, path):
        self.output_dir = path

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

class MockDevice(object):
    def __init__(self, name, src , dst):
        self.name = name
        self.src = src
        self.dst = dst


class Role(object):
    def __init__(self, name, media="SerialMedia", protocol="Smart7eProtocol"):
        self.name = name
        self.media = Media.create_sub_class(media)
        self.protocol = Protocol.create_sub_class(protocol)
        self.session = SessionSuit.create_binary_suit(self.media, self.protocol)
        self.session.data_snd.connect(self.log_snd_frame)
        self.session.data_ready.connect(self.handle_rcv_msg)
        self.timer = QTimer()
        self.timer.timeout.connect(self.timeout_handle)
        self.waiting = False
        self.validate = None
        self.devices = []
        self.default_device = None

    def timeout_handle(self):
        self.handle_rcv_msg(None)


    def config_com(self, **kwargs):
        self.media.config(**kwargs)

    def create_device(self, name, src, dst):
        device = MockDevice(name, src, dst)
        self.devices.append(device)
        if self.default_device is None:
            self.default_device = device
        self.send_local_msg("设置应用层地址", src)
        self.expect_local_msg(["确认", "否认"], timeout=2)

    def send_local_msg(self, cmd, value, **kwargs):
        fbd = LocalFBD(cmd, value)
        data = Smart7EData(0, 0, fbd)
        self.session.write(data)

    def expect_local_msg(self, cmd, value=None, timeout=2, **kwargs):
        self.waiting = True
        self.validate = SmartLocalValidator(cmd=cmd)
        self.timer.start(timeout * 1000)
        while self.waiting:
            QCoreApplication.instance().processEvents()

    def send_did(self, cmd, did, value=None, **kwargs):
        did_cls = DIDRemote.find_class_by_name(did)
        if isinstance(value, str):
            value = hexstr2bytes(value)
        fbd = RemoteFBD.create(cmd, did, value, **kwargs)
        data = Smart7EData(self.default_device.src, self.default_device.dst, fbd)
        self.session.write(data)

    def expect_did(self, cmd, did, value=None, timeout=2, ack=False, **kwargs):
        self.waiting = True
        self.timer.start(timeout*1000)
        cmd = CMD.to_enum(cmd)
        did_cls = DIDRemote.find_class_by_name(did)

        if isinstance(value, str):
            if did_cls.is_value_string(value):
                value = str2bytearray(value)
            else:
                value = BytesCompare(value)
        elif isinstance(value, types.FunctionType):
            value = FunctionCompare(value)
        elif isinstance(value,Validator):
            pass
        elif value is None and len(kwargs) > 0:
            value = BytesCompare(did_cls.encode_reply(**kwargs))
        elif value is not None:
            self.value = value
        else:
            raise ValueError
        self.validate = SmartOneDidValidator(src=self.default_device.dst,
                                             dst= self.default_device.src,
                                             cmd=cmd,
                                             did=did_cls.DID,
                                             value=value,
                                             ack =ack,
                                             **kwargs)
        while self.waiting:
            QCoreApplication.instance().processEvents()

    def handle_rcv_msg(self, data):
        if data is not None:
            self.log_rcv_frame(data)
        if self.validate is not None:
            valid, msg = self.validate(data)
            if valid:
                TestEngine.instance().add_normal_operation(self.name, "expect success", msg)
            else:
                TestEngine.instance().add_fail_test(self.name, "expect fail", msg)
            if self.validate.ack:
                self.ack_report_message(data)
            self.waiting = False
            self.validate = None
            self.timer.stop()

    def wait(self, seconds, expect_no_message):
        self.waiting = True
        self.validate = NoMessage(expect_no_message)
        self.timer.start(seconds * 1000)
        current = self.timer.remainingTime()
        while self.waiting:
            if current - self.timer.remainingTime() > 2000:
                current = self.timer.remainingTime()
                logging.info("\rleft %ds",current//1000)
            QCoreApplication.instance().processEvents()

    def ack_report_message(self, data):
        data = data.ack_message()
        self.session.write(data)

    def log_snd_frame(self, data):
        TestEngine.instance().add_normal_operation(self.name, "snd", str(data))
        TestEngine.instance().add_normal_operation(self.name, "annotation", data.to_readable_str())
        logging.info("snd %s", str(data))
        logging.info("txt %s", data.to_readable_str())

    def log_rcv_frame(self, data):
        TestEngine.instance().add_normal_operation(self.name, "rcv", str(data))
        TestEngine.instance().add_normal_operation(self.name, "annotation", data.to_readable_str())
        logging.info("rcv %s", str(data))
        logging.info("txt %s", data.to_readable_str())


def create_device(name):
    return TestEngine.instance().create_com_device(name)


def add_fail_test(tag, msg):
    TestEngine.add_fail_test(msg)


def add_doc_info(msg):
    TestEngine.instance().add_normal_operation("", "doc", msg)
    logging.info(msg)

def group_begin(name):
    return TestEngine.instance().group_begin(name)


def group_end(name):
    return TestEngine.instance().group_end(name)


def test_begin(name):
    return TestEngine.instance().test_begin(name)


def test_end(name):
    return TestEngine.instance().test_end(name)


def generate_test_report():
    TestEngine.instance().generate_test_report()

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
        com.create_device("monitor", infos["抄控器默认源地址"], infos["测试设备地址"])
    TestEngine.instance().group_begin("测试配置信息", init_func,None)

def get_config():
    return TestEngine.instance().config

def send_did(cmd, did, value=None, **kwargs):
    role = TestEngine.instance().get_default_role()
    role.send_did(cmd, did, value=value, **kwargs)


def expect_did(cmd, did, value=None, timeout=2, ack=False, **kwargs):
    role = TestEngine.instance().get_default_role()
    role.expect_did(cmd, did, value=value, timeout=timeout, ack=ack, **kwargs)

def send_local_msg(cmd, value=None, **kwargs):
    role = TestEngine.instance().get_default_role()
    role.send_local_msg(cmd, value, **kwargs)

def expect_local_msg(cmd, value=None, **kwargs):
    role = TestEngine.instance().get_default_role()
    role.expect_local_msg(cmd, value, **kwargs)

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
        if key.endswith("test"):
            tests.append(value)
    return tests

def _parse_func_testcase(tests):
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


def run_all_tests(funcs, gui=False):
    tests = gather_all_test(funcs)
    _parse_public_test_case()
    _parse_func_testcase(tests)
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