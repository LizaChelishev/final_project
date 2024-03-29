import datetime
import logging
import threading
from datetime import datetime
from configparser import ConfigParser


class Logger:
    _instance = None
    _lock = threading.Lock()
    config = ConfigParser()
    config.read("config.conf")
    LOG_LEVEL = config["logging"]["level"]
    LOG_FILE_NAME_PREFIX = config["logging"]["logfile_name_prefix"]
    LOG_FILE_NAME_EXT = config["logging"]["logfile_name_ext"]
    today = datetime.today()
    day = f'{today.year:02d}-{today.month:02d}-{today.day:02d}'
    filename = f'{LOG_FILE_NAME_PREFIX}-{day}.{LOG_FILE_NAME_EXT}'

    def __init__(self):
        raise RuntimeError('Try using instance!')

    @classmethod
    def get_instance(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = cls.__new__(cls)
                for handler in logging.root.handlers:
                    logging.root.removeHandler(handler)
                cls._instance.logger = logging.getLogger(__name__)
                cls._instance.logger.setLevel(logging.__dict__[cls.LOG_LEVEL])
                cls._instance.formatter = logging.Formatter(
                    f'%(asctime)s:%(module)s:%(levelname)s:%(message)s')
                cls._instance.file_handler = logging.FileHandler(
                    Logger.filename)
                cls._instance.file_handler.setLevel(
                    logging.__dict__[cls.LOG_LEVEL])
                cls._instance.file_handler.setFormatter(
                    cls._instance.formatter)
                cls._instance.logger.addHandler(cls._instance.file_handler)
            return cls._instance

    def __str__(cls):
        return f'Log file-name: {cls.filename}'


def print_to_log(logger, level, msg):
    logger.log(level, f'{datetime.datetime.now()} {logging.getLevelName(level)} {msg}')
