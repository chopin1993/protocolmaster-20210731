import struct
import numpy as np

class Encoder(object):
    def __init__(self):
        self.data = bytes([])

    def encode_str(self, str):
        pass

    def encode_char(self, nb):
        pass

    def encode_unsigned_short(self, nb):
        pass

    def encode_int(self, nb):
       pass

    def encode_object(self, nb):
        pass

    def object2data(self):
        pass

    def get_data(self):
        return bytes([1,2,3])


class Decoder(object):
    pass


class BinaryEncoder(Encoder):
    def __init__(self):
        self.data = bytes([])

    def encode_bytes(self, bytes):
        self.data += bytes

    def encode_byte(self, nb):
        self.data += struct.pack("@B", nb)

    def encode_unsigned_short(self, nb):
        self.data += struct.pack("@H", nb)

    def encode_short(self, nb):
        self.data += struct.pack("@h", nb)

    def encode_int(self, nb):
        self.data += struct.pack("@i", nb)

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

    def decoder_for_object(self, cls):
        protocol = cls()
        protocol.decode(self)
        return protocol

    def decode_bytes(self, length):
        data = self.data[0:length]
        self.data = self.data[length:]
        return data

    def decode_numpy_float(self, w, h):
        data = self.decode_bytes(w*h*4)
        data = np.frombuffer(data, dtype=np.float32)
        data = data.reshape(h,w)
        return data

    def decode_uint(self):
        data = self.decode_bytes(4)
        return struct.unpack("I",data)[0]

    def decode_u16(self):
        data = self.decode_bytes(2)
        return struct.unpack("H",data)[0]

    def decode_byte(self):
        data = self.decode_bytes(1)
        return data

    def set_data(self, data):
        self.data = data