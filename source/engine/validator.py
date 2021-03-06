from register import Register
from protocol.smart7e_protocol import *
from tools.converter import u16tohexstr


class Validator(Register):
    def __init__(self):
        self.ack = False
        pass

    def __call__(self, data):
        raise NotImplementedError


class NoMessage(Validator):
    def __init__(self, allowed_message=False, said=None):
        super(NoMessage, self).__init__()
        self.allowed_message = allowed_message
        self.said = said

    def __call__(self, data):
        if not self.allowed_message and data is not None:
            return False, "等待验证失败,收到异常报文"
        else:
            return True, "等待验证成功"

    def __str__(self):
        return "允许收到信息" if self.allowed_message else "不允许收到信息"


class SmartLocalValidator(Validator):

    def __init__(self, **kwargs):
        super(SmartLocalValidator, self).__init__()
        self.kwargs = kwargs
        self.said = 0
        self.cmd = self.kwargs['cmd']
        if not isinstance(self.cmd, list):
            self.cmd = [self.cmd]
        self.cmd = [LocalFBD.find_cmd(cmd).cmd for cmd in self.cmd]

    def __call__(self, data):
        if data is None:
            return False, "本地通信报文验证失败, 没有收到回复报文"
        is_local = data.is_local()
        if not is_local:
            return False, error_msg("address", "local", "non local")

        fbd = data.fbd
        cmd = fbd.cmd

        if isinstance(self.cmd, list):
            cmd_valid = cmd in self.cmd
        else:
            cmd_valid = (cmd == fbd.cmd)

        if not cmd_valid:
            return False, error_msg("cmd", self.cmd, fbd.cmd)

        return True, "本地报文验证成功"


class BytesCompare(Validator):
    def __init__(self, placeholder):
        self.placeholder = placeholder

    def __call__(self, data):
        if len(self.placeholder) == 0 and len(data) == 0:
            return True
        place_holders = self.placeholder.split(" ")
        place_holders = [x.strip() for x in place_holders]
        place_holders = [x for x in place_holders if len(x) > 0]

        if len(place_holders) != len(data):
            return False
        for i, holder in enumerate(place_holders):
            if "*" in holder:
                continue
            value = int(holder, base=16)
            if value != data[i]:
                return False
        return True

    def __str__(self):
        return self.placeholder


class FunctionCompare(Validator):
    def __init__(self, func):
        self.func = func

    def __call__(self, data):
        return self.func(data)


class UnitCompare(Validator):
    def __init__(self, **kwargs):
        self.kwarges = kwargs

    def __call__(self, data):
        for key, value in self.kwarges:
            pass
        return True


class DIDValidtor(Validator):
    def __init__(self,did, value, gid):
        self.did = did
        self.value = value
        self.gid = gid

    def __call__(self, did):
        def compare_data(expect_value,target_value):
            if isinstance(expect_value, Validator):
                return expect_value(did.data)
            else:
                return  expect_value == target_value
        if self.did != did.DID:
            return False
        if self.gid != did.gid:
            return False

        if did.DID == 0xfe02:
            protocol = Smart7eProtocol()
            decoder = BinaryDecoder()
            decoder.set_data(did.data)
            sub7e_data = protocol.decode(decoder)
            for i in range(len(self.value)):
                didx = self.value[i].did
                valuex = self.value[i].value
                if didx != sub7e_data.fbd.didunits[i].DID:
                    return False
                if isinstance(valuex,bytes):
                    return valuex == sub7e_data.fbd.didunits[i].data
                return valuex(sub7e_data.fbd.didunits[i].data)
        else:
            return  compare_data(self.value, did.data)

    def __str__(self):
        return "gid:{gid} did[{did}] value:{value}".format(gid=self.gid, did=u16tohexstr(self.did) , value=self.value)


def error_msg(filed, expected, rcv):
    return f"{filed} mismatch, expect:{expected} rcv:{rcv}".format(filed=filed, expected=expected, rcv=rcv)


class SmartDataValidator(Validator):
    """
    报文验证
    """
    def __init__(self, said, taid, cmd=None, dids=None, fbd=None, seq=None, ack=False):
        super(SmartDataValidator, self).__init__()
        self.cmd = cmd
        self.dids = dids
        self.said = said
        self.taid = taid
        self.ack = ack
        self.fbd = fbd
        self.seq = seq

    def __call__(self, smartData):
        if smartData is None:
            return False, "没有回复"

        if self.said != smartData.said:
            return False, error_msg("said", self.said, smartData.said)
        if self.taid != smartData.taid:
            return False, error_msg("taid", self.taid, smartData.taid)
        # if self.seq is not None and self.seq != (smartData.seq & 0x7f):
        #     return False, error_msg("seq", self.seq, smartData.seq)
        if self.fbd is None:

            if smartData.fbd.didunits[0].DID == 0xfe02:
                protocol = Smart7eProtocol()
                decoder = BinaryDecoder()
                decoder.set_data(smartData.fbd.didunits[0].data)
                sub7e_data = protocol.decode(decoder)
                if self.cmd != sub7e_data.fbd.cmd:
                    return False, error_msg("cmd", self.cmd, sub7e_data.fbd.cmd)
            else:
                if self.cmd != smartData.fbd.cmd:
                    return False, error_msg("cmd", self.cmd, smartData.fbd.cmd)



            for validator, did in zip(self.dids, smartData.fbd.didunits):
                if not validator(did):
                     return False, error_msg("did", str(validator), str(did))
        else:
            if self.fbd(smartData.fbd.data):
                return False, error_msg("fbd", self.fbd, smartData.fbd.data)
        return True, "报文验证成功"


class MonitorCrossZeroValidator(Validator):
    def __init__(self, channel, status):
        self.channel = channel
        self.status = status

    def __call__(self, monitordata):
        if self.channel != monitordata.group:
            return False, error_msg("group", self.channel, monitordata.group)
        elif self.status != monitordata.data[0]:
            return False, error_msg("status", self.status, monitordata.data[0])
        else:
            return True, "过零检测 channel:{} status:{} 验证成功".format(self.channel, self.status)
