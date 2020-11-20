import struct
import numpy as np
from tools.converter import bytearray2str,str2bytearray

class Encoder(object):
    def __init__(self):
        self.data = bytes([])

class Decoder(object):
    pass


class BinaryEncoder(Encoder):
    def __init__(self):
        self.data = bytes([])

    def encode_str(self, str):
        return self.encode_bytes(str)

    def encode_bytes(self, bytes):
        if isinstance(bytes, str):
            bytes = str2bytearray(bytes)
        self.data += bytes

    def encode_bcd_u16(self, nb):
        nb = int(str(nb), base=16)
        self.encode_u16(nb)

    def encode_bcd_u8(self, nb):
        nb = int(str(nb),base=16)
        self.encode_u8(nb)

    def encode_u8(self, nb):
        self.data += struct.pack("@B", nb)

    def encode_u16(self, nb):
        self.data += struct.pack("@H", nb)

    def encode_s16(self, nb):
        self.data += struct.pack("@h", nb)

    def encode_s32(self, nb):
        self.data += struct.pack("@i", nb)

    def encode_u32(self, nb):
        self.data += struct.pack("@I", nb)

    def encode_object(self, object_data):
        object_data.encode(self)

    @staticmethod
    def object2data(a_object):
        encoder = BinaryEncoder()
        a_object.encode(encoder)
        return encoder.get_data()

    def get_data(self, size=None):
        if size is not None:
            padding = size - len(self.data)
            self.data += padding * chr(0)
        return self.data

    def reset(self):
        self.data = bytes([])


class BinaryDecoder(Decoder):

    def __init__(self, data=None):
        self.data = data

    def left_bytes(self):
        return len(self.data)

    def decoder_for_object(self, cls, **kwargs):
        protocol = cls(decoder=self, **kwargs)
        return protocol

    def decode_bytes(self, length):
        if length == 0:
            return bytes()
        elif length < 0:
            return self.decode_left_bytes()
        data = self.data[0:length]
        self.data = self.data[length:]
        return data

    def decode_numpy_float(self, w, h):
        data = self.decode_bytes(w*h*4)
        data = np.frombuffer(data, dtype=np.float32)
        data = data.reshape(h,w)
        return data

    def decode_numpy_u16(self, w, h):
        data = self.decode_bytes(w*h*2)
        data = np.frombuffer(data, dtype=np.uint16)
        data = data.reshape(h,w)
        return data

    def decode_uint(self):
        data = self.decode_bytes(4)
        return struct.unpack("I",data)[0]

    def decode_u32(self):
        return self.decode_uint()

    def decode_u16(self):
        data = self.decode_bytes(2)
        return struct.unpack("H",data)[0]

    def decode_bcd_u16(self):
        data = self.decode_u16()
        data = int("%x" %(data))
        return data

    def decode_bcd_u8(self):
        data = self.decode_u8()
        data = int("%x" % (data))
        return data

    def decode_u8(self):
        data = self.decode_byte()
        return struct.unpack("B",data)[0]

    def decode_s8(self):
        data = self.decode_byte()
        return struct.unpack("b",data)[0]

    def decode_byte(self):
        data = self.decode_bytes(1)
        return data

    def decode_left_bytes(self):
        data = self.data
        self.data = bytes()
        return data

    def decode_cstr(self):
        i = 0
        for i in range(len(self.data)):
            if self.data[i] == 0:
                break
        data = self.decode_bytes(i+1)
        return  bytearray2str(data)

    def set_data(self, data):
        self.data = data

    @staticmethod
    def data2object(cls, data):
        decoder = BinaryDecoder(data)
        data = decoder.decoder_for_object(cls)
        return data