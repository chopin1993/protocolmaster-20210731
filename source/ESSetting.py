from PyQt5.QtCore import QSettings


class ESSetting(object):
    SELECTED_PLUG_KEY = "selected_plug"
    SELECTED_MEDIA_KEY = "selected_media"
    _instance = None
    @staticmethod
    def instance():
        if ESSetting._instance is None:
            ESSetting._instance = ESSetting()
        return ESSetting._instance

    def __init__(self):
        self.setting = QSettings("Eastsoft", "ProtocolMaster")

    def get_plug_idx(self):
        return self.setting.value(self.SELECTED_PLUG_KEY,0)

    def set_plug_idx(self, idx):
        self.setting.setValue(self.SELECTED_PLUG_KEY, idx)
        self.setting.sync()

    def get_media_key(self, default=None):
        value = self.setting.value(self.SELECTED_MEDIA_KEY, "")
        if value is "":
            self.setting.setValue(self.SELECTED_MEDIA_KEY, default)
            self.setting.sync()
            return default
        return value

    def set_media_key(self, value):
        self.setting.setValue(self.SELECTED_MEDIA_KEY, value)
        self.setting.sync()