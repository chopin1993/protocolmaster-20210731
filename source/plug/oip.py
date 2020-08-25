# encoding:utf-8

from .application_plug import plug_register,ApplicationPlug
from .oip_ui import Ui_Form
from PyQt5.QtGui import QImage,QPixmap
from PyQt5 import QtCore
from protocol.image_0203_protocol import ThremalImageData

@plug_register
class OIPPlug(ApplicationPlug, Ui_Form):

    def __init__(self):
        super(OIPPlug, self).__init__("智能视觉传感器")
        self.setupUi(self)

    def handle_receive_data(self, msg):
        pass
        #self.show_img(msg)

    def show_img(self, msg):
        self.img = msg
        image = QImage(msg.data, msg.width, msg.height, QImage.Format_RGB16)
        pixelmap = QPixmap.fromImage(image)
        self.label.setPixmap(pixelmap)
        self.label.setAlignment(QtCore.Qt.AlignTop |QtCore.Qt.AlignHCenter)

    def get_protocols(self):
        return ["Smart7eProtocol",]