#encoding:utf-8
import os
import logging
from docx_engine import DocxEngine
from media import Media
from protocol import Protocol
from session import SessionSuit
from protocol.smart7e_protocol import *
from PyQt5.QtCore import *
import sys
from validator import *
from tools.converter import *
from test_case import TestCaseInfo
from case_editor import CaseEditor
from PyQt5.QtWidgets import *
logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s', level=logging.DEBUG)



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
        self.test_infos = []
        self.test_name = None

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
        self.test_infos.append(self.current_group)
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

    def summary(self):
        total, passed = 0,0
        fails = []
        for case in self.test_infos:
            case_total, case_passed ,fail = case.summary()
            passed += case_passed
            total += case_total
            fails.extend(fail)
        return total, passed, fails

    def generate_test_report(self):
        self.doc_engine.write_doc_head(self.test_name)
        total, passed, failes = self.summary()
        self.doc_engine.write_summary(total, passed, failes, self.test_infos)
        self.doc_engine.write_detail(self.test_infos)
        self.doc_engine.save_doc()

    def run_all_test(self):
        def run_test(func):
            try:
                func()
            except Exception as e:
                msg = e.__traceback__.tb_frame.f_globals["__file__"]
                msg += "  linenumber:{0}".format(e.__traceback__.tb_lineno)
                self.add_fail_test("engine", "exception", "测试运行异常_" + msg)
                logging.exception(e)
        for group in self.test_infos:
            self.current_group = group
            self.current_test = group
            if self.current_group.func is None:
                for case in group.subcases:
                    self.current_test = case
                    run_test(case.func)
            else:
                run_test(self.current_group.func)
        total, passed, fails = TestEngine.instance().summary()
        if total == passed:
            logging.info("测试通过：totoal:%d  passed:%d", total, passed)
        else:
            logging.info("测试失败：totoal:%d  passed:%d", total, passed)
            for case in fails:
                logging.info("失败测试名称：%s 失败原因：%s", case.name, case.get_fail_msg())




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
        self.waiting = False
        self.timer.stop()
        TestEngine.instance().add_fail_test(self.name, "fail", "no return")

    def config_com(self, **kwargs):
        self.media.config(**kwargs)

    def create_device(self, name, src, dst):
        device = MockDevice(name, src, dst)
        self.devices.append(device)
        if self.default_device is None:
            self.default_device = device
        fbd = LocalFBD(DIDLocal.SET_APPLICATION_ADDR, src)
        data = Smart7EData(0, 0, fbd)
        self.session.write(data)
        self.expect_local_message([DIDLocal.ACTION_OK, DIDLocal.ACTION_FAIL], timeout=2)

    def send_1_did(self, cmd, did, value=bytes(), **kwargs):
        did_cls = DIDRemote.find_class_by_name(did)
        if isinstance(value, str):
            value = hexstr2bytes(value)
        fbd = RemoteFBD.create(cmd, did, value)
        data = Smart7EData(self.default_device.src, self.default_device.dst, fbd)
        self.session.write(data)

    def expect_1_did(self, cmd, did, value=None, timeout=2, **kwargs):
        self.waiting = True
        self.timer.start(timeout*1000)
        cmd = CMD.to_enum(cmd)
        did_cls = DIDRemote.find_class_by_name(did)

        if isinstance(value, str):
            if  did_cls.is_value_string(value):
                value = str2bytearray(value)
            else:
                value = BytesCompare(value)
        self.validate = SmartOneDidValidator(src=self.default_device.dst, dst= self.default_device.src, cmd=cmd, did=did_cls.DID, value=value)
        while self.waiting:
            QCoreApplication.instance().processEvents()

    def expect_local_message(self, cmd, timeout=2):
        self.waiting = True
        self.validate = SmartLocalValidator(cmd=cmd)
        self.timer.start(timeout * 1000)
        while self.waiting:
            QCoreApplication.instance().processEvents()

    def handle_rcv_msg(self, data):
        self.log_rcv_frame(data)
        if self.validate is not None:
            valid, msg = self.validate(data)
            if valid:
                TestEngine.instance().add_normal_operation(self.name, "expect success", msg)
            else:
                TestEngine.instance().add_fail_test(self.name, "expect fail", msg)
            self.waiting = False
            self.validate = None

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

def wait(seconds, msg=""):
    import time
    while seconds >=0 :
        seconds -= 1
        time.sleep(1)
        logging.info("we will wait  %d s, %s", seconds, msg)


def create_test_case(fun, *args, **kwargs):
    from functools import partial
    test_case = partial(fun, *args, **kwargs)
    test_case.__doc__ = fun.__doc__
    return test_case


def config(infos):
    TestEngine.instance().config_test_program_name(infos["测试程序名称"])
    com = TestEngine.instance().create_com_device(infos["串口"])
    def init_func():
        nonlocal com
        com.config_com(port=infos["串口"], baudrate=infos["波特率"], parity=infos["校验位"])
        com.create_device("monitor", infos["抄控器默认源地址"], infos["抄控器默认目的地址"])
    TestEngine.instance().group_begin("测试配置信息", init_func,None)


def add_test_case(name, *args, **kwargs):
    pass

def send_1_did(cmd, did, value=bytes(), **kwargs):
    role = TestEngine.instance().get_default_role()
    role.send_1_did(cmd, did, value=value, **kwargs)


def expect_1_did(cmd, did, value=bytes(), **kwargs):
    role = TestEngine.instance().get_default_role()
    role.expect_1_did(cmd, did, value=value, **kwargs)


def run_all_tests(funcs, gui=False):
    inits = []
    tests = []
    for key, value in funcs.items():
        if key.endswith("init"):
            inits.append(value)
        if key.endswith("test"):
            tests.append(value)

    for init in inits:
        init()

    for test in tests:
            doc_string = test.__doc__
            if doc_string is None:
                doc_string = "默认"
            doc_string = doc_string.strip()
            names = doc_string.split("\n")
            brief = None
            if len(names) >= 2:
                brief = "".join(names[1:])
            doc_string = names[0]
            names = doc_string.split(".")
            if len(names) >= 2:
                import re
                search = re.search(r"group:(.*)case:(.*)", brief, re.S)
                group_brief = None
                if search is not None:
                    group_brief = search.group(1)
                    brief = search.group(2)
                if len(names[0]) >= 2:
                    TestEngine.instance().group_begin(names[0], None, group_brief)
                TestEngine.instance().test_begin(names[1], test, brief)
            else:
                TestEngine.instance().group_begin(names[0], test, brief)

    if gui:
       app = QApplication(sys.argv)
       ui = CaseEditor(TestEngine.instance())
       ui.show()
       sys.exit(app.exec_())
    else:
        app = QCoreApplication(sys.argv)
        TestEngine.instance().run_all_test()
        generate_test_report()

    exit(0)


