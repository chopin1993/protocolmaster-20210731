from PyQt5.QtCore import QTimer
from PyQt5.QtCore import QCoreApplication
import time
import sys

start_t = None

app = QCoreApplication(sys.argv)

def timetout():
    print("real time",time.time() - start_t)

def qttest_timer():
    global start_t
    timer = QTimer()
    timer.setSingleShot(True)
    timer.timeout.connect(timetout)
    start_t = time.time()
    timer.start(1000)
    while True:
        QCoreApplication.instance().processEvents()


qttest_timer()