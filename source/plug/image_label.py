from .application_plug import plug_register, ApplicationPlug
from .image_label_ui import Ui_Form
from tools.imgtool import numpy2jpg
from tools.qttool import display_jpgdata
import numpy as np

def handle_img(data):
    #base_temperature = data.
    return data

@plug_register
class ImageLabel(Ui_Form, ApplicationPlug):
    def __init__(self):
        super(ImageLabel, self).__init__("data label")
        self.setupUi(self)

    def playbutton_clicked(self):
        data, img = self.database.get_first_sample_by_sql("select data,img from thermal_table where rowid==888")
        data = np.frombuffer(data, dtype=np.float32)
        data = data.reshape((24,32))
        display_jpgdata(self.rawDataLabel, img)
        display_jpgdata(self.resultDataLabel, numpy2jpg(data))