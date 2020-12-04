# encoding:utf-8
from tools.converter import str2hexstr, hexstr2bytes
from .codec import BinaryDecoder,BinaryEncoder
from register import Register

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

    def __init__(self, data_cls):
        super().__init__()
        self.data_cls = data_cls

    def __str__(self):
        return self.name

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
            data = data[start:start+datalen]
            data = BinaryDecoder.data2object(self.data_cls, data)
            return data.to_readable_str()
        else:
            return "no valid frame"