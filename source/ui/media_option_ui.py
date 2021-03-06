# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui
from media.media import MediaOptions,MediaText
from PyQt5.QtWidgets import *


class EsUserOptionsDialog(QWidget):
    def __init__(self, data=None):
        super(EsUserOptionsDialog, self).__init__()
        self.options = []
        self.ok_func = None
        self.close_func = None
        self.vlayout = None
        self.group_widget =None
        self.widget_list =[]
        self.data = data

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
            self.ok_func(self.data, self.get_user_options())
        self.hide()

    def reject(self):
        self.hide()

    def close(self):
        if self.close_func is not None:
            self.close_func(self.data)
        self.hide()

    def get_user_options(self):
        for i, widget in enumerate(self.widget_list):
            if isinstance(self.options[i], MediaOptions):
                self.options[i].select_id = widget.currentIndex()
            elif isinstance(self.options[i], MediaText):
                self.options[i]._value = str(widget.text())
        return self.options

dialog = None


class TabsDialog(QDialog):
    def __init__(self):
        super(TabsDialog, self).__init__()
        self.layout = QVBoxLayout()
        self.tabWidgt = QTabWidget()
        self.setLayout(self.layout)
        self.layout.addWidget(self.tabWidgt)

    def add_tabs(self,tabs):
        for tab in tabs:
            self.tabWidgt.addTab(tab, tab.name)


def show_user_media_options(medias, ok_func=None):
    global dialog

    dialog = TabsDialog()
    dialog.setModal(True)
    media_uis = []

    for media in medias:
        def ok_button_press(media, options):
            if media.set_media_options(options):
                if ok_func is not None:
                    ok_func(media)
                dialog.hide()
            else:
                QMessageBox.information(dialog, u"??????", u"?????????????????????????????????????????????")

        def close_button_press(media):
            media.close()
            dialog.hide()

        widgit = EsUserOptionsDialog(media)
        widgit.set_options(media.get_media_options())
        widgit.name = media.name
        widgit.set_ok_function(ok_button_press)
        widgit.set_close_function(close_button_press)
        media_uis.append(widgit)

    dialog.add_tabs(media_uis)
    dialog.show()


def show_user_options(options, ok_func):
    global dialog

    def ok_button_press(protocol, options):
            dialog.close()

    def close_button_press(media):
        dialog.hide()

    dialog = QDialog()
    layout = QVBoxLayout()
    dialog.setLayout(layout)
    widget = EsUserOptionsDialog()
    layout.addWidget(widget)
    dialog.setModal(True)
    widget.set_options(options)
    widget.set_ok_function(ok_button_press)
    widget.set_close_function(close_button_press)
    dialog.show()

