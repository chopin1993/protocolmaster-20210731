import os
from tools.import_helper import import_all_python
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class ApplicationPlug(QWidget):

    def __init__(self, name):
        super(QWidget, self).__init__()
        self.name = name

    def get_medias_cnt(self):
        raise NotImplementedError

    def get_protocols(self):
         raise NotImplementedError

    def handle_receive_data(self):
        pass

    def handle_send_data(self):
        pass


_all_plugs = dict()


def plug_register(plugs_class):
    global _all_plugs
    _all_plugs[plugs_class.__name__] = plugs_class
    return plugs_class


def plugs_get_all():
    plugs = list()
    for value in _all_plugs.values():
        plugs.append(value())
    return plugs

