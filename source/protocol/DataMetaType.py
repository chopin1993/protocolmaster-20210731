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
        type_dict = {}
        type_dict["string"] = "cstring"
        type_dict["bytes"] = "ByteArray"
        for key, value in member.items():
            if value in type_dict:
                value = type_dict[value]
            cls = DataMetaType.find_sub_class_by_name("Data"+value)
            if cls is None:
                print("no meta type:",value)
                raise NotImplemented
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
        self._value = value
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
        return "{0}:{1}".format(self._get_pure_name(), self.value_str())

    def _get_pure_name(self):
        name = self.name
        return name.split("_")[0]

    def get_widgets(self, *args, **kwargs):
        if self.widget is None:
            widget = QtWidgets.QWidget()
            layout = QHBoxLayout()
            name_widget = QLabel(self._get_pure_name())
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
    def __init__(self, name=None, value=None, decoder=None):
        super(DataCString, self).__init__(name, value, decoder)

    def encode(self, encoder, **kwargs):
        encoder.encode_str(self.value)

    def decode(self, decoder, **kwargs):
        self.value = decoder.decode_cstr()

    def str2value(self, strvalue):
        return strvalue


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

    def str2value(self, str_value):
        return to_number(str_value)



class DataU16(DataMetaType):
    def __init__(self,name=None, value=None, decoder=None):
        super(DataU16, self).__init__(name, value, decoder)

    def encode(self, encoder, **kwargs):
        encoder.encode_u16(self.value)

    def decode(self, decoder, **kwargs):
        self.value = decoder.decode_u16()

    def str2value(self, str_value):
        return to_number(str_value)


class DataU32(DataMetaType):
    def __init__(self,name=None, value=None, decoder=None):
        super(DataU32, self).__init__(name, value, decoder)

    def encode(self, encoder, **kwargs):
        encoder.encode_u32(self.value)

    def decode(self, decoder, **kwargs):
        self.value = decoder.decode_u32()

    def str2value(self, str_value):
        return to_number(str_value)


class DataU8Enum(DataMetaType):
    def __init__(self,name=None, value=None, decoder=None, cls=None):
        super(DataU8Enum, self).__init__(name, value, decoder)
        self.enum_cls = cls

    def get_widgets(self, *args, **kwargs):
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
        self._value = decoder.decode_u8()

    def value_str(self):
       return self.enum_cls(value=self.value).name

    def str2value(self, str_value):
        return self.enum_cls[str_value].value

    def __str__(self):
        return self.value_str()
