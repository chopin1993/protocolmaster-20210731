from register import Register
from protocol.smart7e_protocol import *

class Validator(Register):
    def __init__(self):
        self.ack = False
        pass

    def __call__(self, data):
        raise NotImplementedError


class NoMessage(Validator):
    def __init__(self,allowed_message=False):
        super(NoMessage, self).__init__()
        self.allowed_message = allowed_message

    def __call__(self, data):
        if not self.allowed_message and data is not None:
            return False, "验证失败,等待是收到异常报文"
        else:
            return True, "验证成功"



class SmartLocalValidator(Validator):

    def __init__(self, **kwargs):
        super(SmartLocalValidator, self).__init__()
        self.kwargs = kwargs
        self.cmd = self.kwargs['cmd']
        if not isinstance(self.cmd, list):
            self.cmd = [self.cmd]
        self.cmd =[LocalFBD.find_cmd(cmd).cmd for cmd in self.cmd]

    def __call__(self, data):
        if data is None:
            return False, "验证失败, 没有收到回复报文"
        is_local = data.is_local()
        fbd = data.fbd
        cmd = fbd.cmd
        if isinstance(self.cmd , list):
            cmd_valid = cmd in self.cmd
        else:
            cmd_valid = (cmd == fbd.cmd)
        if is_local and cmd_valid:
            return True, "验证成功"
        else:
            return False, "验证失败"

class BytesCompare(Validator):
    def __init__(self, placeholder):
        self.placeholder = placeholder

    def __call__(self, data):
        if len(self.placeholder) == 0 and len(data) == 0:
            return True
        place_holders = self.placeholder.split(" ")
        if len(place_holders) != len(data):
            return False
        for i,holder in enumerate(place_holders):
            if "*" in holder:
                continue
            value = int(holder, base=16)
            if value != data[i]:
                return False
        return True


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
    def __init__(self,did, value):
        self.did = did
        self.value = value

    def __call__(self, did):
        def compare_data(expect_value,target_value):
            if isinstance(expect_value, Validator):
                return expect_value(did.data)
            else:
                return  expect_value == target_value
        if self.did != did.DID:
            return False
        return  compare_data(self.value, did.data)


class SmartDataValidator(Validator):
    def __init__(self, src, dst, cmd, dids, ack=False):
        super(SmartDataValidator, self).__init__()
        self.cmd = cmd
        self.dids = dids
        self.src = src
        self.dst = dst
        self.ack = ack

    def __call__(self, smartData):
        if smartData is None:
            return False, "没有回复"
        if  self.cmd != smartData.fbd.cmd or \
            self.src != smartData.said or \
            self.dst != smartData.taid or \
            self.cmd != smartData.fbd.cmd:
            return False, "验证失败,cmd src dst  not match"

        for validator, did in zip(self.dids, smartData.fbd.didunits):
            if not validator(did):
                return False, "验证失败,did {0} not match".format(str(did))
        return True,"验证成功"