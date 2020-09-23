# encoding:utf-8
from tools.checker import checksum

class DataFragment(object):

    def __init__(self, name, default_value, encode_depends=None, decode_depends=None):
        self.name = name
        self.default_value = default_value
        self.encode_depends = encode_depends
        self.decode_depends = decode_depends
        self.depends_dict = None

    def encode(self, encoder):
        encoder.encode_str(self.default_value)

    def decode(self, decoder):
        return decoder.decode_bytes(self.length())

    def length(self):
        return len(self.default_value);

    def get_min_length(self):
        return len(self.default_value);

    def set_depends(self, depends):
         self.depends_dict = depends

    def fit(self):
        pass


class ConstDataFragment(DataFragment):
    def __init__(self, name, data):
        super(ConstDataFragment, self).__init__(name, data)

    def fit(self, data):
        return self.default_value == data[0:len(self.default_value)], len(self.default_value)



class FixedLengthDataFragment(DataFragment):

    @staticmethod
    def create_auto_increment_data_fragment(name, default_value, length):
        def auto_increment(value):
            int_value = ord(value)
            int_value += 1
            int_value = int_value&0xff
            return chr(int_value+1)
        return FixedLengthDataFragment(name, default_value, length, auto_increment)

    def __init__(self, name, value, length, encoder_hook=None):
        super(FixedLengthDataFragment, self).__init__(name, value)
        self.length = length
        self.encoder_hook = encoder_hook

    def encode(self, encoder):
        encoder.encode_str(self.default_value)
        if self.encoder_hook is not None:
            self.default_value = self.encoder_hook(self.default_value)

    def decode(self, decoder):
        return decoder.decode_bytes(self.length())

    def length(self):
        return self.length;

    def get_min_length(self):
        return self.length;

    def set_depends(self, depends):
         self.depends_dict = depends

    def fit(self, data):
        if len(data) > self.length:
            return True, self.length
        return False


class StatisticsDataFragment(DataFragment):

    @staticmethod
    def create_length_statistics(name, length, encode_depends, decode_depends):
        return

    @staticmethod
    def create_cs_statistics(name, length, encode_depends, decode_depends):
        pass

    def __init__(self, name, encode_depends, decode_depends, statistics_func):
        super(StatisticsDataFragment, self).__init__( name, None, encode_depends, decode_depends)
        self.statistics_func = statistics_func

    def encode(self, encoder):
        value = self.statistics_func(**self.depends_dict)
        encoder.encode_u8(value)

    def decode(self, decoder):
        return decoder.decode_bytes(self.length())

    def length(self):
        return len(self.default_value);

    def get_min_length(self):
        return len(self.default_value);

    def set_depends(self, depends):
         self.depends_dict = depends

    def fit(self, data):
        pass


class VariableDataFragment(DataFragment):
    def __init__(self, name, depends):
        self.name = name
        self.depends = depends