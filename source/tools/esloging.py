import logging
import os

def log_init(path):
    format = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
    root = logging.getLogger()
    for handle in root.handlers:
        if isinstance(handle, logging.StreamHandler) or isinstance( handle,logging.FileHandler):
            root.removeHandler(handle)
    root.setLevel(logging.DEBUG)

    stream = logging.StreamHandler()
    stream.setFormatter(format)
    root.addHandler(stream)

    plc_logger = logging.FileHandler(os.path.join(path,"抄控器.txt"), encoding="utf-8")
    plc_logger.setFormatter(format)
    root.addHandler(plc_logger)

    root.propagate = False

    test_machine = logging.getLogger("测试工装")
    test_machine.handlers.clear()
    machine_log = logging.FileHandler(os.path.join(path,"测试工装.txt"), encoding="utf-8")
    machine_log.setFormatter(format)
    test_machine.addHandler(machine_log)
    test_machine.propagate =False

    device_under_test = logging.getLogger("被测设备")
    device_under_test.handlers.clear()
    device_log = logging.FileHandler(os.path.join(path,"被测设备.txt"), encoding="utf-8")
    device_log.setFormatter(format)
    device_under_test.addHandler(device_log)
    device_under_test.propagate = False

