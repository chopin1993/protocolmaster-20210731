# encoding:utf-8
from .DataMetaType import *


class DataFragment(object):
    def __init__(self, decoder=None, units=None, *kwargs):
        if decoder is not None:
            self.decode(decoder)
        self.kwargs = kwargs
        self.units = units
        for member in self.units:
            if member.name in kwargs:
                member.value = kwargs[member.name]

    def declare_unit(self, unit):
        self.units.append(unit)

    def encode(self, encoder):
        for unit in self.units:
            unit.encoder(unit)
        raise NotImplementedError

    def decode(self, decoder):
        raise NotImplementedError