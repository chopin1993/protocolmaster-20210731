# encoding:utf-8
import os
from PyQt5.QtCore import QObject, pyqtSignal
import pickle
from copy import deepcopy
from register import Register

class MediaOptions(object):
    def __init__(self, key, options, label_text=None, show_options=None,select_id=0):
        self.key = key
        self.options = options
        self.select_id = select_id
        if label_text is None:
            label_text = key
        if show_options is None:
            show_options = options
        self.label_text = label_text
        self.show_options = show_options

    def get_options(self):
        return [str(i) for i in self.show_options]

    def get_selected_key_value(self):
        if 0 <= self.select_id < len(self.options):
            return self.key, self.options[self.select_id]

    def load_save_value(self, saved):
        if self.options == saved.options:
            self.select_id = saved.select_id

    def set_value(self, value):
        for i,option in enumerate(self.get_options()):
            if option == value:
                self.select_id = i
                return
        raise ValueError("only support {0},but get {1}".format(self.get_options(), value))


class MediaText(object):
    def __init__(self, key, value, label_text=None, func=None):
        self.key = key
        self.value = value
        if label_text is None:
            label_text = key
        self.label_text = label_text
        self.func = func

    def get_options(self):
        return str(self.value)

    def get_selected_key_value(self):
        return self.key, self.value

    def load_save_value(self, saved):
        self.value = saved.value

    def set_value(self, option):
        self.value = option


class Media(QObject, Register):
    data_ready = pyqtSignal(bytes)
    error = pyqtSignal(str)
    media_instance = {}

    def __init__(self, media_options):
        super(Media, self).__init__()
        self.media_options = media_options
        self.pickle_file_name = ".config_" + self.__class__.__name__ + ".pkl"
        self.load_saved_options()

    def load_saved_options(self):
        if os.path.exists(self.pickle_file_name):
            with open(self.pickle_file_name, 'rb') as handle:
                media_options = pickle.load(handle)
            for current, last in zip(self.media_options, media_options):
                current.load_save_value(last)

    def is_open(self):
        pass

    def open(self):
        pass

    def close(self):
        pass

    def send(self, data):
        pass

    def _receive(self):
        pass

    def refresh_media_options(self):
        pass

    def set_media_options(self, options):
        self.media_options = options
        with open(self.pickle_file_name, 'wb') as handle:
            pickle.dump(options, handle)

    def get_media_options(self):
        self.refresh_media_options()
        return self.media_options

    def get_selected_options(self):
        selected_options = {}
        for option in self.media_options:
            key, value = option.get_selected_key_value()
            selected_options[key] = value
        return selected_options

    def config(self, **kwargs):
        options = self.get_media_options()
        def sync_options(key,value):
            nonlocal options
            for option in options:
                if key == option.key:
                    option.set_value(value)
                    return
            raise TypeError("{0} is not supported".format(key))
        for key,value in kwargs.items():
            sync_options(key, value)
        return self.set_media_options(options)
