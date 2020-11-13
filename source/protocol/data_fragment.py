# encoding:utf-8

class DataFragment(object):

    def __init__(self, decoder=None, *kwargs):
        if decoder is not None:
            self.decode(decoder)
        self.kwargs = kwargs

    def encode(self, encoder):
        raise NotImplementedError

    def decode(self, decoder):
        raise NotImplementedError

    def length(self):
        raise NotImplementedError
