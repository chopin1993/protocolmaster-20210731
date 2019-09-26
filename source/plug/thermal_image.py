# encoding:utf-8

from .application_plug import plug_register,ApplicationPlug
from .thermal_image_ui import Ui_Form
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import random
from PyQt5.QtWidgets import *
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer
import datetime

class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        self.axes.axis('off')
        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.cb = None

    def imshow(self,img):
        im = self.axes.imshow(img,vmin=20, vmax=38)
        if self.cb is None:
            self.cb = self.fig.colorbar(im, shrink=0.5)
        self.draw()

    def clear_img(self):
        pass
        #self.axes.clear()
        #self.axes.axis('off')
        #if self.cb is not None:
            #self.cb.remove()
        #self.draw()



@plug_register
class ThermalImage(ApplicationPlug, Ui_Form):

    def __init__(self):
        super(ThermalImage, self).__init__("红外阵列90240")
        self.setupUi(self)
        self.layout_image = QtWidgets.QVBoxLayout(self.image)
        self.plot_image = PlotCanvas(self.image)
        self.layout_image.addWidget(self.plot_image)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.readImageOnce)
        self.rcv_cnt = 0
        self.send_cnt = 0
        self.previous_time = datetime.datetime.now()
        self.fresh_timer = QTimer(self)
        self.fresh_timer.timeout.connect(self.refresh_timer_handle)
        self.imges = []
        self.fresh_timer.start(250)

    def refresh_timer_handle(self):
        if len(self.imges) > 0:
            img = self.imges[-1]
            self.imges.clear()
            self.plot_image.imshow(img)

    def readImageOnce(self):
        self.send_cnt += 1
        now  = datetime.datetime.now()
        print("snd:" ,now - self.previous_time , self.send_cnt)
        self.session.write(bytes([0x30]))
        self.previous_time = now
        self.plot_image.clear_img()

    def startRead(self):
        self.timer.start(int(self.timespanLineeidt.text()))

    def stopRead(self):
        self.timer.stop()

    def handle_receive_data(self, msg):
        self.imges.append(msg.image_data)
        self.rcv_cnt += 1
        print("rcv:",(self.send_cnt, self.rcv_cnt))
        #self.readImageOnce()

