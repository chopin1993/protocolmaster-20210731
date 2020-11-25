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
        self.current_seq = None

    def send_did(self, cmd, did, value=None, taid=None, gids=None, gid_type="U16", **kwargs):
        gid, taid = self.get_gid(taid, gids, gid_type)
        fbd = RemoteFBD.create(cmd, did, value,gids=gids, gid_type=gid_type, **kwargs)
        dst = self.device.get_dst_addr(taid)
        data = Smart7EData(self.src, dst, fbd)
        self.write(data)

    def get_gid(self, taid, gids, gid_type):
        gid = None
        if taid==0xffffffff and gids is None:
            raise ValueError("taid is boardcat but gids is None")
        if gids is not None:
            gid = GID(gid_type, gids)
            taid = 0xffffffff
        return gid,taid

    def send_multi_dids(self, cmd, *args, taid=None, gids=None, gid_type="U16"):
        dids = [DIDRemote.create_did(args[idx], args[idx + 1]) for idx, arg in enumerate(args) if idx % 2 == 0]
        gid,taid = self.get_gid(taid, gids, gid_type)
        fbd = RemoteFBD(cmd, dids, gid=gid)
        dst = self.device.get_dst_addr(taid)
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

    def get_expect_seq(self,cmd):
        if cmd in [CMD.WRITE, CMD.READ]:
            return self.current_seq
        else:
            return None

    def expect_did(self, cmd, did, value=None,
                   timeout=2, ack=False, said=None,
                   gids=None, gid_type="U16",
                   **kwargs):
        cmd = CMD.to_enum(cmd)
        did = [self._create_did_validtor(did, value, **kwargs)]
        seq = self.get_expect_seq(cmd)
        gid = None
        if gids is not None:
            self.is_expect_boradcast = True
            gid = GID(gid_type, gids)
            seq = None
        self.validate = SmartDataValidator(src=self.device.get_dst_addr(said),
                                           dst=self.src,
                                           cmd=cmd,
                                           dids=did,
                                           gid=gid,
                                           seq=seq,
                                           ack=ack)
        self.wait_event(timeout)

    def wait(self, seconds, allowed_message):
        self.validate = NoMessage(allowed_message)
        self.wait_event(seconds)

    def expect_multi_dids(self, cmd, *args,
                          said=None, timeout=2, ack=False,
                          gids=None, gid_type="U16"):
        cmd = CMD.to_enum(cmd)
        gid = None
        if gids is not None:
            self.is_expect_boradcast = True
            gid = GID(gid_type, gids)
        dids = [self._create_did_validtor(args[idx], args[idx + 1]) for idx, arg in enumerate(args) if idx % 2 == 0]
        dst = self.device.get_dst_addr(said)
        self.validate = SmartDataValidator(src=dst,
                                           dst=self.src,
                                           cmd=cmd,
                                           gid = gid,
                                           dids=dids,
                                           seq = self.get_expect_seq(cmd),
                                           ack=ack)
        self.wait_event(timeout)

    def send_raw(self, fbd, taid=None):
        if isinstance(fbd, str):
            fbd = hexstr2bytes(fbd)
        dst = self.device.get_dst_addr(taid)
        data = Smart7EData(self.src, dst, fbd)
        self.write(data)

    def expect_raw(self, fbd, said=None, timeout=2):
        fbd = BytesCompare(fbd)
        self.validate = SmartDataValidator(src=self.device.get_dst_addr(said),
                                           dst=self.src,
                                           fbd = fbd)
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
            self.is_expect_boradcast = False

    def ack_report_message(self, data):
        if data is None:
            return
        data = data.ack_message()
        self.write(data)

    def write(self,data):
        log_snd_frame(self.name, data)
        self.current_seq = data.seq
        self.device.write(data)
