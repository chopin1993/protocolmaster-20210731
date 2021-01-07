# encoding:utf-8
from .data_meta_type import *
from copy import deepcopy

class DataStruct(DataMetaType):

    @staticmethod
    def create_data_struct(metas):
        data = DataStruct()
        for meta in metas:
            data.declare_unit(meta)
        return data

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

    def min_bytes(self):
        cnt = 0
        for unit in self.units:
            cnt += unit.min_bytes()
        return cnt


class DataArray(DataMetaType):
    def __init__(self, name, metas,cnt_name="",values=[], cnt=-1, decoder=None):
        assert len(metas)>=0
        self.metas = metas
        self.cnt_name = cnt_name
        self.data_struct = DataStruct.create_data_struct(metas)
        super(DataArray, self).__init__(name, attr=metas[0].attr, decoder=decoder)
        self.meta_values = []
        self.cnt = cnt
        self.value = values

    @property
    def value(self):
        return self.meta_values

    @value.setter
    def value(self, value):
        assert isinstance(value, list),"必须使用list给数组赋值"
        self.meta_values = []
        for unit in value:
            self.data_struct.load_args(unit)
            unit = deepcopy(self.data_struct)
            self.meta_values.append(unit)


    def decode(self, decoder, **kwargs):
        self.meta_values = []
        while decoder.left_bytes() >= self.data_struct.min_bytes():
            self.data_struct.decode(decoder)
            unit = deepcopy(self.data_struct)
            self.meta_values.append(unit)

    def encode(self, encoder, **kwargs):
        for unit in self.meta_values:
            encoder.encode_object(unit)

    def __str__(self):
        txt = "["
        for idx,unit in enumerate(self.meta_values):
            txt +="\n        {},".format(str(unit))
        txt += "]"
        return txt
