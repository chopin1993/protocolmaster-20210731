# encoding:utf-8
from abc import ABC

from .application_plug import plug_register,ApplicationPlug
from .thermal_image_ui import Ui_Form
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer
import datetime
from database import EsDatabase
from tools.imgtool import numpy2jpg


@plug_register
class ThermalImage(ApplicationPlug, Ui_Form):

    def __init__(self):
        super(ThermalImage, self).__init__("红外阵列90240")
        self.setupUi(self)
        self.layout_image = QtWidgets.QVBoxLayout(self.image)
        self.image_label = QLabel()
        self.layout_image.addWidget(self.image_label)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.readImageOnce)
        self.rcv_cnt = 0
        self.send_cnt = 0
        self.previous_time = datetime.datetime.now()
        self.imges = []
        self.database = EsDatabase("image.db")

    def readImageOnce(self):
        self.send_cnt += 1
        now  = datetime.datetime.now()
        # print("snd:" ,now - self.previous_time , self.send_cnt)
        self.session.write(bytes([0x30]))
        self.previous_time = now

    def startRead(self):
        self.timer.start(int(self.timespanLineeidt.text()))

    def stopRead(self):
        self.timer.stop()

    def handle_receive_data(self, msg):
        self.imges.append(msg.image_data)
        #print(msg.image_data)
        self.rcv_cnt += 1
        jpg_data = numpy2jpg(np.copy(msg.image_data.data))
        self.database.append_sample(msg.idx,self.tagLineEdit.text(),"rcv",msg.image_data.data, jpg_data)
        image = QImage.fromData(jpg_data)
        pixmap = QPixmap.fromImage(image)
        self.image_label.setPixmap(pixmap)
        self.image_label.setAlignment(QtCore.Qt.AlignCenter)
        #print("rcv:",(self.send_cnt, self.rcv_cnt))
        #self.readImageOnce()

    def media_error_happen(self):
        self.timer.stop()
