# encoding:utf-8

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from application_plug import plug_register


@plug_register
class ProtocolTest(QLabel):

    def __init__(self):
        super(QLabel, self).__init__()
        self.setText("this is test")
        self.name = u"协议测试"