# encoding:utf-8
from .protocol import Protocol
from .protocol import find_head
from tools.checker import checksum
from tools.esenum import EsEnum
import time
from .smart7e_DID import *
from register import Register
Monitor_ID = bytes([0x9e])


class HardwareEnum(EsEnum):
    SPI = 0
    UART = 1
    GPIO = 2
    RELAY = 3
    CROSS_ZERO = 4 #过零检测
    监测器 = 0xf


# serial wire bus
class SPICmd(EsEnum):
    MOINTOR_DETECT_NOTIFY = 0x01
    DEVICE_ID = 0x02
    RESTART = 0x11
    W_RESTART = 0x83
    DATA = 0x03
    W_DATA = 0x83


class UARTCmd(EsEnum):
    DATA = 0x01
    W_DATA = 0x81
    SETTING = 0x12
    W_SETTING= 0x92


class RELAYCmd(EsEnum):
    DATA = 0x01
    W_DATA= 0x81

class GPIOCmd(EsEnum):
    DATA = 0x01
    SETTING = 0x02


class CrossZeroCmd(EsEnum):
    DATA = 0x01

class Parity(EsEnum):
      无校验=0
      奇校验=1
      偶校验=2



class SPIMessageType(EsEnum):
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


class BytesChannelEnum(EsEnum):
    PLC_RCV = 0x00
    PLC_SND = 0x01
    PRINT = 0x40


class MonitorUnit(DataStruct):
    SUPPORT_CMDS = []

class MonitorByteArray(MonitorUnit):
    SUPPORT_CMDS = []
    def __init__(self, decoder=None, **kwargs):
        super(MonitorUnit, self).__init__()
        self.declare_unit(DataByteArray(name="data"))
        self.load_args(decoder, **kwargs)


class UARTSettingFbd(MonitorUnit):
    SUPPORT_CMDS = [UARTCmd.SETTING, UARTCmd.W_SETTING]

    def __init__(self, decoder=None, **kwargs):
        super(UARTSettingFbd, self).__init__()
        self.declare_unit(DataU32(name="baudrate"))
        self.declare_unit(DataU8Enum(name="parity", name_dict=Parity.name_dict()))
        self.load_args(decoder,**kwargs)


class SPIDeviceID(MonitorUnit):
    SUPPORT_CMDS = [SPICmd.DEVICE_ID]

    def __init__(self, decoder=None, **kwargs):
        """
        {ver(1Byte)+sn,dkey,aid,pwd,gid,panid,sid}
        """
        super(SPIDeviceID, self).__init__()
        self.declare_unit(DataU8(name="version"))
        self.declare_unit(DataByteArray(name="sn",length=12))
        self.declare_unit(DataByteArray(name="dkey", length=8))
        self.declare_unit(DataU32(name="aid"))
        self.declare_unit(DataU16(name="pwd"))
        self.declare_unit(DataU16(name="gid"))
        self.declare_unit(DataU16(name="panid"))
        self.declare_unit(DataU16(name="sid"))
        self.load_args(decoder, **kwargs)


class SPIData(MonitorUnit):
    SUPPORT_CMDS = [SPICmd.DATA,SPICmd.W_DATA]

    def __init__(self, chn=None, msg_type=None, data=None, decoder=None):
        """
         CHN（u8），MSG(u8),LEN(u8) INFODATA
        """
        super(SPIData, self).__init__()
        self.chn = chn
        self.msg_type = SPIMessageType.to_enum(msg_type)
        if data is not None and not isinstance(data, (bytes,bytearray)):
            data = SPIData.encode_data(msg_type, data)
        self.data = data
        if decoder is not None:
            self.decode(decoder)

    @staticmethod
    def encode_data(msg_type, value):
        msg_type = SPIMessageType.to_enum(msg_type)
        unit = SPIData.get_data_parse_object(msg_type)
        unit.value = value
        data = BinaryEncoder.object2data(unit)
        return data

    @staticmethod
    def get_data_parse_object(msg_type):
        if msg_type in [SPIMessageType.二进制输入,\
                             SPIMessageType.二进制输出,\
                             SPIMessageType.光学人体存在,\
                             SPIMessageType.红外传感器,\
                             SPIMessageType.雷达人体存在,\
                             SPIMessageType.可控硅输出,\
                             SPIMessageType.干节点输入,\
                             SPIMessageType.继电器输出,\
                             SPIMessageType.干簧管输入,\
                             SPIMessageType.插卡取电,\
                             SPIMessageType.光耦输出]:
            return DataU8()
        elif msg_type in [SPIMessageType.按键输入]:
            name_dict={"短按":1, "长按":2}
            return DataU8Enum(name_dict=name_dict)
        elif msg_type in [SPIMessageType.温度,\
                               SPIMessageType.湿度,\
                               SPIMessageType.大量程照度,\
                               SPIMessageType.照度,\
                               SPIMessageType.电压,\
                               SPIMessageType.电流,\
                               SPIMessageType.电阻,\
                               SPIMessageType.自然光照度,\
                               ]:
            return DataU32
        elif msg_type in [SPIMessageType.字节类型]:
            return DataByteArray()
        else:
            return DataByteArray()

    def is_plc_rcv(self):
        return self.msg_type == SPIMessageType.字节类型 and self.chn == BytesChannelEnum.PLC_RCV.value

    def is_plc_snd(self):
        return self.msg_type == SPIMessageType.字节类型 and self.chn == BytesChannelEnum.PLC_SND.value

    def is_print_msg(self):
        return self.msg_type == SPIMessageType.字节类型 and self.chn == BytesChannelEnum.PRINT

    def encode(self, encoder):
        encoder.encode_u8(self.chn)
        encoder.encode_u8(self.msg_type.value)
        encoder.encode_u8(len(self.data))
        encoder.encode_bytes(self.data)

    def decode(self, decoder):
        self.chn = decoder.decode_u8()
        self.msg_type = SPIMessageType.to_enum(decoder.decode_u8())
        self.len  = decoder.decode_u8()
        self.data = decoder.decode_bytes(self.len)


    def __str__(self):
        if self.msg_type == SPIMessageType.字节类型:
            chn_name = BytesChannelEnum.value_to_name(self.chn)
        else:
            chn_name = self.chn
        txt = "chn[{}]:{} {}[{}] len[{}]:{} data:{}".format(\
                    u8tohexstr(self.chn),chn_name,\
                    self.msg_type.name, self.msg_type.value,\
                    u8tohexstr(self.len),self.len,\
                    str2hexstr(self.data))
        return txt

class Monitor7EData(DataStruct):
    """
    0X9E INTERFACE(u8) CMD(u8) LEN(u8) DATA 0X9E
    """
    @staticmethod
    def create_uart_message(data, cmd=UARTCmd.DATA, group=0):
        if isinstance(data, DataStruct):
            data = BinaryEncoder.object2data(data)
        return Monitor7EData(hardware=HardwareEnum.UART, group=group, cmd=cmd, data=data)

    @staticmethod
    def create_spi_message(data,  group=0, cmd=SPICmd.W_DATA):
        return Monitor7EData(hardware=HardwareEnum.SPI, group=group, cmd=cmd, data=data)

    @staticmethod
    def create_relay_message(channel, status, cmd=RELAYCmd.W_DATA):
        encoder = BinaryEncoder()
        encoder.encode_u8(status)
        data = encoder.get_data()
        return Monitor7EData(hardware=HardwareEnum.RELAY, group=channel, cmd=cmd, data=data)

    @staticmethod
    def create_cross_zero_message(channel, cmd=CrossZeroCmd.DATA):
        return Monitor7EData(hardware=HardwareEnum.CROSS_ZERO, group=channel, cmd=cmd, data=bytes())

    def __init__(self, hardware=None, group=0, cmd=None, data=bytes(), decoder=None):
        if hardware == 0xf:
            group = 0xf
        self.raw_data = None
        self.hardware = hardware
        self.group = group
        self.cmd = self.to_enum_cmd(cmd) if cmd else None
        if not isinstance(data, bytes):
            data = BinaryEncoder.object2data(data)
        self.data = data
        self.len = len(data)
        if decoder is not None:
            self.decode(decoder)

    def is_uart_data(self):
        return self.hardware == HardwareEnum.UART

    def is_spi_data(self):
        return self.hardware == HardwareEnum.SPI

    def is_crosszero_data(self):
        return self.hardware== HardwareEnum.CROSS_ZERO

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
        self.cmd = self.to_enum_cmd(decoder.decode_u8())
        self.len = decoder.decode_u8()
        self.data = decoder.decode_bytes(self.len)

    def encode(self, encoder):
        tmp_encoder = BinaryEncoder()
        interface = (self.hardware.value << 4) | self.group
        tmp_encoder.encode_u8(interface)
        tmp_encoder.encode_u8(self.cmd.value)
        tmp_encoder.encode_u8(len(self.data))
        tmp_encoder.encode_bytes(self.data)
        encoder.encode_str(Monitor_ID)
        escape_data = self.to_escape_data(tmp_encoder.get_data())
        encoder.encode_bytes(escape_data)
        encoder.encode_str(Monitor_ID)

    def to_escape_data(self, data):
        output = bytes()
        for byte in data:
            if byte == Monitor_ID[0]:
                output += bytes([0X7D, byte^0x20])
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
            if byte == 0x7d:
                flag = 0x20
                continue
            if flag == 0x20:
                byte ^= 0x20
                flag = 0
            output += bytes([byte])
        return output

    def to_enum_cmd(self, cmd):
        return self.get_cmd_enum(self.hardware).to_enum(cmd)

    def get_cmd_enum(self, hardware):
        enum_dict = {
            HardwareEnum.UART:UARTCmd,
            HardwareEnum.SPI:SPICmd,
            HardwareEnum.GPIO:GPIOCmd,
            HardwareEnum.RELAY:RELAYCmd
        }
        assert self.hardware in enum_dict
        return enum_dict[hardware]

    def get_parsed_cls(self, cmd):
        for key, cls in MonitorUnit.get_sub_class_dict().items():
            if cmd in cls.SUPPORT_CMDS:
                return cls
        return MonitorByteArray

    def get_parsed_data(self):
        cls = self.get_parsed_cls(self.cmd)
        decoder = BinaryDecoder(self.data)
        return decoder.decoder_for_object(cls)

    def to_readable_str(self):
        interface = (self.hardware.value << 4) | self.group
        text = "interface[{}] 功能:{} channel:{} cmd[{}]:{} len[{}]:{} {}".format(\
            u8tohexstr(interface),self.hardware.name,self.group,\
            u8tohexstr(self.cmd.value),self.cmd.name,\
            u8tohexstr(self.len),self.len,\
            self.get_parsed_data())
        return text

    def __str__(self):
        data = self.raw_data if self.raw_data is not None else BinaryEncoder.object2data(self)
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

