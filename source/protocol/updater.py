import os
from .codec import BinaryDecoder
import re

def parse_file(data):
    decoder = BinaryDecoder(data)
    outputs = {}

    for i in range(4):
        value = decoder.decode_cstr()
        key = re.findall(r"([\w\s]*):", value)
        value = re.findall(r":(\w*)", value)
        outputs[key] = value

    return NotImplementedError


class Updater(object):
    def __init__(self, name):
        self.name = name
        assert os.path.exists(name)
        with open(self.name, "rb") as handle:
            self.data = handle.read()
            # self.version, self.crc, self.file_size, self.program = parse_file(self.data)

    def test_method(self):
        raise NotImplementedError
