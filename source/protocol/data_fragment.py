# encoding:utf-8
from .DataMetaType import *


class DataFragment(object):
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
            unit.decode(decoder)

    def __str__(self):
        txt = ""
        for unit in self.units:
            txt += " "
            txt += str(unit)
        return txt

    def to_readable_str(self):
        return str(self)