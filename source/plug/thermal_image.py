# encoding:utf-8

from .application_plug import plug_register,ApplicationPlug
from .thermal_image_ui import Ui_Form
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import random
from PyQt5.QtWidgets import *


class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def imshow(self,img):
        self.axes.imshow(img)
        self.draw()


@plug_register
class ThermalImage(ApplicationPlug, Ui_Form):

    def __init__(self):
        super(ThermalImage, self).__init__("红外阵列90240")
        self.setupUi(self)
        self.sender_image = PlotCanvas(self.image)

    def readImageOnce(self):
        self.session.write(bytes("1124324324",encoding='utf8'))
        print("read image once")

    def handle_receive_data(self, msg):
        self.sender_image.imshow(msg.image_data)