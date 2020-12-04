import logging


def log_init():
    format = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    stream = logging.StreamHandler()
    stream.setFormatter(format)

    plc_logger = logging.FileHandler("抄控器.txt")
    plc_logger.setFormatter(format)
    root.addHandler(plc_logger)
    root.addHandler(stream)

    test_machine = logging.getLogger("测试工装")
    machine_log = logging.FileHandler("测试工装.txt")
    test_machine.addHandler(machine_log)
    test_machine.propagate =False

    device_under_test = logging.getLogger("被测设备")
    device_log = logging.FileHandler("被测设备.txt")
    device_under_test.addHandler(device_log)
    device_under_test.propagate = False

log_init()
