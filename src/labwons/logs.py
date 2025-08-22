from labwons.path import PATH
from labwons.util import DATETIME
import logging, os, time


def create_logger(file:str):
    def kst(*args):
        return time.localtime(time.mktime(time.gmtime(*args)) + 9 * 3600)

    name = os.path.basename(file).split("_")[0]

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    formatter = logging.Formatter(f"[{name.upper()}] %(asctime)s [%(levelname)s] %(message)s")
    formatter.converter = kst

    file_handler = logging.FileHandler(file, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger


os.makedirs(os.path.join(PATH.LOGS), exist_ok=True)
build_logger = create_logger(os.path.join(PATH.LOGS, rf'build_{DATETIME.TODAY}.log'))
fetch_logger = create_logger(os.path.join(PATH.LOGS, rf'fetch_{DATETIME.TODAY}.log'))
