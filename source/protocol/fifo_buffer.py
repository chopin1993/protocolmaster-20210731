# encoding:utf-8
from copy import  deepcopy

class FifoBuffer(object):
    """
    >>> buff = FifoBuffer()
    >>> buff.receive('123')
    >>> buff.peek(4)
    '123'
    >>> buff.read(1)
    '1'
    >>> buff.peek(2)
    '23'
    """

    def __init__(self):
        self.buff = bytes([])

    def receive(self, data):
        self.buff += data

    def peek(self, length):
        if length == -1:
            return  deepcopy(self.buff)
        length = min(length, len(self.buff))
        return self.buff[0:length]

    def read(self, length):
        if length <0:
            length = len(self.buf)
        data = self.peek(length)
        if length == 0:
            return bytes([])
        if len(self.buff) <= length:
            self.buff = bytes([])
        else:
            self.buff = self.buff[length:]
        return data

    def data_length(self):
        return len(self.buff)