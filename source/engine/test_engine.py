from engine.docx_engine import DocxEngine
from media import Media
from session import SessionSuit
from engine.test_case import TestCaseInfo
import json
import logging
import os
from PyQt5.QtCore import QTimer,QCoreApplication
import time
from engine.validator import *
import weakref


def get_current_time_str():
    return time.strftime('%H:%M:%S', time.localtime(time.time()))


class TestEngine(object):
    """
    1. 统计测试信息
    2. 运行测试
    3. 生成测试报告
    """
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
        self.config = None

    def get_default_role(self):
        return self.com_medias[0].default_role

    def get_updater(self):
        return self.com_medias[0].updater

    def get_local_routine(self):
        return self.com_medias[0].local_routine

    def get_default_device(self):
        return self.com_medias[0]

    def config_test_program_name(self, name):
        self.test_name = name

    def get_test_dev_addr(self):
        return self.config["测试设备地址"]

    def create_com_device(self, name):
        device = Device(name)
        self.com_medias.append(device)
        return device

    def group_begin(self, name, func, brief=None):
        #logging.info("start test group %s", name)
        self.current_group = TestCaseInfo(name,func,brief)
        self.all_infos.append(self.current_group)
        self.current_test = self.current_group

    def group_end(self, name):
        self.current_group = None

    def test_begin(self, name, func, brief):
        #logging.info("start test case %s", name)
        self.current_test = self.current_group.add_sub_case(name,func, brief)

    def test_end(self, name):
        self.current_test = None

    def add_fail_test(self, role, tag, msg):
        self.current_test.add_fail_test(role, tag, msg, get_current_time_str())
        logging.info("case %s fail, %s %s ", self.current_test.name, tag, msg)

    def add_normal_operation(self,role, tag, msg):
        self.current_test.add_normal_operation(role, tag, msg, get_current_time_str())

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


def log_snd_frame(name, data, only_log=False):
    if not only_log:
        TestEngine.instance().add_normal_operation(name, "snd", str(data))
        TestEngine.instance().add_normal_operation(name, "annotation", data.to_readable_str())
    logging.info("snd %s", str(data))
    logging.info("txt %s", data.to_readable_str())


def log_rcv_frame(name, data, only_log=False):
    if not only_log:
        TestEngine.instance().add_normal_operation(name, "rcv", str(data))
        TestEngine.instance().add_normal_operation(name, "annotation", data.to_readable_str())
    logging.info("rcv %s", str(data))
    logging.info("txt %s", data.to_readable_str())


class Routine(object):

    def __init__(self, name, device):
        self.name = name
        self.device = weakref.proxy(device)
        self.validate = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.timeout_handle)
        self.validate = None
        self.name = name

    def timeout_handle(self):
        self.handle_rcv_msg(None)

    def get_remaining_time(self):
        if self.timer.isActive():
            return max(1,self.timer.remainingTime()//1000)
        return 0

    def wait_event(self, timeout):
        self.timer.start(timeout*1000)
        self.device.wait_event()

    def handle_rcv_msg(self, msg):
        if msg is not None:
            log_rcv_frame(self.name,msg)
        if self.validate is not None:
            valid, msg = self.validate(msg)
            if valid:
                TestEngine.instance().add_normal_operation(self.name, "expect success", msg)
            else:
                TestEngine.instance().add_fail_test(self.name, "expect fail", msg)
            self.timer.stop()



class Device(object):
    """
    串口相关的设备
    """
    def __init__(self, name, media="SerialMedia", protocol="Smart7eProtocol"):
        self.name = name
        self.media = Media.create_sub_class(media)
        self.protocol = Protocol.create_sub_class(protocol)
        self.session = SessionSuit.create_binary_suit(self.media, self.protocol)
        self.session.data_ready.connect(self.handle_rcv_msg)
        self.roles = []
        self.default_role = None
        self.updater = None
        self.local_routine = None
        self.legal_devices = set()

    def config_com(self, **kwargs):
        self.media.config(**kwargs)

    def create_role(self, name, src):
        from .role_routine import RoleRoutine
        from .local_routine import LocalRoutine
        role = RoleRoutine(name, src, self)
        self.roles.append(role)
        if self.default_role is None:
            self.default_role = role
            from engine.updater import UpdateRoutine
            self.updater = UpdateRoutine("updater", src, self)
            self.local_routine = LocalRoutine("local", self)
            self.roles.append(self.local_routine)
            self.roles.append(self.updater)
        self.local_routine.send_local_msg("设置应用层地址", src)
        self.local_routine.expect_local_msg(["确认", "否认"], timeout=2)
        return role

    def get_dst_addr(self, dst=None):
        if dst is None:
            return TestEngine.instance().get_test_dev_addr()
        else:
            return dst

    def get_waiting_time(self):
        left_time = 0
        cnt = 0
        for role in self.roles:
            remaining = role.get_remaining_time()
            if remaining > 0:
                cnt += 1
                left_time = max(remaining, left_time)
        return left_time, cnt

    def wait_event(self):
        current,cnt = self.get_waiting_time()
        if cnt > 1:
            return
        while True:
            time,cnt = self.get_waiting_time()
            if current - time >= 10:
                current = time
                logging.info("left %ds", current)
            if time == 0:
                break
            QCoreApplication.instance().processEvents()

    def write(self, data):
        self.legal_devices.add(data.taid)
        self.session.write(data)

    def handle_rcv_msg(self, data):

        if data.is_local():
            self.local_routine.handle_rcv_msg(data)
            return

        if data.said not in self.legal_devices:
            log_rcv_frame(self.name, data, only_log=True)
            return

        if data.is_update():
            self.updater.handle_rcv_msg(data)
            return

        for role in self.roles:
            from .role_routine import RoleRoutine
            if isinstance(role, RoleRoutine):
                if data.taid == role.src:
                    role.handle_rcv_msg(data)