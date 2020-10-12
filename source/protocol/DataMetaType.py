from tools.converter import bytearray2str,str2hexstr,hexstr2bytes
from protocol.codec import BinaryEncoder,BinaryDecoder
from register import Register
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class DataMetaType(Register):

    @classmethod
    def create(cls, member):
        for key,value in member.items():
            cls = DataMetaType.find_class_by_name(value)
            return cls(name=key)
        return None

    def __init__(self, name=None, value=None, decoder=None):
        self.name = name
        self.value = value
        if decoder is not None:
            self.decode(decoder)

    def encode(self, encoder):
        pass

    def decode(self, decoder):
        pass

    def value_str(self):
        if isinstance(self.value, bytes) or isinstance(self.value, bytearray):
            return str2hexstr(self.value)
        else:
            return str(self.value)

    def __str__(self):
        return "{0}:{1}".format(self.name,self.value_str())


    def encoder_widget_helper(self, widget, encoder, to_value):
        value_widget = widget.value_widget
        self.value = to_value(value_widget)
        self.encode(encoder)

    def get_pure_name(self):
        name = self.name
        return name.split("_")[0]

    def create_widgets(self, cmd):
        widget = QtWidgets.QWidget()
        layout = QHBoxLayout()
        name_widget = QLabel(self.get_pure_name())
        value_widget = QLineEdit()
        layout.addWidget(name_widget)
        layout.addWidget(value_widget)
        widget.setLayout(layout)
        widget.value_widget = value_widget
        widget.setObjectName("dataMeta")
        value_widget.setObjectName("valueMeta")
        return widget

    def encode_widget_value(self, widget, encoder):
        self.encoder_widget_helper(widget, encoder, lambda widget:hexstr2bytes(widget.text()))

    def set_widget_value(self, widget, decoder):
        self.decode(decoder)
        widget.value_widget.setText(self.value_str())



class DataCString(DataMetaType):
    def __init__(self, name=None, value=None, decoder=None):
        super(DataCString, self).__init__(name, value, decoder)

    def encode(self, encoder):
        encoder.encode_str(self.value)

    def decode(self, decoder):
        self.value = decoder.decode_cstr()

    def encode_widget_value(self, widget, encoder):
        value_widget = widget.value_widget
        txt = value_widget.text()
        encoder.encode_str(txt)


class DataU8(DataMetaType):
    def __init__(self,name=None, value=None, decoder=None):
        super(DataU8, self).__init__(name, value, decoder)

    def encode(self, encoder):
        encoder.encode_u8(self.value)

    def decode(self, decoder):
        self.value = decoder.decode_u8()

    def encode_widget_value(self, widget, encoder):
        def to_value(widget):
            if widget.text() is "":
                return 0
            else:
                return int(widget.text())
        self.encoder_widget_helper(widget, encoder, to_value)


class DataU16(DataMetaType):
    def __init__(self,name=None, value=None, decoder=None):
        super(DataU16, self).__init__(name, value, decoder)

    def encode(self, encoder):
        encoder.encode_u16(self.value)

    def decode(self, decoder):
        self.value = decoder.decode_u16()

    def encode_widget_value(self, widget, encoder):
        value_widget = widget.value_widget
        txt = hexstr2bytes(value_widget.text())
        encoder.encode_str(txt)

    def encode_widget_value(self, widget, encoder):
        def to_value(widget):
            if widget.text() is "":
                return 0
            else:
                return int(widget.text())
        self.encoder_widget_helper(widget, encoder, to_value)


class ConextBaseStep(DataMetaType):
    pass

class DataU8Enum(DataMetaType):
    def __init__(self,name=None, value=None, decoder=None, cls=None):
        super(DataU8Enum, self).__init__(name, value, decoder)
        self.enum_cls = cls

    def create_widgets(self, cmd):
        widget = QtWidgets.QWidget()
        layout = QHBoxLayout()
        name_widget = QLabel(self.get_pure_name())
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

    def value_str(self):
       return self.enum_cls(value=self.value).name

    def __str__(self):
        return self.value_str()

    def encode(self, encoder):
        encoder.encode_u8(self.value)

    def decode(self, decoder):
        self.value = decoder.decode_u8()

    def encode_widget_value(self, widget, encoder):
        self.encoder_widget_helper(widget, encoder, lambda widget: self.enum_cls[widget.currentText()].value)

    def set_widget_value(self, widget, decoder):
        self.decode(decoder)
        widget.value_widget.setCurrentText(self.value_str())
