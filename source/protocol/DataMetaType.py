from tools.converter import bytearray2str,str2hexstr
from protocol.codec import BinaryEncoder,BinaryDecoder
from register import Register


class DataMetaType(Register):

    @classmethod
    def create(cls, member):
        for key,value in member.items():
            cls = DataMetaType.find_class_by_name(value)
            return cls(name=key)
        return None


    def __init__(self, name=None, value=None, decoder=None):
        self.name = name
        self.value = value
        if decoder is not None:
            self.decode(decoder)

    def encode(self, encoder):
        pass

    def decode(self, decoder):
        pass

    def value_str(self):
        if isinstance(self.value, bytes) or isinstance(self.value, bytearray):
            return str2hexstr(self.value)
        else:
            return str(self.value)

    def __str__(self):
        return "{0}:{1}".format(self.name,self.value_str())


class DataCString(DataMetaType):
    def __init__(self, name=None, value=None, decoder=None):
        super(DataCString, self).__init__(name, value, decoder)

    def encode(self, encoder):
        encoder.encode_str(self.value)

    def decode(self, decoder):
        self.value = decoder.decode_cstr()


class DataU8(DataMetaType):
    def __init__(self,name=None, value=None, decoder=None):
        super(DataU8, self).__init__(name, value, decoder)

    def encode(self, encoder):
        encoder.encode_u8(self.value)

    def decode(self, decoder):
        self.value = decoder.decode_u8()