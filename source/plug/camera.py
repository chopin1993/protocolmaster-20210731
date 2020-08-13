# encoding:utf-8

from .application_plug import plug_register,ApplicationPlug
from .camera_ui import Ui_Form
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer
import datetime
from tools.imgtool import numpy2jpg
from protocol.image_0203_protocol import ThremalImageData

@plug_register
class CameraImage(ApplicationPlug, Ui_Form):

    def __init__(self):
        super(CameraImage, self).__init__("摄像头调试")
        self.setupUi(self)
        # 高字节：低字节 r g b 。计算机采用小端模式
        test = ThremalImageData(400,300,bytes([0x00,0xf8]*400*100) + bytes([0xe0,0x07]*400*100)+bytes([0x1f,0x00]*400*100))
        self.show_img(test)
        self.img = None

    def handle_receive_data(self, msg):
        self.show_img(msg)

    def show_img(self, msg):
        self.img = msg
        image = QImage(msg.data, msg.width, msg.height, QImage.Format_RGB16)
        pixelmap = QPixmap.fromImage(image)
        self.label.setPixmap(pixelmap)
        self.label.setAlignment(QtCore.Qt.AlignTop |QtCore.Qt.AlignHCenter)

    def get_protocols(self):
        return ["ImageProtocol0203",]