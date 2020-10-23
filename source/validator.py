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
            return True, "expect success"
        else:
            return False, "expect fail"

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


class SmartOneDidValidator(Validator):
    def __init__(self, src, dst, cmd, did, value):
        self.cmd = cmd
        self.did = did
        self.value = value
        self.src = src
        self.dst = dst

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
            return True, "expect success"
        else:
            return False, "expect fail,cmd src dst or did data not match"