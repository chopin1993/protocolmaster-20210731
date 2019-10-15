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
        self.axes.axis('off')
        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.cb = None

    def imshow(self,img):
        im = self.axes.imshow(img,vmin=15, vmax=38)
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