# encoding:utf-8


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


#
#
# self.add_fragment(ConstDataFragment("head", chr(0x68)))
#        self.add_fragment(ConstDataFragment("type", chr(0x01)))
#        self.add_fragment(FixedLengthDataFragment("address", 7, chr(0xaa) * 7))
#        self.add_fragment(FixedLengthDataFragment("cmd", 1, chr(0x02)))
#        self.add_fragment(StatisticsDataFragment.create_length_statistics("length", 1, ("didunit",)))
#        self.add_fragment(VariableDataFragment("didunit", "length"))
#        self.add_fragment(StatisticsDataFragment.create_cs_statistics("cs", 1, ("head", "type", "address", "cmd", "didunit")))
#        self.add_fragment(ConstDataFragment("tail", chr(0x16)))

class Protocol(object):

    @staticmethod
    def create_frame(self, *args, **kwargs):
        pass

    def __init__(self):
        self.data_fragments = []

    def _get_min_length(self):
        length = 0
        for fragment in self.data_fragments:
            length += fragment.get_min_length()
        return length

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

    def encode(self, encoder, dicts):
        for fragment in self.data_fragments:
            fragment.set_depends(self.gather_fragments(fragment.encode_depends))
            encoder.encode_object(fragment)

    def decode(self, decoder):
        datas = dict()
        for fragment in self.data_fragments:
            fragment.set_depends(self.gather_fragments(fragment.decode_depends, datas))
            datas[fragment.name] = decoder.encode_object(fragment)
        return datas



_all_protocols = dict()


def protocol_register(media_class):
    global _all_protocols
    _all_protocols[media_class.__name__] = media_class
    return media_class


def protocol_create(name):
    from ..user_exceptions import FoundClassException
    protocol_class = _all_protocols(name)
    if protocol_class is None:
        raise FoundClassException(name)
    return protocol_class()



