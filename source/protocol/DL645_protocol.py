# encoding:utf-8
from .protocol import Protocol, protocol_register
from .protocol import find_head
from .codec import BinaryEncoder, BinaryDecoder
from tools.converter import hexstr2bytes, str2hexstr
from tools.checker import checksum

DL645_HEAD = chr(0x68)
DL645_TAIL = chr(0x16)


class DIDReadAddress(object):
    def encode(self, encoder):
        encoder.encode_u8(0x13)
        encoder.encode_u8(0x00)

    def decode(self, decoder):
        pass


class DIDESTunnelData(object):
    def __init__(self, data):
        self.data = data

    def encode(self, encoder):
        encoder.encode_u8(0x50)
        encoder.encode_u8(0x4d)
        encoder.encode_str(self.data)

class DIDRealTimeMeterData(object):

    def __init__(self, data=None):
        self.address = data
        self.current_meter_used = 0

    def encode(self, encoder):
        encoder.encode_u8(00)
        encoder.encode_u8(0xff)
        encoder.encode_u8(0x01)
        encoder.encode_u8(0x00)
        encoder.encode_u8(0x00)
        encoder.encode_str(self.address[::-1])

    def decode(self, decoder):
        decoder.decode_bytes(54) # did
        self.address = decoder.decode_bytes(7)[::-1]


def data_encrypt(data):
    out = ""
    for byte in data:
        out += chr((ord(byte)+0x33)&0xff)
    return out

def data_unencrypt(data):
    out = ""
    for byte in data:
        out += chr((ord(byte)+256-0x33)&0xff)
    return out

@protocol_register
class DL645_07_Protocol(Protocol):
    """
    >>> encoder = BinaryEncoder()
    >>> protocol = DL645_07_Protocol()
    >>> encoder.encode_object(protocol)
    >>> str2hexstr(encoder.get_data())
    '68 11 11 11 11 11 11 68 01 02 80 83 3C 16'
    """

    @staticmethod
    def create_frame(*args, **kwargs):
        protocol = DL645_07_Protocol()
        protocol.address = args[0]
        protocol.did_unit = args[1]
        if kwargs.has_key("cmd"):
            protocol.cmd = kwargs["cmd"]
        return protocol

    def __init__(self, did_unit=None):
        self.address = chr(0x11)*6
        self.meter_type = 0x10
        self.cmd = 0x11
        self.length = 0x04
        self.did_unit = did_unit
        self.serial = 0x90

    def encode(self, encoder):
        encoder.encode_str(DL645_HEAD)
        encoder.encode_str(self.address[::-1])
        encoder.encode_str(DL645_HEAD)
        encoder.encode_u8(self.cmd)
        if self.cmd == 0x11:
            did_data = encoder.object2data(self.did_unit)
            encoder.encode_u8(len(did_data))
            did_data = data_encrypt(did_data)
            encoder.encode_str(did_data)
        elif self.cmd == 0x13:
            encoder.encode_u8(0x00)
        encoder.encode_u8(checksum(encoder.get_data()))
        encoder.encode_str(DL645_TAIL)

    def decode(self, decoder):
        decoder.decode_bytes(1)
        self.address = decoder.decode_bytes(6)[::-1]
        decoder.decode_bytes(1)
        self.cmd = decoder.decode_bytes(1)
        self.length = decoder.decode_byte()
        if self.length > 30:
            did_data = decoder.decode_bytes(self.length)
            did_data = data_unencrypt(did_data)
            did_decoder = BinaryDecoder()
            did_decoder.set_data(did_data)
            self.did_unit = did_decoder.decoder_for_object(DIDRealTimeMeterData)

    @staticmethod
    def find_frame_in_buff(data):
        """
        >>> receive_str =" fe fe 68 11 11 11 11 11 11 68 01 02 43 C3 3F 16 "
        >>> receive_data = hexstr2bytes(receive_str)
        >>> protocol =  DL645_07_Protocol()
        >>> protocol.find_frame_in_buff(receive_data)
        (True, 2, 14)
        >>> receive_data = hexstr2bytes("68 10 01 02 03 04 05 ")
        >>> protocol.find_frame_in_buff(receive_data)
        (False, 0, 0)
        """
        start_pos = 0
        found = 0
        while start_pos < (len(data) - 11):
            start_pos = find_head(data, start_pos, DL645_HEAD)
            if start_pos == -1:
                break
            frame_data = data[start_pos:]

            if len(frame_data) < 10:
                break

            data_len = ord(frame_data[9])

            if data_len + 12 > len(frame_data):
                start_pos += 1
                continue
            if ord(frame_data[10+data_len])  != checksum(frame_data[0:data_len+10]):
                start_pos += 1
                continue
            if frame_data[11+data_len] != DL645_TAIL:
                start_pos += 1
                continue
            found = 1
            break

        if found:
            return True, start_pos, data_len+12
        else:
            return False, 0, 0


@protocol_register
class DL645_97_Protocol(Protocol):
    """
    >>> encoder = BinaryEncoder()
    >>> protocol = DL645_07_Protocol()
    >>> encoder.encode_object(protocol)
    >>> str2hexstr(encoder.get_data())
    '68 11 11 11 11 11 11 68 01 02 80 83 3C 16'
    """

    @staticmethod
    def create_frame(*args, **kwargs):
        protocol = DL645_97_Protocol()
        protocol.address = args[0]
        protocol.did_unit = args[1]
        if kwargs.has_key("cmd"):
            protocol.cmd = kwargs["cmd"]
        return protocol

    def __init__(self, did_unit=None):
        self.address = chr(0x11)*6
        self.meter_type = 0x10
        self.cmd = 0x11
        self.length = 0x04
        self.did_unit = did_unit
        self.serial = 0x90

    def encode(self, encoder):
        encoder.encode_str(DL645_HEAD)
        encoder.encode_str(self.address[::-1])
        encoder.encode_str(DL645_HEAD)
        encoder.encode_u8(self.cmd)
        if self.cmd == 0x11:
            did_data = encoder.object2data(self.did_unit)
            encoder.encode_u8(len(did_data))
            did_data = data_encrypt(did_data)
            encoder.encode_str(did_data)
        elif self.cmd == 0x13:
            encoder.encode_u8(0x00)
        encoder.encode_u8(checksum(encoder.get_data()))
        encoder.encode_str(DL645_TAIL)

    def decode(self, decoder):
        decoder.decode_bytes(1)
        self.address = decoder.decode_bytes(6)[::-1]
        decoder.decode_bytes(1)
        self.cmd = decoder.decode_bytes(1)
        self.length = decoder.decode_byte()
        if self.length > 30:
            did_data = decoder.decode_bytes(self.length)
            did_data = data_unencrypt(did_data)
            did_decoder = BinaryDecoder()
            did_decoder.set_data(did_data)
            self.did_unit = did_decoder.decoder_for_object(DIDRealTimeMeterData)

    @staticmethod
    def find_frame_in_buff(data):
        """
        >>> receive_str ="fe fe 68 72 00 22 10 16 20 68 81 25 80 83 9B 43 33 33 33 33 33 33 34 B4 49 C3 52 34 3B 94 33 5F 33 3B 94 33 5F 33 33 33 33 33 33 33 33 33 1D 33 33 20 16  "
        >>> receive_data = hexstr2bytes(receive_str)
        >>> protocol =  DL645_97_Protocol()
        >>> protocol.find_frame_in_buff(receive_data)
        (True, 2, 49)
        >>> receive_data = hexstr2bytes("68 10 01 02 03 04 05 ")
        >>> protocol.find_frame_in_buff(receive_data)
        (False, 0, 0)
        """
        start_pos = 0
        found = 0
        while start_pos < (len(data) - 11):
            start_pos = find_head(data, start_pos, DL645_HEAD)
            if start_pos == -1:
                break
            frame_data = data[start_pos:]

            if len(frame_data) < 10:
                break

            data_len = ord(frame_data[9])

            if data_len + 12 > len(frame_data):
                start_pos += 1
                continue
            if ord(frame_data[10+data_len])  != checksum(frame_data[0:data_len+10]):
                start_pos += 1
                continue
            if frame_data[11+data_len] != DL645_TAIL:
                start_pos += 1
                continue
            found = 1
            break

        if found:
            return True, start_pos, data_len+12
        else:
            return False, 0, 0




