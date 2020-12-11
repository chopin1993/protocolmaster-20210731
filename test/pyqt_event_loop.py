from PyQt5.QtCore import QTimer,QObject,QEvent
from PyQt5.QtCore import QCoreApplication
import time
import sys

start_t = None

app = QCoreApplication(sys.argv)



class EventHandler(QObject):
    def __init__(self):
        super(EventHandler, self).__init__()
        
    def event(self, a0: 'QEvent') -> bool:
        print(a0)
        return True


class MyEvent(QEvent):
    def __init__(self, ids=10000):
        super(MyEvent,self).__init__(QEvent.User+10)
        self.idx = ids

    def __str__(self):
        return "my event" + str(self.idx)

if __name__ == "__main__":
    handler = EventHandler()
    QCoreApplication.postEvent(handler, MyEvent(1))
    QCoreApplication.postEvent(handler, MyEvent(2))
    while True:
        QCoreApplication.instance().processEvents()