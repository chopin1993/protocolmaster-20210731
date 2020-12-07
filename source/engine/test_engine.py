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
from user_exceptions import MeidaException
from protocol.monitor7e_protocol import *
from protocol.fifo_buffer import FifoBuffer

def get_current_time_str():
    cur = time.time()
    s, ms = int(cur),cur - int(cur)
    return time.strftime('%H:%M:%S', time.localtime(s))+":{0:0>3}".format(int(ms*1000))


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
        self.running = False
        self.report_enable = False
        self.fail_idx = 0
        self.fifo = FifoBuffer()
        self.output_doc_dir = None

    def get_all_role(self):
        return self.com_medias[0].roles

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
        device = TestEquiment(name)
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
        self.fail_idx += 1
        fail_idx = "erroridx-{:0>6d}".format(self.fail_idx)
        self.current_test.add_fail_test(role, tag, msg, fail_idx)
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
        self.doc_engine.save_doc(self.get_output_doc_dir())

    def get_valid_infos(self):
        valids = []
        for i, group in enumerate(self.all_infos):
            if group.is_enable() or i==0:
                valids.append(group)
        return valids

    def is_running(self):
        return self.running

    def run_single_case(self,case):
        return self.run_all_test([self.all_infos[0], case])

    def run_all_test(self, valids=None):
        self.running = True

        from tools.esloging import log_init
        log_init(TestEngine.instance().get_output_doc_dir())

        def run_test(case):
            func = case.func
            case.clear()
            try:
                func()
            except MeidaException as e:
                logging.exception(e)
                raise e
            except Exception as e:
                msg = "异常原因:{}\nfile:{} line:{}".format(str(e),
                                                         e.__traceback__.tb_frame.f_globals["__file__"],
                                                         e.__traceback__.tb_lineno)
                self.add_fail_test("engine", "exception", msg)
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
        self.running = False

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

    def get_output_doc_dir(self):
        time_str = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
        self.output_doc_dir = os.path.join(self.output_dir, "测试报告")
        if not os.path.exists(self.output_doc_dir):
            os.mkdir(self.output_doc_dir)
        self.output_doc_dir = os.path.join(self.output_dir, "测试报告",time_str)
        if not os.path.exists(self.output_doc_dir):
            os.mkdir(self.output_doc_dir)
        return self.output_doc_dir



def log_snd_frame(name, data, only_log=False):
    if not only_log:
        TestEngine.instance().add_normal_operation(name, "snd", str(data))
        TestEngine.instance().add_normal_operation(name, "annotation", data.to_readable_str())
    if name in ["被测设备","测试工装"]:
        logger = logging.getLogger(name)
    else:
        logger = logging.getLogger()
    logger.info("%s snd %s", name, str(data))
    logger.info("%s txt %s", name, data.to_readable_str())


def log_rcv_frame(name, data, only_log=False):
    if not only_log:
        TestEngine.instance().add_normal_operation(name, "rcv", str(data))
        TestEngine.instance().add_normal_operation(name, "annotation", data.to_readable_str())
    if name in ["被测设备","测试工装"]:
        logger = logging.getLogger(name)
    else:
        logger = logging.getLogger()
    logger.info("%s rcv %s",name, str(data))
    logger.info("%s txt %s",name, data.to_readable_str())


class Routine(object):

    def __init__(self, name, device):
        self.name = name
        self.device = weakref.proxy(device)
        self.validate = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.timeout_handle)
        self.validate = None
        self.name = name
        self.is_expect_boradcast = False

    def timeout_handle(self):
        self.handle_rcv_msg(None)

    def get_remaining_time(self):
        if self.timer.isActive():
            return max(1,self.timer.remainingTime()//1000)
        return 0

    def wait_event(self, timeout):
        self.timer.start(int(timeout*1000))
        total = self.get_remaining_time()
        while True:
            left = self.get_remaining_time()
            if total - left >= 10:
                total = left
                logging.info("left %ds", total)
            if left == 0:
                break
            QCoreApplication.instance().processEvents()

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



class TestEquiment(object):
    """
    串口相关的设备
    """
    def __init__(self, name, media="SerialMedia", protocol="Monitor7eProtocol"):
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
        self.legal_devices.add(TestEngine.instance().get_test_dev_addr())
        self.buffer = FifoBuffer()

    def config_com(self, **kwargs):
        setting = UARTSettingFbd(baudrate=kwargs['baudrate'], parity=Parity.无校验)
        data = Monitor7EData.create_uart_message(setting, UARTCmd.W_SETTING)
        ret = self.media.config(**kwargs)
        self.write(data)
        return ret

    def create_role(self, name, src):
        self.legal_devices.add(src)
        from .role_routine import RoleRoutine
        from .local_routine import LocalRoutine
        for role in self.roles:
            if isinstance(role, RoleRoutine):
                if role.src == src:
                    role.name = name
                    self.local_routine.send_local_msg("设置应用层地址", src)
                    self.local_routine.expect_local_msg(["确认", "否认"], timeout=2)
                    self.local_routine.send_local_msg("设置透传模式", 1)
                    self.local_routine.expect_local_msg("确认")
                    return role
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
        self.local_routine.expect_local_msg(["确认", "否认"], timeout=2000)
        self.local_routine.send_local_msg("设置透传模式", 1)
        self.local_routine.expect_local_msg("确认")
        return role

    def get_dst_addr(self, dst=None):
        if dst is None:
            return TestEngine.instance().get_test_dev_addr()
        else:
            return dst

    def write(self, data):
        if isinstance(data, Smart7EData):
            self.legal_devices.add(data.taid)
            data = Monitor7EData.create_uart_message(data, cmd=UARTCmd.W_DATA)
        log_snd_frame("测试工装", data, only_log=True)
        self.session.write(data)


    def handle_plc_msg(self, data):
        if data.is_local():
            self.local_routine.handle_rcv_msg(data)
            return

        if data.said not in self.legal_devices:
            #log_rcv_frame("ignore:", data, only_log=True)
            return

        if data.is_update():
            self.updater.handle_rcv_msg(data)
            return

        for role in self.roles:
            from .role_routine import RoleRoutine
            if isinstance(role, RoleRoutine):
                if data.taid == 0xffffffff:
                    if role.is_expect_boradcast:
                        role.handle_rcv_msg(data)
                else:
                    if data.taid == role.src:
                        role.handle_rcv_msg(data)

    def handle_rcv_msg(self, monitor_data):
        log_rcv_frame("测试工装", monitor_data, only_log=True)
        if monitor_data.is_uart_data():
           self.buffer.receive(monitor_data.data)
           buffer_data = self.buffer.peek(-1)
           protocol = Smart7eProtocol()
           decoder = BinaryDecoder()
           (found, start, length) = protocol.find_frame_in_buff(buffer_data)
           if found:
               self.buffer.read(start + length)
               frame_data = buffer_data[start:start + length]
               decoder.set_data(frame_data)
               monitor_data = protocol.decode(decoder)
               self.handle_plc_msg(monitor_data)
           else:
               if self.buffer.data_length() > 5000:
                   logging.warning("test engine buff too big %d, we will clear all buff", self.buffer.data_length())
                   self.buffer.read(self.buffer.read(self.buffer.data_length()))
        else:
           log_rcv_frame("测试工装", monitor_data, only_log=True)