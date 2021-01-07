import logging

def root_logging():
    logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s', level=logging.DEBUG)
    logging.info("this issssss my debug")
    logging.error("sssss")


def multi_logger():
    format = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    stream = logging.StreamHandler()
    stream.setFormatter(format)

    file_log = logging.FileHandler("stream.txt")
    file_log.setFormatter(format)
    root.addHandler(file_log)
    root.addHandler(stream)
    logging.info("hello world logging")

    modle1 = logging.getLogger("monitor")
    file_log2 = logging.FileHandler("monitor.txt")
    modle1.addHandler(file_log2)
    modle1.propagate =False
    modle1.info("monitor 2 log")


def eslogging():
    from tools.esloging import log_init
    log_init(".")
    logging.info("hello world")
    logger =  logging.getLogger("被测设备")
    logger.info("被测设备， hellwrold")

    logger =  logging.getLogger()
    logger.info("default， hellwrold")

    logger  = logging.getLogger("测试工装")
    logger.info("测试工装， hellwrold")
if __name__ == "__main__":
    #root_logging()
    #test_multi_logger()
    eslogging()