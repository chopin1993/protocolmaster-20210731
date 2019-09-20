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

    def imshow(self,img):
        self.axes.imshow(img)
        self.draw()

    def clear_img(self):
        self.axes.clear()
        self.axes.axis('off')
        self.draw()


@plug_register
class ThermalImage(ApplicationPlug, Ui_Form):

    def __init__(self):
        super(ThermalImage, self).__init__("红外阵列90240")
        self.setupUi(self)
        self.layout_image =  QtWidgets.QVBoxLayout(self.image)
        self.plot_image = PlotCanvas(self.image)
        self.layout_image.addWidget(self.plot_image)

    def readImageOnce(self):
        self.session.write(bytes("1124324324",encoding='utf8'))
        self.plot_image.clear_img()

    def handle_receive_data(self, msg):
        self.plot_image.imshow(msg.image_data)
        print(msg.image_data)