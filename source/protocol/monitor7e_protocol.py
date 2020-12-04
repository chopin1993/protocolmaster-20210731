# encoding:utf-8
from .protocol import Protocol
from .protocol import find_head
from tools.checker import checksum
from tools.esenum import EsEnum
import time
from .smart7e_DID import *

Monitor_ID = bytes([0x7e])


class HardwareEnum(EsEnum):
    SPI = 0
    UART = 1
    GPIO = 2
    RELAY = 3
    过零检测 = 4
    监测器 = 0xf

# serial wire bus
class SPICmd(EsEnum):
    MOINTOR_DETECT_NOTIFY = 0x01
    DEVICE_ID = 0x02
    RESTART = 0x11
    DATA = 0x03

class UARTCmd(EsEnum):
    DATA = 0x01
    W_DATA = 0x81
    SETTING = 0x12
    W_SETTING= 0x92


class RELAYCmd(EsEnum):
    DATA = 0x01

class GPIOCmd(EsEnum):
    DATA = 0x01
    SETTING = 0x02

class Parity(EsEnum):
      无校验=0
      奇校验=1
      偶校验=2


class UARTSettingFbd(DataFragment):
    def __init__(self, decoder=None, **kwargs):
        super(UARTSettingFbd, self).__init__()
        self.declare_unit(DataU32(name="baudrate"))
        self.declare_unit(DataU8Enum(name="parity", name_dict=Parity.name_dict()))
        self.load_args(decoder,**kwargs)


class MessageType(EsEnum):
    温度 = 1
    湿度 = 2
    电压 = 3
    电流 = 4
    电阻 = 5
    雷达人体存在 = 11
    光学人体存在 = 12
    红外传感器 = 13
    插卡取电 = 21
    大量程照度 = 31
    自然光照度 = 32
    照度 = 33
    继电器输出 = 41
    光耦输出 = 42
    可控硅输出 = 43
    按键输入 = 51
    干节点输入 = 52
    干簧管输入 = 53
    二进制输入 = 61
    二进制输出 = 62
    字节类型 = 80
    设备信息 = 0xff


class PLCChannel(EsEnum):
    RCV = 0x00
    SND = 0x01
    PRINT = 0x40


class MonitorSWBFBD(DataFragment):
    """
    监测器的数据包结构
    CHN（u8），MSG(u8),LEN(u8) INFODATA
    """
    def __init__(self, device_chn=None, msg_type=None, data=bytes(), decoder=None):
        self.device_chn = device_chn
        self.msg_type =MessageType.to_enum(msg_type)
        self.data = data
        self.len = len(data)
        if decoder is not None:
            self.decode(decoder)

    def decode(self, decoder):
        self.device_chn = decoder.decode_u8()
        self.msg_type = MessageType.to_enum(decoder.decode_u8())
        self.len = decoder.decode_u8()
        self.data = decoder.decode_bytes(self.len)

    def encode(self, encoder):
        encoder.encode_u8(self.device_chn)
        encoder.encode_u8(self.msg_type)
        encoder.encode_u8(self.len)
        encoder.encode_str(self.data)

    def to_readable_str(self):
        text = "chn[{}]:{} type[{}]:{} len[{}]:{} data:{}".format(\
            u8tohexstr(self.device_chn),self.device_chn,\
            u8tohexstr(self.msg_type.value),self.msg_type.name,\
            u8tohexstr(self.len),self.len,\
            str2hexstr(self.data))
        return text


class Monitor7EData(DataFragment):
    """
    0X7E INTERFACE(u8) CMD(u8) LEN(u8) DATA 0X7E
    """
    @staticmethod
    def create_uart_message(data, cmd=UARTCmd.DATA, group=0):
        if isinstance(data, DataFragment):
            data = BinaryEncoder.object2data(data)
        return Monitor7EData(hardware=HardwareEnum.UART, group=group, cmd=cmd, data=data)

    def __init__(self, hardware=None, group=0, cmd=None, data=bytes(), decoder=None):
        if hardware == 0xf:
            group = 0xf
        self.hardware = hardware
        self.group = group
        self.cmd = cmd.value if isinstance(cmd, Enum) else cmd
        if not isinstance(data, bytes):
            data = BinaryEncoder.object2data(data)
        self.data = data
        self.len = len(data)
        if decoder is not None:
            self.decode(decoder)

    def is_uart_data(self):
        return self.hardware == HardwareEnum.UART

    def decode(self, decoder):
        self.raw_data = deepcopy(decoder.data)
        decoder.decode_u8()
        data = decoder.decode_bytes(-1)
        data = data[:-1]
        real_data = self.to_real_data(data)
        decoder = BinaryDecoder(real_data)
        u8_data = decoder.decode_u8()
        self.hardware = HardwareEnum.to_enum((u8_data & 0xf0) >> 4)
        self.group = u8_data&0x0f
        self.cmd = decoder.decode_u8()
        self.len = decoder.decode_u8()
        self.data = decoder.decode_bytes(self.len)

    def encode(self, encoder):
        tmp_encoder = BinaryEncoder()
        interface = (self.hardware.value << 4) | self.group
        tmp_encoder.encode_u8(interface)
        tmp_encoder.encode_u8(self.cmd)
        tmp_encoder.encode_u8(len(self.data))
        tmp_encoder.encode_bytes(self.data)
        encoder.encode_str(Monitor_ID)
        escape_data = self.to_escape_data(tmp_encoder.get_data())
        encoder.encode_bytes(escape_data)
        encoder.encode_str(Monitor_ID)

    def to_escape_data(self, data):
        output = bytes()
        for byte in data:
            if byte == 0x7e:
                output += bytes([0X7D, 0X5E])
            elif byte == 0x7d:
                output += bytes([0X7D, 0X5D])
            else:
                output += bytes([byte])
        return output

    def to_real_data(self, data):
        output = bytes()
        i = 0
        flag = 0
        for byte in data:
            if flag == 0x20:
                byte ^= 0x20
                flag = 0
            if byte == 0x7d:
                flag = 0x20
                continue
            output += bytes([byte])
        return output

    def to_readable_str(self):
        interface = (self.hardware.value << 4) | self.group
        text = "interface[{}] 功能:{} channel:{} cmd[{}]:{} len[{}]:{} data:{}".format(\
            u8tohexstr(interface),self.hardware.name,self.group,\
            u8tohexstr(self.cmd),self.cmd,\
            u8tohexstr(self.len),self.len,\
            str2hexstr(self.data))
        return text

    def __str__(self):
        data = BinaryEncoder.object2data(self)
        return str2hexstr(data)


class Monitor7eProtocol(Protocol):
    FRMAE_MIN = 5

    def __init__(self):
        super().__init__(Monitor7EData)

    def find_frame_in_buff(self, data):
        start_pos = 0
        total_len = len(data)
        show_time = False
        start = time.time()
        assert not isinstance(data, str)
        while start_pos < (len(data) - self.FRMAE_MIN):
            start_pos = find_head(data, start_pos, Monitor_ID)
            if start_pos == -1:
                break
            frame_data = data[start_pos:]
            end =find_head(frame_data, 1, Monitor_ID)
            if start_pos == (end-1):
                start_pos +=1
                continue
            if end == -1:
                break
            else:
                return True, start_pos, end+1
        if (show_time):
            print("time const:", time.time() - start, "data length", total_len)
        return False, 0, 0

