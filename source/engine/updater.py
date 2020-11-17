from .test_engine import TestEngine,Device,log_snd_frame,log_rcv_frame
from .interface import *
import os
from protocol.codec import BinaryDecoder
import re
import weakref

def parse_file(data):
    decoder = BinaryDecoder(data)
    outputs = {}
    for i in range(4):
        value = decoder.decode_cstr()
        key = re.findall(r"([\w\s]*):", value)[0]
        value = re.findall(r":([\w\-().]*)", value)[0]
        outputs[key] = value

    start = decoder.decode_bytes(14)
    program = decoder.decode_left_bytes()
    crc = int(outputs['file crc'], base=16)
    size = int(outputs['size'], base=16)
    return outputs['device type'], outputs['soft ver'], crc, size, program



class UpdateRoutine(object):
    """
    主要用来处理升级事务
    """
    def __init__(self, name, src, device):
        self.name = name
        self.src = src
        self.device = weakref.proxy(device)
        self.name = name
        self.file_name = None
        self.device_type = None
        self.soft_version = None
        self.crc = None
        self.size = None
        self.data = None
        self.send_idx = 0

    def update(self, file_name, control_func=None, expect_seqs=None):
        pass
        # self.file_name = file_name
        # if not os.path.exists(file_name):
        #     TestEngine.instance().add_fail_test(self.name,"fail", self.file_name + " 不存在")
        #     return
        # with open(self.file_name, "rb") as handle:
        #     self.data = handle.read()
        #     self.device_type, self.soft_version, self.crc, self.size, self.data = parse_file(self.data)
        #
        # msg = "{0} {1} {2} {4} start update".format(self.soft_version, self.device_type, self.crc, self.size)
        # add_doc_info(msg)
        # self.send_idx = 0
        # self.send_update_package(self.send_idx)
        # self.device.waiting_event(3, self.handle_rcv_msg)

    def send_update_package(self, idx):
        pass
        # self.device.write()

    def handle_rcv_msg(self, data):
        print(str(data))
        # if data is not None:
        #     log_rcv_frame(self.name, data)
        #
        # if self.validate is not None:
        #     valid, msg = self.validate(data)
        #     if valid:
        #         TestEngine.instance().add_normal_operation(self.name, "expect success", msg)
        #     else:
        #         TestEngine.instance().add_fail_test(self.name, "expect fail", msg)
        #     if self.validate.ack:
        #         self.ack_report_message(data)
