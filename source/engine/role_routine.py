from tools.converter import *
import types
import weakref
from engine.validator import *
from .test_engine import TestEngine,log_snd_frame,log_rcv_frame,Routine,TestEquiment
import logging
from .spy_device import SpyDevice
import engine

class RoleRoutine(Routine):
    """
    主要远程用来处理单个did，上报和联动测试
    """
    def __init__(self, name, said, device:TestEquiment):
        super(RoleRoutine, self).__init__(name, device)
        self.said = said
        self.current_seq = None
        self.waiting_send_frames = []

    def send_did(self, cmd, did, value=None, taid=None, gids=None, gid_type="U16", reply=False, **kwargs):
        gid, taid = self.get_gid(taid, gids, gid_type)
        fbd = RemoteFBD.create(cmd, did, value,gids=gids, gid_type=gid_type, **kwargs)
        taid = self.device.get_taid(taid)
        data = Smart7EData(self.said, taid, fbd, reply=reply)
        self.write(data)

    def get_gid(self, taid, gids, gid_type):
        gid = None
        if taid==0xffffffff and gids is None:
            raise ValueError("taid is boardcast but gids is None")
        if gids is not None:
            gid = GID(gid_type, gids)
            taid = 0xffffffff
        return gid,taid

    def send_multi_dids(self, cmd, *args, taid=None, reply=False):
        dids = [DIDRemote.create_did(name=args[i+2], value=args[i+3], gids=args[i],gid_type=args[i+1]) for i in range(0, len(args), 4)]
        fbd = RemoteFBD(cmd, dids)
        taid = self.device.get_taid(taid)
        data = Smart7EData(self.said, taid, fbd, reply=reply)
        self.write(data)

    def timeout_handle(self):
        if isinstance(self.validate, SmartDataValidator):
            frames = SpyDevice.instance().get_snd_frames()[::-1]
            for frame in frames:
                if frame.taid == self.validate.taid:
                    engine.add_doc_info("****warnging***抄控器没有收到数据，使用监控器数据代替进行测试")
                    msg = "使用spy监控器数据代替进行抄控器数据"
                    TestEngine.instance().add_fix_rcv_operation(self.name,"doc", msg)
                    self.handle_rcv_msg(frame)
                    return
        self.handle_rcv_msg(None)

    def _create_did_validtor(self, did, value, gids=None, gid_type=None, **kwargs):
        did_cls = DIDRemote.find_class_by_name(did)
        gid = None
        if gids is not None:
            gid = GID(gid_type, gids)
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
        return DIDValidtor(did_cls.DID, value, gid)

    def get_expect_seq(self,cmd, check):
        if cmd in [CMD.WRITE, CMD.READ] and check:
            return self.current_seq
        else:
            return None

    def expect_did(self, cmd, did, value=None,
                   timeout=2, ack=False, said=None,
                   gids=None, gid_type="U16",
                   check_seq=True,
                   **kwargs):
        cmd = CMD.to_enum(cmd)
        did = [self._create_did_validtor(did, value, **kwargs)]
        seq = self.get_expect_seq(cmd, check_seq)
        gid = None
        if gids is not None:
            self.is_expect_boradcast = True
            gid = GID(gid_type, gids)
            seq = None
        self.validate = SmartDataValidator(said=self.device.get_taid(said),
                                           taid=self.said,
                                           cmd=cmd,
                                           dids=did,
                                           gid=gid,
                                           seq=seq,
                                           ack=ack)
        self.wait_event(timeout)

    def wait_event(self, timeout):
        SpyDevice.instance().clear_send_frames()
        super(RoleRoutine, self).wait_event(timeout)
        for frame in self.waiting_send_frames:
            self.write(frame)
        self.waiting_send_frames = []

    def wait(self, seconds, allowed_message, said=None):
        if allowed_message:
            self.validate = None
        else:
            self.validate = NoMessage(allowed_message, said=self.device.get_taid(said))
        self.wait_event(seconds)

    def expect_multi_dids(self, cmd, *args,
                          said=None, timeout=2, ack=False,
                          gids=None, gid_type="U16",
                          check_seq=True
                          ):
        assert len(args)%4 == 0
        cmd = CMD.to_enum(cmd)
        seq = self.get_expect_seq(cmd, check_seq)
        gid = None
        if gids is not None:
            self.is_expect_boradcast = True
            gid = GID(gid_type, gids)
        dids = []
        for i in range(0, len(args), 4):
            did = self._create_did_validtor(did=args[i+2],
                                            value=args[i+3],
                                            gids=args[i],
                                            gid_type=args[i+1])
            dids.append(did)
        taid = self.device.get_taid(said)
        self.validate = SmartDataValidator(said=taid,
                                           taid=self.said,
                                           cmd=cmd,
                                           gid=gid,
                                           dids=dids,
                                           seq=seq,
                                           ack=ack)
        self.wait_event(timeout)

    def send_raw(self, fbd, taid=None):
        if isinstance(fbd, str):
            fbd = hexstr2bytes(fbd)
        taid = self.device.get_taid(taid)
        data = Smart7EData(self.said, taid, fbd)
        self.write(data)

    def expect_raw(self, fbd, said=None, timeout=2):
        fbd = BytesCompare(fbd)
        self.validate = SmartDataValidator(said=self.device.get_taid(said),
                                           taid=self.said,
                                           fbd = fbd)
        self.wait_event(timeout)

    def handle_rcv_msg(self, data):
        #检查是否可以忽略上报报文
        if data is not None and \
                data.fbd.cmd in [CMD.REPORT, CMD.NOTIFY] and \
                not TestEngine.instance().report_enable:
            log_rcv_frame(self.name+" report ignone" +"如果你想要检测上报，需要调用 engine.report_check_enable_all(True)", data)
            return

        if isinstance(data, Smart7EData):
            Smart7EData.LAST_FRAME_SEQ = data.seq

        if self.validate is not None:
            if data is not None:
                if data.said != self.validate.said:
                    log_rcv_frame("said mismatch ignore " + self.name, data)
                    return
                else:
                    log_rcv_frame(self.name, data)
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
        else:
            if data is None:
                self.timer.stop()
                self.validate = None
                self.is_expect_boradcast = False
            else:
                log_rcv_frame("no validator ignore " + self.name, data)

    def ack_report_message(self, data):
        if data is None:
            return
        data = data.ack_message()
        self.waiting_send_frames.append(data)

    def write(self,data):
        log_snd_frame(self.name, data)
        self.current_seq = data.seq
        self.device.write(data)
