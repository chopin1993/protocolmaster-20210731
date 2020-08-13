# encoding:utf-8

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
        super(ThermalImage, self).__init__("红外阵列90240数据收集")
        self.setupUi(self)
        self.layout_image = QtWidgets.QVBoxLayout(self.image)
        self.image_label = QLabel()
        self.layout_image.addWidget(self.image_label)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.readImageOnce)
        self.rcv_cnt = 0
        self.send_cnt = 0
        self.previous_time = datetime.datetime.now()
        self.refresh_timer = QTimer(self)
        self.refresh_timer.timeout.connect(self.show_next_img_in_db)
        self.data_src = None

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
        self.rcv_cnt += 1
        numpy = np.copy(msg.image_data.data)
        jpg_data = numpy2jpg(numpy)
        self.database.append_sample(msg.idx,self.tagLineEdit.text(),"rcv",msg.image_data.data, jpg_data)
        self._show_numpy(numpy)

    def _show_numpy(self, data):
        jpg_data = numpy2jpg(data)
        image = QImage.fromData(jpg_data)
        pixelmap = QPixmap.fromImage(image)
        self.image_label.setPixmap(pixelmap)
        self.image_label.setAlignment(QtCore.Qt.AlignTop |QtCore.Qt.AlignHCenter)

    def media_error_happen(self):
        self.timer.stop()

    def playImage(self):
        self.data_src = self.database.get_sample_images()
        self.refresh_timer.start(300)

    def show_next_img_in_db(self):
        try:
            datas = next(self.data_src)
            if datas is not None:
                img = datas[3]
                data = np.frombuffer(img, dtype=np.float32)
                data = data.reshape(24, 32)
                self._show_numpy(data)
        except StopIteration:
            self.refresh_timer.stop()
            QMessageBox.information(None,"信息","数据播放完毕")

    def searchImage(self):
        pass