# encoding:utf-8
from .data_meta_type import *


class DataStruct(DataMetaType):
    def __init__(self):
        self.units = []

    def load_args(self, decoder=None,**kwargs):
        if decoder is not None:
            self.decode(decoder)
        else:
            for member in self.units:
                if member.name in kwargs:
                    member.value = kwargs[member.name]

    def declare_unit(self, unit):
        self.units.append(unit)

    def encode(self, encoder):
        for unit in self.units:
            unit.encode(encoder)

    def decode(self, decoder):
        for unit in self.units:
            if decoder.left_bytes() > unit.min_bytes():
                unit.decode(decoder)

    def __str__(self):
        txt = ""
        for unit in self.units:
            txt += " "
            txt += str(unit)
        return txt

    def to_readable_str(self):
        return str(self)

    def min_bytes(self):
        cnt = 0
        for unit in self.units:
            cnt += unit.min_bytes()
        return cnt


class DataArray(DataMetaType):
    def __init__(self,name, meta_type, attr="", cnt=0, decoder=None):
        super(DataArray, self).__init__(name, attr=attr, decoder=decoder)
        self.meta_type = meta_type
        self.cnt = cnt


