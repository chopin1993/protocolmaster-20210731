# encoding:utf-8

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from application_plug import plug_register,ApplicationPlug
from thermal_image_ui import Ui_Form

@plug_register
class ThermalImage(ApplicationPlug, Ui_Form):

    def __init__(self):
        super(ThermalImage, self).__init__("test")
        self.setupUi(self)

    def readImageOnce(self):
        print "read image once"

    def get_medias_cnt(self):
        return 1

    def get_protocols(self):
        return 1