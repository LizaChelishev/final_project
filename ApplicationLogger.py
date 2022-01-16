import datetime
import logging
import datetime as dt


def init_logger():
    for handler in logging.root.handlers:
        logging.root.removeHandler(handler)

    logging.basicConfig(level='DEBUG')
    file_handler = logging.FileHandler("logfile.log")
    file_handler.setLevel(logging.DEBUG)
    logger = logging.getLogger()
    logger.addHandler(file_handler)


def print_to_log(logger, level, msg):
    logger.log(level, f'{datetime.datetime.now()} {logging.getLevelName(level)} {msg}')
