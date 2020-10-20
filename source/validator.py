from register import Register
from protocol.smart7e_protocol import *

class Validator(Register):
    def __int__(self):
        pass

    def __call__(self, data):
        raise NotImplemented


class SmartLocalValidator(Validator):

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __call__(self, data):
        is_local = data.is_local()
        fbd = data.fbd
        values = self.kwargs['cmd']
        cmd = fbd.cmd
        if isinstance(values, list):
            cmd_valid = cmd in values
        else:
            cmd_valid = (cmd == fbd.cmd)
        if is_local and cmd_valid:
            return True, "expect sucess"
        else:
            return False, "expect fail"


class SmartOneDidValidator(Validator):
    def __init__(self, src, dst, cmd, did, value):
        self.cmd = cmd
        self.did = did
        self.value = value
        self.src = src
        self.dst = dst

    def __call__(self, smartData):
        did = smartData.fbd.didunits[0]
        if  self.cmd == smartData.fbd.cmd and \
            self.src == smartData.said and \
            self.dst == smartData.taid and \
            self.did ==  did.DID and\
            self.value == did.data:
            return True, "expect sucess"
        else:
            return False, "expect fail"