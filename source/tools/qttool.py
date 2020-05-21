from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui, QtWidgets


def display_jpgdata(image_label, jpg_data):
    image = QImage.fromData(jpg_data)
    pixelmap = QPixmap.fromImage(image)
    image_label.setPixmap(pixelmap)
    image_label.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)