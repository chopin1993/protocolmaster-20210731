# encoding:utf-8
from media.serial_media import SerialMedia
from protocol.codec import BinaryEncoder, BinaryDecoder
from protocol.fifo_buffer import FifoBuffer
from tools.converter import hexstr2bytes, str2hexstr
from PyQt5.QtCore import QObject, pyqtSignal, QTimer
from tools.converter import bytearray2str, str2bytearray
from protocol import Protocol
import datetime
import logging
from copy import deepcopy
from protocol.data_container import DataMetaType, DataByteArray


class SessionSuit(QObject):
    data_ready = pyqtSignal(DataMetaType)
    data_snd = pyqtSignal(DataMetaType)
    data_clean = pyqtSignal(DataMetaType)

    @staticmethod
    def create_binary_suit(media, protocol):
        encoder = BinaryEncoder()
        decoder = BinaryDecoder()
        return SessionSuit(media, encoder, decoder, protocol)

    def __init__(self, media, encoder, decoder, protocol):

        self._media = None
        self.media = media
        self.encoder = encoder
        self.decoder = decoder
        self.protocol = protocol
        self.buffer = FifoBuffer()
        super(SessionSuit, self).__init__()
        self.bytes_timer = QTimer()
        self.bytes_timer.timeout.connect(self.clear_data)

        self.tailing = 0

    @property
    def media(self):
        return self._media

    @media.setter
    def media(self, value):
        if self._media is not None:
            self._media.data_ready.disconnect(self.handle_receive_data)
        value.data_ready.connect(self.handle_receive_data)
        self._media = value

    def handle_receive_data(self, string):
        # assert len(string) > 0
        if len(string) > 0:
            self.tailing = 0
            pass
        self.tailing += 1
        if self.tailing < 5:
            pass

        self.buffer.receive(string)
        protocol = deepcopy(self.protocol)
        # print(datetime.datetime.now()," rcv bytes:",len(string),string[0])
        while True:
            data = self.buffer.peek(-1)
            (found, start, length) = protocol.find_frame_in_buff(data)
            if found:
                raw_data = self.buffer.read(start + length)
                # logging.info("rev raw: %s",str2hexstr(raw_data))
                frame_data = data[start:start + length]
                self.decoder.set_data(frame_data)
                data = protocol.decode(self.decoder)
                self.data_ready.emit(data)
            elif length > 0:
                self.buffer.read(start + length)
            else:
                if len(data) >= 800000:
                    self.clear_data()
                else:
                    if len(data) > 0:
                        self.bytes_timer.start(5000)
                    else:
                        self.bytes_timer.stop()
                break

    def clear_data(self):
        data = self.buffer.read(-1)
        if len(data) > 0:
            self.data_clean.emit(DataByteArray(value=data))
            logging.warning("noise data %s", str2hexstr(data))
        self.bytes_timer.stop()

    def write(self, data, **kwargs):
        self.data_snd.emit(data)
        self.encoder.reset()
        self.encoder.encode_object(data)
        data = self.encoder.get_data()
        self._media.send(data)

    def close(self):
        self._media.close()

    def status_message(self):
        length = self.buffer.data_length()
        if length > 0:
            msg = "received {0} bytes, wait more data receiving...".format(length)
        else:
            msg = 'reveive no data, free'
        return msg
