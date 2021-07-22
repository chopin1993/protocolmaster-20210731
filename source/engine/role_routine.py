from tools.converter import *
import types
import weakref
from engine.validator import *
from .test_engine import TestEngine, log_snd_frame, log_rcv_frame, Routine, TestEquiment
import logging
from .spy_device import SpyDevice
import engine


class RoleRoutine(Routine):
    """
    主要用来处理单个did，上报和联动测试
    """

    def __init__(self, name, said, device: TestEquiment):
        super(RoleRoutine, self).__init__(name, device)
        self.said = said
        self.current_seq = None
        self.waiting_send_frames = []
        self.re_sending_status = False
        self.waiting_received_frames = []
        self.send_OK = False
        self.rcv_timer = QTimer()
        self.rcv_timer.timeout.connect(self.rcv_frame_in_buff)

    def rcv_frame_in_buff(self):
        if len(self.waiting_received_frames) > 0:
            data = self.waiting_received_frames.pop(0)
            logging.warning("处理发送过程中收到的信息")
            self.handle_rcv_msg(data)
        else:
            self.rcv_timer.stop()

    def send_did(self, cmd, did, value=None, taid=None, gids=None, gid_type="U16", reply=False, **kwargs):
        gid, taid = self.get_gid(taid, gids, gid_type)
        fbd = RemoteFBD.create(cmd, did, value, gids=gids, gid_type=gid_type, **kwargs)
        taid = self.device.get_taid(taid)
        data = Smart7EData(self.said, taid, fbd, reply=reply)
        self.write(data)
        return str(data)

    def send_FE02_did(self, cmd, did, value=None, taid=None, gids=None, gid_type="U16", reply=False, **kwargs):
        """

        :param cmd: 支持“READ”,"WRITE","REPORT","NOTIFY"(不可靠上报)
        :param did: 此处的did固定为FE02
        :param value: 可是数字,也可以是类似于“00 34 78”的字符串
        :param taid: 目标地址
        :param gids: 组地址列表，可以是组地址列表。
        :param gid_type: 组地址编码类型，支持"BIT1","U8","U16"
        :param reply: 序号自动取自上一帧，并将其最高位置1
        :param kwargs: 如果数据标识中有多个数据单元，可以使用key,value的方式赋值
        :return:
        """
        # 第一层7E
        gid, taid = self.get_gid(taid, gids, gid_type)
        taid = self.device.get_taid(taid)
        fbd = RemoteFBD.create(cmd, did, value, gids=gids, gid_type=gid_type, **kwargs)
        data = Smart7EData(self.said, taid, fbd, reply=reply)
        # 第二层7E，使用了第一层的str(data)
        fbd = RemoteFBD.create(cmd, "FE02", str(data), gids=gids, gid_type=gid_type, **kwargs)
        data = Smart7EData(self.said, taid, fbd, reply=reply)
        self.write(data)
        return data

    def get_gid(self, taid, gids, gid_type):
        gid = None
        if taid == 0xffffffff and gids is None:
            raise ValueError("taid is boardcast but gids is None")
        if gids is not None:
            gid = GID(gid_type, gids)
            taid = 0xffffffff
        return gid, taid

    def send_multi_dids(self, cmd, *args, taid=None, reply=False):
        dids = [DIDRemote.create_did(name=args[i + 2], value=args[i + 3], gids=args[i], gid_type=args[i + 1]) for i in
                range(0, len(args), 4)]
        fbd = RemoteFBD(cmd, dids)
        taid = self.device.get_taid(taid)
        data = Smart7EData(self.said, taid, fbd, reply=reply)
        self.write(data)

    def timeout_handle(self):
        if self.re_sending_status:
            self.timer.stop()
            return
        if isinstance(self.validate, SmartDataValidator):
            frames = SpyDevice.instance().get_snd_frames()[::-1]
            for frame in frames:
                if frame.taid == self.validate.taid:
                    engine.add_doc_info("****warnging***抄控器没有收到数据，使用监控器数据代替进行测试")
                    msg = "使用spy监控器数据代替进行抄控器数据"
                    TestEngine.instance().add_fix_rcv_operation(self.name, "doc", msg)
                    self.handle_rcv_msg(frame)
                    SpyDevice.instance().clear_send_frames()
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

    def get_expect_seq(self, cmd, check):
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

        seq = self.get_expect_seq(cmd, check_seq)
        taid = self.said
        if gids is not None:
            self.is_expect_boradcast = True
            did = [self._create_did_validtor(did, value, gids=gids, gid_type=gid_type, **kwargs)]
            seq = None
            taid = 0xffffffff
        else:
            did = [self._create_did_validtor(did, value, **kwargs)]
            self.is_expect_boradcast = False

        self.validate = SmartDataValidator(said=self.device.get_taid(said),
                                           taid=taid,
                                           cmd=cmd,
                                           dids=did,
                                           seq=seq,
                                           ack=ack)
        self.wait_event(timeout)

    # def expect_FE02_did(self, cmd, did, value=None, timeout=2, ack=False, said=None, gids=None, gid_type="U16",
    #                     check_seq=True, **kwargs):
    #     """
    #
    #     """
    #     # 解析外层报文，无对比验证
    #     cmd = CMD.to_enum(cmd)
    #
    #     seq = self.get_expect_seq(cmd, check_seq)
    #     taid = self.said
    #     if gids is not None:
    #         self.is_expect_boradcast = True
    #         # 第一层验证did=FE02
    #         did_fe02 = [self._create_did_validtor(did='FE02', value=value, gids=gids, gid_type=gid_type, **kwargs)]
    #         seq = None
    #         taid = 0xffffffff
    #
    #     else:
    #         did_fe02 = [self._create_did_validtor(did=did, value=value, **kwargs)]
    #         self.is_expect_boradcast = False
    #
    #     data_in_7e = SmartDataValidator(said=self.device.get_taid(said), taid=taid,
    #                                     cmd=cmd, dids=did_fe02, seq=seq, ack=ack)
    #     # self.wait_event(timeout)
    #
    #     # 解析内层报文，需要验证报文正确性
    #     cmd = CMD.to_enum(cmd)
    #
    #     seq = self.get_expect_seq(cmd, check_seq)
    #     taid = self.said
    #     if gids is not None:
    #         self.is_expect_boradcast = True
    #         did = [self._create_did_validtor(did, value=data_in_7e, gids=gids, gid_type=gid_type, **kwargs)]
    #         seq = None
    #         taid = 0xffffffff
    #     else:
    #         did = [self._create_did_validtor(did, value=data_in_7e, **kwargs)]
    #         self.is_expect_boradcast = False
    #
    #     # except值与接收数据对比
    #     self.validate = SmartDataValidator(said=self.device.get_taid(said), taid=taid,
    #                                        cmd=cmd, dids=did, seq=seq, ack=ack)
    #     self.wait_event(timeout)

    def wait_event(self, timeout):
        SpyDevice.instance().clear_send_frames()
        super(RoleRoutine, self).wait_event(timeout)
        # 发送过程不能重入
        if not self.re_sending_status:
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
                          check_seq=True
                          ):
        assert len(args) % 4 == 0
        cmd = CMD.to_enum(cmd)
        seq = self.get_expect_seq(cmd, check_seq)
        dids = []
        self.is_expect_boradcast = False
        taid = self.said
        for i in range(0, len(args), 4):
            if args[i] is not None:
                self.is_expect_boradcast = True
                seq = None
                taid = 0xffffffff
            did = self._create_did_validtor(did=args[i + 2],
                                            value=args[i + 3],
                                            gids=args[i],
                                            gid_type=args[i + 1])
            dids.append(did)
        said = self.device.get_taid(said)
        self.validate = SmartDataValidator(said=said,
                                           taid=taid,
                                           cmd=cmd,
                                           dids=dids,
                                           seq=seq,
                                           ack=ack)
        self.wait_event(timeout)

    def send_raw(self, fbd, taid=None, swb_spy=True):
        if isinstance(fbd, str):
            fbd = hexstr2bytes(fbd)
        taid = self.device.get_taid(taid)
        data = Smart7EData(self.said, taid, fbd)
        self.write(data, swb_spy=swb_spy)

    def expect_raw(self, fbd, said=None, timeout=2):
        fbd = BytesCompare(fbd)
        self.validate = SmartDataValidator(said=self.device.get_taid(said),
                                           taid=self.said,
                                           fbd=fbd)
        self.wait_event(timeout)

    def handle_rcv_msg(self, data):
        # 检查是否可以忽略上报报文
        if self.re_sending_status:
            if (data.seq & 0x7f) == (self.current_seq & 0x7f):
                logging.warning("监测器检测失败，载波接收成功，不再重试发送")
                self.send_OK = True
                self.timer.stop()
            else:
                logging.warning("监测器重发过程中收到plc消息，暂存，延时处理")
            self.waiting_received_frames.append(data)
            return

        # 保证报文的收发顺序
        if len(self.waiting_received_frames) > 0:
            self.waiting_received_frames.append(data)
            data = self.waiting_received_frames.pop(0)

        if data is not None and \
                data.fbd.cmd in [CMD.REPORT, CMD.NOTIFY] and \
                not TestEngine.instance().report_enable:
            log_rcv_frame(self.name + " report ignone" + "如果你想要检测上报，需要调用 engine.report_check_enable_all(True)", data)
            return

        # 手动组织回复报文
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

    def write(self, data, swb_spy=True):
        from .spy_device import SpyDevice
        log_snd_frame(self.name, data)
        self.current_seq = data.seq
        if SpyDevice.instance().probe_connected and \
                data.taid == self.device.get_taid() and \
                data.is_need_spy() and \
                swb_spy:
            self.re_sending_status = True
            self.send_OK = False

            def receive_frame(frame):
                if frame.said == data.said and frame.seq == data.seq:
                    self.timer.stop()
                    self.send_OK = True

            SpyDevice.instance().install_rcv_hook(receive_frame)
            self.device.write(data)
            snd_cnt = 0
            while snd_cnt <= 4:
                self.wait_event(2)
                if self.send_OK:
                    break
                else:
                    data.increase_seq()
                    self.current_seq = data.seq
                    TestEngine.instance().add_resend_operation("", "doc",
                                                               "probe not rcv messgae, resend {}".format(snd_cnt))
                    log_snd_frame(self.name, data)
                    self.device.write(data)
                    snd_cnt += 1
            SpyDevice.instance().install_rcv_hook(None)
            self.re_sending_status = False
            self.rcv_timer.start(50)
        else:
            self.device.write(data)
