from tools.converter import *
import types
import weakref
from engine.validator import *
from .test_engine import TestEngine,Device,log_snd_frame,log_rcv_frame
import logging
from .test_engine import Routine


class LocalRoutine(Routine):
    """
    主要用来处理单个did，上报和联动测试
    """
    def __init__(self, name, device:Device):
        super(LocalRoutine, self).__init__(name, device)

    def send_local_msg(self, cmd, value, **kwargs):
        fbd = LocalFBD(cmd, value)
        data = Smart7EData(0, 0, fbd)
        self.device.write(data)
        log_snd_frame(self.name, data)

    def expect_local_msg(self, cmd, value=None, timeout=2, **kwargs):
        self.validate = SmartLocalValidator(cmd=cmd)
        self.wait_event(timeout)

