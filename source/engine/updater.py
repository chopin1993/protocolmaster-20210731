from .test_engine import TestEngine,TestEquiment,log_snd_frame,log_rcv_frame
from .interface import *
import os
from protocol.codec import BinaryDecoder,BinaryEncoder
import re
import weakref
from tools.converter import hexstr2bytes
from protocol.smart7e_protocol import UpdateStartInfo,UpdateFBD,CMD,Smart7EData
from PyQt5.QtCore import QTimer


class UpdaterFileParser(object):
    def __init__(self,cmd, file_name):
        self.device_type = None
        self.soft_version = None
        self.crc = None
        self.size = None
        self.data = None
        self.file_name = file_name
        self.cmd = cmd

        with open(self.file_name, "rb") as handle:
            self.data = handle.read()
            self.device_type, self.soft_version, self.crc, self.size, self.data = self.parse_file(self.data)

    def get_package(self, idx, block_size):
        if idx == 0:
            info = UpdateStartInfo(size=self.size,
                                   crc=self.crc,
                                   blocksize=block_size,
                                   devicetype=self.device_type,
                                   softversion=self.soft_version)
            data = BinaryEncoder.object2data(info)
        else:
            data_idx = idx-1
            data = self.data[data_idx*block_size:block_size*(data_idx+1)]
        fbd = UpdateFBD(cmd=self.cmd, seq=idx,ack=True,crc=self.crc, data=data)
        return fbd

    def parse_file(self,data):
        decoder = BinaryDecoder(data)
        outputs = {}
        for i in range(4):
            value = decoder.decode_cstr()
            key = re.findall(r"([\w\s]*):", value)[0]
            value = re.findall(r":([\w\-().]*)", value)[0]
            outputs[key] = value

        start = decoder.decode_bytes(14)
        program = decoder.decode_left_bytes()
        crc = hexstr2bytes(outputs['file crc'])
        size = int(outputs['file size'], base=16)
        return hexstr2bytes(outputs['device type']), outputs['soft ver'], crc, size, program


def _default_control_func(seq):
    return seq

from .test_engine import Routine

class UpdateRoutine(Routine):
    """
    主要用来处理升级事务
    """
    UPDATEING=0
    SUSPEND=1
    STOP=2
    def __init__(self, name, src, device):
        super(UpdateRoutine, self).__init__(name, device)
        self.src = src
        self.file_name = None
        self.send_idx = 0
        self.block_size = 128
        self.parser= None
        self.update_func = None
        self.status = self.STOP
        self.resend = 0
        self.snd_seqs = []
        self.rcv_seqs = []

    def timeout_handle(self):
        self.handle_rcv_msg(None)

    def update(self, cmd, file_name, block_size=128, update_func=None, control_func=None):
        self.snd_seqs = []
        self.rcv_seqs = []
        self.file_name = file_name
        self.block_size = block_size
        self.update_func = _default_control_func if update_func is None else update_func
        self.control_func = control_func
        if not os.path.exists(file_name):
            TestEngine.instance().add_fail_test(self.name, "fail", self.file_name + " 不存在")
            return
        self.parser = UpdaterFileParser(cmd, self.file_name)
        self.send_idx = 0
        self.send_update_package(self.send_idx)
        self.status = self.UPDATEING
        self.wait_event(4)
        add_doc_info("snd seq:" + str(self.snd_seqs))
        add_doc_info("rcv seq:" + str(self.rcv_seqs))
        return self.rcv_seqs

    def wait_event(self, timeout):
        self.timer.start(int(timeout * 1000))
        tick = time.time()
        last = 0
        while self.get_remaining_time() > 0:
            QCoreApplication.instance().processEvents()
            if self.control_func is not None:
                current = int(time.time() - tick)
                if last != current:
                    last = current
                    self.status = self.SUSPEND
                    self.control_func(current)
                    self.status= self.UPDATEING

    def get_remaining_time(self):
        remaining = super(UpdateRoutine, self).get_remaining_time()
        if self.status!=self.STOP or remaining>0:
            return max(remaining, 1)
        else:
            return 0

    def send_update_package(self, idx):
        self.send_idx = idx
        self.snd_seqs.append(idx)
        fbd = self.parser.get_package(idx, self.block_size)
        dst = self.device.get_dst_addr(None)
        data = Smart7EData(self.src, dst, fbd)
        logging.info("update snd %s", str(data))
        logging.info("update txt %s", data.to_readable_str())
        self.device.write(data)

    def handle_rcv_msg(self, data):
        if data is not None:
            logging.info("update rcv %s", str(data))
            logging.info("update txt %s", data.to_readable_str())

        if self.status == self.STOP:
            return
        elif self.status == self.SUSPEND:
            self.timer.start(4000)
        else:
            if data is None:
                if self.resend < 10:
                    add_doc_info("resend package {0}  次数 {1}".format(self.send_idx, self.resend))
                    self.resend += 1
                    self.send_update_package(self.send_idx)
                    self.timer.start(4000)
                    return
                else:
                    add_fail_test("没有回复")
                    self.status = self.STOP
                    self.timer.stop()
                return
            else:
                self.resend = 0
                self.rcv_seqs.append(data.fbd.seq)
                seq = self.update_func(data.fbd.seq)
                if seq is not None and seq != 0xffff:
                    self.send_update_package(seq)
                    self.timer.start(4000)
                else:
                    if seq == 0xffff:
                        add_doc_info("升级成功")
                    else:
                        add_doc_info("手动停止升级")
                    self.status = self.STOP
                    self.timer.stop()
