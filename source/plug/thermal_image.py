# encoding:utf-8

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from .application_plug import plug_register,ApplicationPlug
from .thermal_image_ui import Ui_Form

@plug_register
class ThermalImage(ApplicationPlug, Ui_Form):

    def __init__(self):
        super(ThermalImage, self).__init__("红外阵列90240")
        self.setupUi(self)

    def readImageOnce(self):
        self.session.write(bytes("1124324324",encoding='utf8'))
        print("read image once")

    def get_medias_cnt(self):
        return 1

    def get_protocols(self):
        return 1