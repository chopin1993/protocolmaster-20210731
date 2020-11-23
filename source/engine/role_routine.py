from tools.converter import *
import types
import weakref
from engine.validator import *
from .test_engine import TestEngine,Device,log_snd_frame,log_rcv_frame,Routine
import logging


class RoleRoutine(Routine):
    """
    主要用来处理单个did，上报和联动测试
    """
    def __init__(self, name, src, device:Device):
        super(RoleRoutine, self).__init__(name, device)
        self.src = src

    def send_did(self, cmd, did, value=None, dst=None,**kwargs):
        fbd = RemoteFBD.create(cmd, did, value, **kwargs)
        dst = self.device.get_dst_addr(dst)
        data = Smart7EData(self.src, dst, fbd)
        self.write(data)

    def send_multi_dids(self, cmd, *args, dst=None):
        dids = [DIDRemote.create_did(args[idx], args[idx + 1]) for idx, arg in enumerate(args) if idx % 2 == 0]
        fbd = RemoteFBD(cmd, dids)
        dst = self.device.get_dst_addr(dst)
        data = Smart7EData(self.src, dst, fbd)
        self.write(data)

    def _create_did_validtor(self, did, value, **kwargs):
        did_cls = DIDRemote.find_class_by_name(did)
        if did_cls is None:
            logging.error("%s cant not search in excel", did)
            raise NotImplementedError
        if isinstance(value, str):
            if did_cls.is_value_string(value):
                value = did_cls.encode_reply(value)
            else:
                value = BytesCompare(value)
        elif isinstance(value, types.FunctionType):
            value = FunctionCompare(value)
        elif isinstance(value, Validator):
            pass
        elif value is None and len(kwargs) > 0:
            value = did_cls.encode_reply(**kwargs)
        elif value is not None:
            value = did_cls.encode_reply(value)
        else:
            raise ValueError("cant not encode value for did {0}".format(did))
        return DIDValidtor(did_cls.DID, value)

    def expect_did(self, cmd, did, value=None, timeout=2, ack=False, **kwargs):
        cmd = CMD.to_enum(cmd)
        did = [self._create_did_validtor(did, value, **kwargs)]
        self.validate = SmartDataValidator(src=self.device.get_dst_addr(),
                                           dst=self.src,
                                           cmd=cmd,
                                           dids=did,
                                           ack=ack)
        self.wait_event(timeout)

    def wait(self, seconds, allowed_message):
        self.validate = NoMessage(allowed_message)
        self.wait_event(seconds)

    def expect_multi_dids(self, cmd, *args, dst=None, timeout=2, ack=False):
        cmd = CMD.to_enum(cmd)
        dids = [self._create_did_validtor(args[idx], args[idx + 1]) for idx, arg in enumerate(args) if idx % 2 == 0]
        dst = self.device.get_dst_addr(dst)
        self.validate = SmartDataValidator(src=dst,
                                           dst=self.src,
                                           cmd=cmd,
                                           dids=dids,
                                           ack=ack)
        self.wait_event(timeout)

    def handle_rcv_msg(self, data):
        if data is not None:
            log_rcv_frame(self.name, data)
        if data is not None and data.fbd.cmd == CMD.UPDATE:
            return
        if self.validate is not None:
            valid, msg = self.validate(data)
            if valid:
                TestEngine.instance().add_normal_operation(self.name, "expect success", msg)
            else:
                TestEngine.instance().add_fail_test(self.name, "expect fail", msg)
            if self.validate.ack:
                self.ack_report_message(data)
            self.timer.stop()
            self.validate = None

    def ack_report_message(self, data):
        if data is None:
            return
        data = data.ack_message()
        self.write(data)

    def write(self,data):
        log_snd_frame(self.name, data)
        self.device.write(data)
