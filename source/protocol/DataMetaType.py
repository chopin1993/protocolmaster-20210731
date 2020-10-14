#encoding:utf-8
from tools.converter import bytearray2str,str2hexstr,hexstr2bytes
from protocol.codec import BinaryEncoder,BinaryDecoder
from register import Register
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import types

def to_number(txt):
    if txt is "":
        return 0
    else:
        return int(txt)


class DataMetaType(Register):

    @classmethod
    def create(cls, member):
        '''
          利用字符串从json中创建DataMetaType
        '''
        for key,value in member.items():
            cls = DataMetaType.find_class_by_name(value)
            return cls(name=key)
        return None

    def __init__(self, name=None, value=None, decoder=None):
        '''
        数据显示的基本单元，主要作用如下：
        1. 创建对应的wdiget
        2. 发送时，编码widget数据
        3. 接收时，将数据放到widget进行显示
        4. 接收时，将数据解析为对人类友好的txt
        '''
        self.name = name
        self.value = value
        if decoder is not None:
            self.decode(decoder)

    def encode(self, encoder, **kwargs):
        encoder.encode_str(self.value)

    def decode(self, decoder, **kwargs):
        self.value = decoder.decode_left_bytes()

    def to_value(self, widget):
        return hexstr2bytes(widget.text())

    def value_str(self):
        if isinstance(self.value, bytes) or isinstance(self.value, bytearray):
            return str2hexstr(self.value)
        else:
            return str(self.value)

    def __str__(self):
        return "{0}:{1}".format(self._get_pure_name(), self.value_str())

    def _get_pure_name(self):
        name = self.name
        return name.split("_")[0]

    def create_widgets(self, *args, **kwargs):
        widget = QtWidgets.QWidget()
        layout = QHBoxLayout()
        name_widget = QLabel(self._get_pure_name())
        value_widget = QLineEdit()
        layout.addWidget(name_widget)
        layout.addWidget(value_widget)
        widget.setLayout(layout)
        widget.value_widget = value_widget
        widget.setObjectName("dataMeta")
        value_widget.setObjectName("valueMeta")
        return widget

    def encode_widget_value(self, widget, encoder, **kwargs):
        value_widget = widget.value_widget
        self.value = self.to_value(value_widget)
        self.encode(encoder)

    def set_widget_value(self, widget, decoder, **kwargs):
        self.decode(decoder, **kwargs)
        widget.value_widget.setText(self.value_str())


class ContextBaseValue(DataMetaType):
    def __init__(self,  name=None, value=None, decoder=None,
                 encoder_func=None, decoder_func=None, to_value_func=None, value_str_func=None):
        super(ContextBaseValue, self).__init__(name=name, value=value, decoder=decoder)
        self.encode_func = encoder_func
        self.decoder_func = decoder_func
        self.to_value_func = to_value_func
        self.value_str_func = value_str_func

    def encode(self, encoder, **kwargs):
        self.encode_func(self.value, encoder, **kwargs)

    def decode(self, decoder, **kwargs):
        self.value = self.decoder_func(decoder, **kwargs)

    def to_value(self, widget):
        if self.to_value_func is None:
            return to_number(widget.text())
        return self.to_value_func(widget.text())

    def value_str(self):
        if self.value_str_func is None:
            return str(self.value)
        else:
            return self.value_str_func(self.value)


class DataCString(DataMetaType):
    def __init__(self, name=None, value=None, decoder=None):
        super(DataCString, self).__init__(name, value, decoder)

    def encode(self, encoder, **kwargs):
        encoder.encode_str(self.value)

    def decode(self, decoder, **kwargs):
        self.value = decoder.decode_cstr()

    def to_value(self, widget):
        return widget.text()


class DataByteArray(DataMetaType):
    def __init__(self, name=None, value=None, decoder=None):
        super(DataByteArray, self).__init__(name, value, decoder)


class DataU8(DataMetaType):
    def __init__(self,name=None, value=None, decoder=None):
        super(DataU8, self).__init__(name, value, decoder)

    def encode(self, encoder, **kwargs):
        encoder.encode_u8(self.value)

    def decode(self, decoder, **kwargs):
        self.value = decoder.decode_u8()

    def to_value(self, widget):
        return to_number(widget.text())


class DataU16(DataMetaType):
    def __init__(self,name=None, value=None, decoder=None):
        super(DataU16, self).__init__(name, value, decoder)

    def encode(self, encoder, **kwargs):
        encoder.encode_u16(self.value)

    def decode(self, decoder, **kwargs):
        self.value = decoder.decode_u16()

    def to_value(self, widget):
        return to_number(widget.text())


class DataU8Enum(DataMetaType):
    def __init__(self,name=None, value=None, decoder=None, cls=None):
        super(DataU8Enum, self).__init__(name, value, decoder)
        self.enum_cls = cls

    def create_widgets(self,  *args, **kwargs):
        widget = QtWidgets.QWidget()
        layout = QHBoxLayout()
        name_widget = QLabel(self._get_pure_name())
        value_widget = QComboBox()
        for e in self.enum_cls:
            value_widget.addItem(e.name)
        layout.addWidget(name_widget)
        layout.addWidget(value_widget)
        widget.setLayout(layout)
        widget.value_widget = value_widget
        widget.setObjectName("dataMeta")
        value_widget.setObjectName("valueMeta")
        return widget

    def set_widget_value(self, widget, decoder, **kwargs):
        self.decode(decoder, **kwargs)
        widget.value_widget.setCurrentText(self.value_str())

    def encode(self, encoder, **kwargs):
        encoder.encode_u8(self.value)

    def decode(self, decoder, **kwargs):
        self.value = decoder.decode_u8()

    def value_str(self):
       return self.enum_cls(value=self.value).name

    def to_value(self, widget):
        return self.enum_cls[widget.currentText()].value

    def __str__(self):
        return self.value_str()
