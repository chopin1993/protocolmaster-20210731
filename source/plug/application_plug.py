import os
from tools.import_helper import import_all_python
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import logging


class ApplicationPlug(QWidget):

    def __init__(self, name):
        super(QWidget, self).__init__()
        self.name = name
        self.session = None

    def get_protocols(self):
         return []

    def handle_receive_data(self, msg):
        print("unhandle plug data", msg)

    def send_data(self, data):
        self.session.write(data)

    def media_error_happen(self):
        pass

    def show_error_msg(self, title, msg):
        QMessageBox.information(self, title, msg)



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