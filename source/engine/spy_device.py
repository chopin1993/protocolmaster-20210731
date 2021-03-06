from engine.test_engine import log_snd_frame, log_rcv_frame, log_info
from protocol.monitor9e_protocol import *
from protocol.fifo_buffer import FifoBuffer
import logging
from protocol.smart7e_protocol import Smart7eProtocol
import engine


class SpyDevice(object):
    _instance = None

    @staticmethod
    def handle_spi_msg(msg):
        if not SpyDevice.instance().probe_connected:
            SpyDevice.instance().probe_connected = True
            engine.add_doc_info("\n\n***************监测器探测成功，测试将充分利用监测器信息**********\n\n")
        log_rcv_frame("被测设备.raw", msg, only_log=True)
        cmd = SPICmd.to_enum(msg.cmd)
        if cmd in [SPICmd.MOINTOR_DETECT_NOTIFY]:
            log_info("被测设备", "探测调试总线")
        elif cmd in [SPICmd.RESTART, SPICmd.W_RESTART]:
            log_info("被测设备", "同步调试总线")
        elif cmd in [SPICmd.DEVICE_ID]:
            device_info = msg.get_parsed_data()
            log_info("被测设备", "device info:%s", str(device_info))
            SpyDevice.instance().set_device_info(device_info)
        elif cmd in [SPICmd.DATA]:
            spi_data = msg.get_parsed_data()
            SpyDevice.instance().rcv_probe_msg(spi_data)
        else:
            log_rcv_frame("被测设备", "ignore " + msg, only_log=True)

    @staticmethod
    def instance():
        if SpyDevice._instance is None:
            SpyDevice._instance = SpyDevice()
        return SpyDevice._instance

    def __init__(self):
        self.rcv_proto = Smart7eProtocol()
        self.snd_proto = Smart7eProtocol()
        self.info = None
        self.rcv_frames = []
        self.snd_frames = []
        self.sensor_status = {}
        self.probe_connected = False
        self.snd_hook = None
        self.rcv_hook = None

    def append_rcv_frame(self, frame):
        if self.rcv_hook:
            self.rcv_hook(frame)
        if len(self.rcv_frames) > 10:
            self.rcv_frames.pop(0)
        self.rcv_frames.append(frame)
        log_rcv_frame("被测设备", frame, only_log=True)

    def append_snd_frame(self, frame):
        if self.snd_hook:
            self.snd_hook(frame)
        if len(self.snd_frames) > 10:
            self.snd_frames.pop(0)
        self.snd_frames.append(frame)
        log_snd_frame("被测设备", frame, only_log=True)

    def get_snd_frames(self):
        return self.snd_frames

    def set_device_info(self, info):
        self.info = info

    def rcv_probe_msg(self, spi_msg):
        if spi_msg.is_plc_rcv():
            ret = self.rcv_proto.store_and_find_frame(spi_msg.data)
            if ret is not None:
                self.append_rcv_frame(ret)
        elif spi_msg.is_plc_snd():
            ret = self.snd_proto.store_and_find_frame(spi_msg.data)
            if ret is not None:
                self.append_snd_frame(ret)
        elif spi_msg.is_print_msg():
            log_info("print %s", bytearray2str(spi_msg.data))
        else:
            self.set_sensor_status(spi_msg.chn, spi_msg.msg_type, spi_msg.data)

    def get_sensor_status(self, chn, msg_type):
        msg_type = SPIMessageType.to_enum(msg_type)
        key = "{}-{}".format(msg_type.name, chn)
        if key in self.sensor_status:
            return self.sensor_status[key]
        return None

    def set_sensor_status(self, chn, msg_type, status):
        key = "{}-{}".format(msg_type.name, chn)
        log_info("被测设备", "%s: channel:%s value:%s", msg_type.name, chn, str2hexstr(status))
        self.sensor_status[key] = status

    def clear_status(self):
        self.sensor_status = {}
        self.rcv_frames = []
        self.snd_frames = []
        self.probe_connected = False
        self.snd_hook = None
        self.rcv_hook = None

    def clear_send_frames(self):
        self.snd_frames = []

    def install_rcv_hook(self, hook):
        self.rcv_hook = hook
