import logging
import os

def log_init(path):
    format = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
    root = logging.getLogger()
    add_handlers = []
    for handle in root.handlers:
        if isinstance(handle, logging.StreamHandler) or isinstance( handle,logging.FileHandler):
            pass
        else:
            add_handlers.append(handle)
    root.handlers.clear()
    root.handlers.extend(add_handlers)
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

    device_raw = logging.getLogger("被测设备.raw")
    device_raw.handlers.clear()
    device_raw_logger = logging.FileHandler(os.path.join(path,"被测设备_raw.txt"), encoding="utf-8")
    device_raw_logger.setFormatter(format)
    device_raw.addHandler(device_raw_logger)
    device_raw.propagate = False


    ignore_logger = logging.getLogger("ignore")
    ignore_logger.handlers.clear()
    ignore_file = logging.FileHandler(os.path.join(path,"ignore.txt"), encoding="utf-8")
    ignore_file.setFormatter(format)
    ignore_logger.addHandler(ignore_file)
    ignore_logger.propagate = False

