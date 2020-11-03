from register import Register
from protocol.smart7e_protocol import *

class Validator(Register):
    def __init__(self):
        self.ack = False
        pass

    def __call__(self, data):
        raise NotImplemented

class NoMessage(Validator):
    def __init__(self,expect_no_message=False):
        super(NoMessage, self).__init__()
        self.expect_no_message = expect_no_message

    def __call__(self, data):
        if data is None or not self.expect_no_message:
            return True, "验证成功"
        else:
            return False,"验证失败,收到异常报文"


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
        place_holders = self.placeholder.split(" ")
        for i,holder in enumerate(place_holders):
            if "*" in holder:
                continue
            value = int(holder, base=16)
            if value != data[i]:
                return False
        return True


class UnitCompare(Validator):
    def __init__(self, **kwargs):
        self.kwarges = kwargs

    def __call__(self, data):
        for key, value in self.kwarges:
            pass
        return True

class SmartOneDidValidator(Validator):
    def __init__(self, src, dst, cmd, did, value,ack=False,**kwargs):
        super(SmartOneDidValidator, self).__init__()
        self.cmd = cmd
        self.did = did
        self.value = value
        self.src = src
        self.dst = dst
        self.kwargs = kwargs
        self.ack = ack

    def __call__(self, smartData):
        def compare_data(expect_value,target_value):
            if isinstance(expect_value, Validator):
                return expect_value(did.data)
            else:
                return  expect_value == target_value
        did = smartData.fbd.didunits[0]
        if  self.cmd == smartData.fbd.cmd and \
            self.src == smartData.said and \
            self.dst == smartData.taid and \
            self.did == did.DID and \
            compare_data(self.value, did.data):
            return True, "验证成功"
        else:
            return False, "验证失败,cmd src dst or did data not match"