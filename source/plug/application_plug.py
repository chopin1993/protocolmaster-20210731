import os
from tools.import_helper import import_all_python
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class ApplicationPlug(QWidget):

    def __init__(self, name):
        super(QWidget, self).__init__()
        self.name = name

    def get_medias_cnt(self):
        raise NotImplementedError

    def get_protocols(self):
         raise NotImplementedError

    def handle_receive_data(self):
        pass

    def handle_send_data(self):
        pass


_all_plugs = dict()


def plug_register(plugs_class):
    global _all_plugs
    _all_plugs[plugs_class.__name__] = plugs_class
    return plugs_class


def plugs_get_all():
    plugs = list()
    for value in _all_plugs.values():
        plugs.append(value())
    return plugs


#
# def import_device_list(self):
#     file_name = QFileDialog.getOpenFileName(directory=ESConfig.get_instance().get_device_file())
#     file_name = unicode(file_name.toUtf8(), 'utf-8', 'ignore')
#     ESConfig.get_instance().set_device_file(file_name)
#     self.devices = get_all_device(file_name)
#     self.sync_device_to_ui()
#
# def sync_device_to_ui(self):
#     devices = self.devices
#     self.tableWidget.setRowCount(len(devices))
#     for i, device in enumerate(devices):
#         widget = QTableWidgetItem(device.get_hex_string_address())
#         self.tableWidget.setItem(i, 0, widget)
#         device.device_update.connect(self.sync_status_to_ui)
#     self.send_idx = 0
#
# def sync_status_to_ui(self):
#     for i, device in enumerate(self.devices):
#         widget = QTableWidgetItem(device.get_summary())
#         self.tableWidget.setItem(i, 1, widget)
#
# def read_next_device(self):
#     device = self.devices[self.send_idx]
#     device.add_send_count()
#     self.send_idx += 1
#     self.send_idx %= len(self.devices)
#     self.sync_status_to_ui()
#     if self.protocol_idx == PROTOL_645_07:
#         self.session.send_data(hexstr2str(str(self.convertAddressLineEdit.text())), DIDRealTimeMeterData(device.address))
#     elif self.protocol_idx == PROTOL_188:
#         self.session.send_data(device.address, DIDReadMeter())
#     elif self.protocol_idx == PROTOL_645_97:
#         protocol = CJT188Protocol.create_frame(device.address,DIDReadMeter())
#         data = BinaryEncoder.object2data(protocol)
#         self.session.send_data(hexstr2str(str(self.convertAddressLineEdit.text())), DIDESTunnelData(data))
#