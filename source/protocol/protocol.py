# encoding:utf-8
from tools.converter import str2hexstr, hexstr2bytes
from .codec import BinaryDecoder, BinaryEncoder
from register import Register
from .fifo_buffer import FifoBuffer
import logging


def find_head(buff, start, head):
    """
    >>> buff = "1234567123"
    >>> find_head(buff, 0, '2')
    1
    >>> find_head(buff, 2, '2')
    8
    >>> find_head(buff, 2, '9')
    -1
    """
    pos = buff[start:].find(head)
    if -1 == pos:
        return pos
    return pos + start


class Protocol(Register):

    def __init__(self, data_cls, max_length=300):
        super().__init__()
        self.data_cls = data_cls
        self.buffer = FifoBuffer()
        self.max_length = max_length

    def __str__(self):
        return self.name

    def store_and_find_frame(self, msg: object) -> object:
        self.buffer.receive(msg)
        buffer_data = self.buffer.peek(-1)
        decoder = BinaryDecoder()
        (found, start, length) = self.find_frame_in_buff(buffer_data)
        if found:
            self.buffer.read(start + length)
            frame_data = buffer_data[start:start + length]
            decoder.set_data(frame_data)
            monitor_data = self.decode(decoder)
            return monitor_data
        else:
            if self.buffer.data_length() > self.max_length:
                logging.warning(self.__class__.name + "test engine buff too big %d, we will clear all buff",
                                self.buffer.data_length())
                self.buffer.read(self.buffer.read(self.buffer.data_length()))
        return None

    def find_frame_in_buff(self, data):
        """
        :param data:数据
        :return: (是否有完整帧，起始位置，帧长度)
        """
        raise NotImplementedError

    def decode(self, decoder):
        return decoder.decoder_for_object(self.data_cls)

    def to_readable_str(self, text):
        data = hexstr2bytes(text)
        found, start, datalen = self.find_frame_in_buff(data)
        if found:
            data = data[start:start + datalen]
            data = BinaryDecoder.data2object(self.data_cls, data)
            return data.to_readable_str
        else:
            return "no valid frame"
