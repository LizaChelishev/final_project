import datetime
import logging
from configparser import ConfigParser
import threading


def init_logger():
    for handler in logging.root.handlers:
        logging.root.removeHandler(handler)

    logging.basicConfig(level='DEBUG')
    file_handler = logging.FileHandler("logfile.log")
    file_handler.setLevel(logging.DEBUG)
    logger = logging.getLogger()
    logger.addHandler(file_handler)

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
                cls._instance.file_handler = logging.FileHandler(
                    f'{logging.Logger.LOG_FILE_NAME_PREFIX}.{logging.Logger.LOG_FILE_NAME_EXT}')
                cls._instance.file_handler.setLevel(logging.__dict__[cls.LOG_LEVEL])
                cls._instance.file_handler.setFormatter(cls._instance.formatter)
                cls._instance.logger.addHandler(cls._instance.file_handler)

                return cls._instance
            else:
                return cls._instance


def print_to_log(logger, level, msg):
    logger.log(level, f'{datetime.datetime.now()} {logging.getLevelName(level)} {msg}')
