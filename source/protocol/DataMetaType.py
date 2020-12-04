#encoding:utf-8
from tools.converter import bytearray2str,str2hexstr,hexstr2bytes
from protocol.codec import BinaryEncoder,BinaryDecoder
from register import Register
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import types
from enum import Enum

def to_number(txt):
    if txt is "":
        return 0
    else:
        return int(txt)


class DataMetaType(Register):

    @staticmethod
    def to_cls_name(value):
        value = value.split(".")[0]
        type_dict = {}
        type_dict["string"] = "cstring"
        type_dict["bytes"] = "ByteArray"
        type_dict['vs'] = "ContextBaseValue"
        type_dict['f32'] = "ByteArray"
        if value in type_dict:
            value = type_dict[value]
        if not value.startswith("Data"):
            value = "Data" + value
        return value

    @classmethod
    def create(cls, member):
        '''
        利用字符串从json中创建DataMetaType
        '''
        for key, value_raw in member.items():
            value = DataMetaType.to_cls_name(value_raw)
            cls = DataMetaType.find_sub_class_by_name(value)
            if cls is None:
                print("no meta type:",value)
                raise NotImplementedError(str(value))
            ob = cls(name=key)
            if "attr" in member:
                ob.attr = member["attr"]
            ob.extra = value_raw.split(".")[1:]
            return ob
        return None

    def __init__(self, name=None, value="", attr="", decoder=None):
        '''
        数据显示的基本单元，主要作用如下：
        1. 创建对应的wdiget
        2. 发送时，编码widget数据
        3. 接收时，将数据放到widget进行显示
        4. 接收时，将数据解析为对人类友好的txt
        '''
        self.name = name
        self._value = value
        self.attr = attr
        self.extra = []
        if decoder is not None:
            self.decode(decoder)
        self.widget = None

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if isinstance(value, str):
            self._value = self.str2value(value)
        else:
            self._value = value
        if self.widget is not None:
            self.widget.value_widget.setText(self.value_str())

    def encode(self, encoder, **kwargs):
        encoder.encode_str(self._value)

    def decode(self, decoder, **kwargs):
        self._value = decoder.decode_left_bytes()

    def str2value(self, str_value):
        return hexstr2bytes(str_value)

    def widget2value(self, widget):
        if isinstance(widget, QLineEdit):
            value = widget.text()
        elif isinstance(widget, QComboBox):
            value = widget.currentText()
        else:
            raise ValueError("not recgonize type")
        return self.str2value(value)

    def value_str(self):
        if self._value is None:
            return ""
        if isinstance(self._value, bytes) or isinstance(self._value, bytearray):
            return str2hexstr(self._value)
        else:
            return str(self._value)

    def __str__(self):
        return "{0}:{1}".format(self.name, self.value_str())

    def get_widgets(self, *args, **kwargs):
        if self.widget is None:
            widget = QtWidgets.QWidget()
            layout = QHBoxLayout()
            name_widget = QLabel(self.name)
            value_widget = QLineEdit()
            if self._value is not None:
                value_widget.setText(self.value_str())
            value_widget.textChanged.connect(self.text_change)
            layout.addWidget(name_widget)
            layout.addWidget(value_widget)
            widget.setLayout(layout)
            widget.value_widget = value_widget
            widget.setObjectName("dataMeta")
            value_widget.setObjectName("valueMeta")
            self.widget = widget
        return self.widget

    def text_change(self, str1):
        self._value = self.widget2value(self.widget.value_widget)

    def encode_widget_value(self, widget, encoder, **kwargs):
        value_widget = widget.value_widget
        self._value = self.widget2value(value_widget)
        self.encode(encoder, **kwargs)

    def set_widget_value(self, widget, decoder, **kwargs):
        self.decode(decoder, **kwargs)
        widget.value_widget.setText(self.value_str())


class DataContextBaseValue(DataMetaType):
    def __init__(self,  name=None, value="", decoder=None,
                 encoder_func=None, decoder_func=None, to_value_func=None, value_str_func=None):
        super(DataContextBaseValue, self).__init__(name=name, value=value, decoder=decoder)
        self.encode_func = encoder_func
        self.decoder_func = decoder_func
        self.to_value_func = to_value_func
        self.value_str_func = value_str_func

    def encode(self, encoder, **kwargs):
        self.encode_func(self.value, encoder, **kwargs)

    def decode(self, decoder, **kwargs):
        self.value = self.decoder_func(decoder, **kwargs)

    def widget2value(self, widget):
        if self.to_value_func is None:
            return to_number(widget.text())
        return self.to_value_func(widget.text())

    def value_str(self):
        if self.value_str_func is None:
            return str(self.value)
        else:
            return self.value_str_func(self.value)


class DataCString(DataMetaType):
    def __init__(self, name=None, value="", decoder=None):
        super(DataCString, self).__init__(name, value, decoder)

    @property
    def reverse(self):
        if len(self.extra) > 0 and self.extra[0]=='r':
            return True
        else:
            return False

    def encode(self, encoder, **kwargs):
        value = self.value
        if self.reverse:
            value = value[::-1]
        encoder.encode_str(value)

    def decode(self, decoder, **kwargs):
        value = decoder.decode_cstr()
        if self.reverse:
            value = value[::-1]
        self.value = value

    def str2value(self, strvalue):
        return strvalue


class DataByteArray(DataMetaType):
    def __init__(self, name=None, value=bytes(),length=-1 ,decoder=None):
        super(DataByteArray, self).__init__(name, value, decoder)
        self.length = length

    def decode(self, decoder, **kwargs):
        self._value = decoder.decode_bytes(self.length)


class DataU8(DataMetaType):
    def __init__(self,name=None, value=0, decoder=None):
        super(DataU8, self).__init__(name, value, decoder)

    def encode(self, encoder, **kwargs):
        encoder.encode_u8(self.value)

    def decode(self, decoder, **kwargs):
        self.value = decoder.decode_u8()

    def str2value(self, str_value):
        return to_number(str_value)



class DataU16(DataMetaType):
    def __init__(self,name=None, value=0, decoder=None):
        super(DataU16, self).__init__(name, value, decoder)

    def encode(self, encoder, **kwargs):
        encoder.encode_u16(self.value)

    def decode(self, decoder, **kwargs):
        self.value = decoder.decode_u16()

    def str2value(self, str_value):
        return to_number(str_value)


class DataU32(DataMetaType):
    def __init__(self,name=None, value=0, decoder=None):
        super(DataU32, self).__init__(name, value, decoder)

    def encode(self, encoder, **kwargs):
        encoder.encode_u32(self.value)

    def decode(self, decoder, **kwargs):
        self.value = decoder.decode_u32()

    def str2value(self, str_value):
        return to_number(str_value)


class DataU8Enum(DataMetaType):
    def __init__(self, name=None, value=None, decoder=None, name_dict=None):
        if isinstance(value, Enum):
            value = str(value)
        super(DataU8Enum, self).__init__(name, value, decoder)
        self.name_dict = name_dict

    def get_widgets(self, *args, **kwargs):
        widget = QtWidgets.QWidget()
        layout = QHBoxLayout()
        name_widget = QLabel(self.name)
        value_widget = QComboBox()
        for key, value in self.name_dict.items():
            value_widget.addItem(key)
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
        self._value = decoder.decode_u8()

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if isinstance(value, Enum):
            value = value.name
        if isinstance(value, str):
            self._value = self.str2value(value)
        else:
            self._value = value
        if self.widget is not None:
            self.widget.value_widget.setText(self.value_str())

    def value_str(self):
        for key, value in self.name_dict.items():
            if value == self._value:
                return key
        return "no txt for {0}".format(self._value)

    def str2value(self, str_value):
        return self.name_dict[str_value]

    def __str__(self):
        return self.value_str()
