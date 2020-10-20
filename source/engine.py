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

logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s', level=logging.DEBUG)

app = QCoreApplication(sys.argv)


class TestCaseInfo(object):
    def __init__(self, name):
        self.name = name
        self.bodys = []
        self.passed = True
        self.errors = []
        self.subcases = []

    def add_fail_test(self,role, tag, msg):
        self.passed = False
        self.errors.append((role, tag, msg))

    def add_normal_operation(self, role, tag, msg):
        self.bodys.append((role, tag, msg))

    def add_sub_case(self, name):
        case = TestCaseInfo(name)
        self.subcases.append(case)
        return case

    def is_passed(self):
        passed = True
        for sub in self.subcases:
            passed = passed and sub.is_passed()
        return passed and self.passed

    def summary(self):
        if len(self.subcases) > 0:
            total = len(self.subcases)
            fails = [sub for sub in self.subcases if not sub.is_passed()]
            passed_cnt = total - len(fails)
        else:
            total = 1
            passed_cnt = 1 if self.passed else 0
            fails =[] if self.passed else [self]
        return total, passed_cnt,fails

    def write_doc(self, doc_engine, group=False):
        if len(self.subcases) > 0:
            doc_engine.start_group(self.name)
            for case in self.subcases:
                case.write_doc(doc_engine)
            doc_engine.end_group(self.name)
        else:
            if group:
                doc_engine.start_group(self.name)
            else:
                doc_engine.start_test(self.name)
            for body in self.bodys:
                doc_engine.add_tag_msg(*body)
            for error in self.errors:
                doc_engine.add_tag_msg(*error)
            if group:
                doc_engine.end_group(self.name)
            else:
                doc_engine.end_test(self.name)

    def get_fail_msg(self):
        return self.errors[0][1]

    def write_fail_table(self, table):
        row_cells = table.add_row().cells
        row_cells[0].text = self.name
        row_cells[1].text = self.get_fail_msg()

    def write_summary_table(self, table):
        row_cells = table.add_row().cells
        row_cells[0].text = self.name
        row_cells[1].text = ""
        if self.is_passed():
            row_cells[2].text = "通过"
        else:
            row_cells[2].text = "失败"
        for case in self.subcases:
            row_cells = table.add_row().cells
            row_cells[0].text = self.name
            row_cells[1].text = case.name
            if case.is_passed():
                row_cells[2].text = "通过"
            else:
                row_cells[2].text = "失败"


class TestEngine(object):
    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = TestEngine()
        return cls._instance

    def __init__(self):
        self.doc_engine = DocxEngine()
        self.roles = []
        self.current_group = None
        self.current_test = None
        self.test_infos = []
        self.test_name = None

    def config_test_program_name(self, name):
        self.test_name = name

    def create_role(self, name):
        role = Role(name)
        self.roles.append(role)
        return role

    def group_begin(self, name):
        logging.info("start test group %s", name)
        self.current_group = TestCaseInfo(name)
        self.test_infos.append(self.current_group)
        self.current_test = self.current_group

    def group_end(self, name):
        self.current_group = None

    def test_begin(self, name):
        logging.info("start test case %s", name)
        self.current_test = self.current_group.add_sub_case(name)

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
        self.doc_engine.write_detail()
        for case in self.test_infos:
            case.write_doc(self.doc_engine, True)
        self.doc_engine.save_doc()


def config_test_program_name(name):
    TestEngine.instance().config_test_program_name(name)


class Role(object):
    def __init__(self, name, media="SerialMedia", protocol="Smart7eProtocol"):
        self.name = name
        self.src = None
        self.dst = None
        self.media = Media.create_sub_class(media)
        self.protocol = Protocol.create_sub_class(protocol)
        self.session = SessionSuit.create_binary_suit(self.media, self.protocol)
        self.session.data_snd.connect(self.log_snd_frame)
        self.session.data_ready.connect(self.handle_rcv_msg)
        self.timer = QTimer()
        self.timer.timeout.connect(self.timeout_handle)
        self.waiting = False
        self.validate = None

    def timeout_handle(self):
        self.waiting = False
        self.timer.stop()
        TestEngine.instance().add_fail_test(self.name, "fail", "no return")

    def config_com(self, **kwargs):
        self.media.config(**kwargs)

    def config_address(self, src, dst):
        self.src = src
        self.dst = dst
        fbd = LocalFBD(DIDLocal.SET_APPLICATION_ADDR, self.src)
        data = Smart7EData(0, 0, fbd)
        self.session.write(data)
        self.expect_local_message([DIDLocal.ACTION_OK, DIDLocal.ACTION_FAIL], timeout=2)

    def send_1_did(self, cmd, did, value=bytes(), **kwargs):
        fbd = RemoteFBD.create(cmd, did, value)
        data = Smart7EData(self.src, self.dst, fbd)
        self.session.write(data)

    def expect_1_did(self, cmd, did, value=None, timeout=2, **kwargs):
        self.waiting = True
        self.timer.start(timeout*1000)
        cmd = CMD.to_enum(cmd)
        did_cls = DIDRemote.find_class_by_name(did)
        if isinstance(value, str):
            value = did_cls.encode_string(value)
        self.validate = SmartOneDidValidator(src=self.dst, dst= self.src, cmd=cmd, did=did_cls.DID, value=value)
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


def create_role(name):
    return TestEngine.instance().create_role(name)


def add_fail_test(tag, msg):
    TestEngine.add_fail_test(msg)


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


def run_all_tests(funcs):
    inits =[]
    tests = []
    for key,value in funcs.items():
        if key.endswith("init"):
            inits.append(value)
        if key.endswith("test"):
            tests.append(value)
    def run_func(funcs):
        for value in funcs:
            try:
                names = value.__doc__.split(".")
                if len(names) >= 2:
                    if len(names[0]) >= 2:
                        TestEngine.instance().group_begin(names[0])
                    TestEngine.instance().test_begin(names[1])
                else:
                    TestEngine.instance().group_begin(names[0])
                value()
            except Exception as e:
                msg = e.__traceback__.tb_frame.f_globals["__file__"]
                msg += "  linenumber:{0}".format(e.__traceback__.tb_lineno)
                TestEngine.instance().add_fail_test("程序运行异常", msg)
    run_func(inits)
    run_func(tests)
    generate_test_report()
    total, passed, fails = TestEngine.instance().summary()
    if total == passed:
        logging.info("测试通过：totoal:%d  passed:%d", total, passed)
    else:
        logging.info("测试失败：totoal:%d  passed:%d", total, passed)
        for case in fails:
            logging.info("失败测试名称：%s 失败原因：%s",case.name, case.get_fail_msg())
    exit(0)

