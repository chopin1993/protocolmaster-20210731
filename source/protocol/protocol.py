# encoding:utf-8
from tools.converter  import str2hexstr
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

    @staticmethod
    def create_frame(self, *args, **kwargs):
        pass

    @staticmethod
    def create_raw_frame(data):
        pro = Protocol()
        pro.raw_data = data
        return pro

    def __init__(self):
        self.data_fragments = []
        self.raw_data = None

    def _get_min_length(self):
        length = 0
        for fragment in self.data_fragments:
            length += fragment.get_min_length()
        return length

    def __str__(self):
        return "{0} no data analyse \n".format(self.__class__.__name__)

    def _get_frame_len(self, data ,decoder):
        decoder.data = data
        data_fragments =  decoder.decode_for_object(self)
        length = 0
        for data_fragment in data_fragments:
            length += data_fragment.get_length()
        return length

    def find_frame_in_buff(self, data, decoder):
        start_pos = 0
        found = 0
        min_length = self._get_min_length()
        left_length = len(data)
        while left_length >=  min_length:
            frame_data = data[start_pos:]
            for fragment in self.data_fragments:
                if not fragment.fit(frame_data):
                    start_pos += 1
                    found = False
                    break;
            if found:
                return True, start_pos, self._get_frame_len(data[start_pos:], decoder)

        return False, 0, 0


    def add_fragment(self, fragment):
        self.data_fragments.append(fragment)

    def encode(self, encoder):
        print("error not handle encode")
        pass

    def decode(self, decoder):
        datas = dict()
        for fragment in self.data_fragments:
            fragment.set_depends(self.gather_fragments(fragment.decode_depends, datas))
            datas[fragment.name] = decoder.encode_object(fragment)
        return datas

    def to_readable_str(self, hex_text):
        return "no text tranlation"

