import datetime
import logging
from configparser import ConfigParser
import threading


class Logger:
    _instance = None
    _lock = threading.Lock()

    config = ConfigParser()
    config.read("config.conf")
    LOG_LEVEL = config["logging"]["level"]
    LOG_FILE_NAME_PREFIX = config["logging"]["logfile_name_prefix"]
    LOG_FILE_NAME_EXT = config["logging"]["logfile_name_ext"]

    def __init__(self):
        self.file_handler = None
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.getLevelName(Logger.LOG_LEVEL))
        formatter = logging.Formatter('%(asctime)s - %(name)s%(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S%p')
        file_handler = logging.FileHandler('logFile.log')
        file_handler.setFormatter(formatter)
        stream_handler = logging.StreamHandler() #if we want to print to consol
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(stream_handler)
        raise RuntimeError('Call instance() instead')

    @classmethod
    def get_instance(cls):
        if cls._instance:
            return cls._instance
        with cls._lock:
            if cls._instance is None:
                cls._instance = cls.__new__(cls)
                for handler in logging.root.handlers:
                    logging.root.removeHandler(handler)
                cls._instance.logger = logging.getLogger(__name__)
                cls._instance.logger.setLevel(logging.__dict__[cls.LOG_LEVEL])
                cls._instance.formatter = logging.Formatter(
                    f'%(asctime)s:%(module)s:%(process)d:%(thread)d:%(levelname)s:%(message)s')
                cls._instance.file_handler.setLevel(logging.__dict__[cls.LOG_LEVEL])
                cls._instance.file_handler.setFormatter(cls._instance.formatter)
                cls._instance.logger.addHandler(cls._instance.file_handler)

                return cls._instance
            else:
                return cls._instance


def print_to_log(logger, level, msg):
    logger.log(level, f'{datetime.datetime.now()} {logging.getLevelName(level)} {msg}')
