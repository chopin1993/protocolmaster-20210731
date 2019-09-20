# encoding:utf-8
from media.serial_media import SerialMedia
from protocol.codec import BinaryEncoder, BinaryDecoder
from protocol.fifo_buffer import FifoBuffer
from tools.converter import hexstr2bytes, str2hexstr
from PyQt5.QtCore import QObject, pyqtSignal
from tools.converter import bytearray2str,str2bytearray
from protocol import Protocol

class SessionSuit(QObject):
    data_ready = pyqtSignal(Protocol)

    @staticmethod
    def create_binary_suit(media, protocol):
        encoder = BinaryEncoder()
        decoder = BinaryDecoder()
        return SessionSuit(media, encoder, decoder, protocol)

    def __init__(self, media, encoder, decoder, protocol):
        media.data_ready.connect(self.handle_receive_data)
        self.media = media
        self.encoder = encoder
        self.decoder = decoder
        self.protocol = protocol
        self.buffer = FifoBuffer()
        super(SessionSuit, self).__init__()

    def handle_receive_data(self, string):
        assert len(string) > 0
        self.buffer.receive(string)
        data = self.buffer.peek(10000)
        protocol = self.protocol
        print("data rcv",len(data))
        (found, start, length) = protocol.find_frame_in_buff(data)
        if found:
            self.buffer.read(start + length)
            print("rcv", str2hexstr(data[0:start + length]))
            frame_data = data[start:start+length]
            self.decoder.set_data(frame_data)
            protocol.decode(self.decoder)
            self.data_ready.emit(protocol)


    def write(self, data, **kwargs):
        protocol = self.protocol.create_frame(None,data, **kwargs)
        self.encoder.encode_object(protocol)
        data = self.encoder.get_data()
        self.media.send(data)
        print("snd",str2hexstr(data))
        self.encoder.reset()

    def close(self):
        self.media.close()
