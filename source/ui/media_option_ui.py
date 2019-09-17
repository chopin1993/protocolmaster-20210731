# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui
from media.media import MediaOptions,MediaText
from PyQt5.QtWidgets import *

class EsUserOptionsDialog(QDialog):
    def __init__(self):
        super(EsUserOptionsDialog, self).__init__()
        self.options = []
        self.setModal(True)
        self.ok_func = None
        self.close_func = None
        self.vlayout = None
        self.group_widget =None
        self.widget_list =[]

    def setup_ui(self):
        #self.resize(237, 298)
        self.vlayout = QVBoxLayout()
        self.vlayout.setSpacing(20)
        self.config_groups = QGroupBox(self.group_widget)
        self.config_layout = QGridLayout(self.config_groups)
        self.config_layout.setHorizontalSpacing(20)
        self.config_layout.setVerticalSpacing(10)

        for i,option in enumerate(self.options):
            if isinstance(option, MediaOptions):
                combobox = QComboBox(self.config_groups)
                combobox.addItems(option.get_options())
                combobox.setCurrentIndex(option.select_id)
                self.widget_list.append(combobox)
                self.config_layout.addWidget(combobox, i, 1, 1, 1)
                label = QLabel(self.config_groups)
                size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
                size_policy.setHorizontalStretch(0)
                size_policy.setVerticalStretch(0)
                size_policy.setHeightForWidth(label.sizePolicy().hasHeightForWidth())
                label.setSizePolicy(size_policy)
                label.setText(option.label_text)
                self.config_layout.addWidget(label, i, 0, 1, 1)
            elif isinstance(option, MediaText):
                line_edit = QLineEdit(self.config_groups)
                line_edit.setText(option.get_options())
                self.widget_list.append(line_edit)
                self.config_layout.addWidget(line_edit, i, 1, 1, 1)
                label = QLabel(self.config_groups)
                size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
                size_policy.setHorizontalStretch(0)
                size_policy.setVerticalStretch(0)
                size_policy.setHeightForWidth(label.sizePolicy().hasHeightForWidth())
                label.setSizePolicy(size_policy)
                label.setText(option.label_text)
                self.config_layout.addWidget(label, i, 0, 1, 1)
            else:
                assert False,"unhandle class"

        self.vlayout.addWidget(self.config_groups)
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Open|QDialogButtonBox.Close)
        self.vlayout.addWidget(self.buttonBox)
        self.setLayout(self.vlayout)

    def set_options(self, options):
        self.options = options
        self.setup_ui()
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.clicked.connect(self.close)

    def set_ok_function(self, func):
        self.ok_func = func

    def set_close_function(self,func):
        self.close_func = func

    def accept(self):
        if self.ok_func is not None:
            self.ok_func(self.get_user_options())
        self.hide()

    def reject(self):
        self.hide()

    def close(self):
        if self.close_func is not None:
            self.close_func()
        self.hide()

    def get_user_options(self):
        for i, widget in enumerate(self.widget_list):
            if isinstance(self.options[i], MediaOptions):
                self.options[i].select_id = widget.currentIndex()
            elif isinstance(self.options[i], MediaText):
                self.options[i].value = str(widget.text())
        return self.options

dialog = None


def show_user_media_options(media):
    global dialog

    def ok_button_press(options):
        if media.set_media_options(options):
            dialog.hide()
        else:
            QMessageBox.information(dialog, u"错误", u"打开错误，请检查资源是否被占用")

    def close_button_press():
        media.close()

    dialog = EsUserOptionsDialog()
    dialog.setModal(True)
    dialog.set_options(media.get_media_options())
    dialog.set_ok_function(ok_button_press)
    dialog.set_close_function(close_button_press())
    dialog.show()


def show_user_options(options, ok_func):
    global dialog
    dialog = EsUserOptionsDialog()
    dialog.setModal(True)
    dialog.set_options(options)
    dialog.set_ok_function(ok_func)
    dialog.show()

