# encoding:utf-8

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from application_plug import plug_register,ApplicationPlug


@plug_register
class ProtocolTest(ApplicationPlug):

    def __init__(self):
        super(ProtocolTest, self).__init__("test")

    def get_medias_cnt(self):
        return 1

    def get_protocols(self):
        return 1