import logging
from const import LOG


class LoggerClass(object):

    log = None

    def __init__(self):
        # create logger
        dir = logging.FileHandler(LOG)  # %I:%M:%S
        # create a logging format
        formatter = logging.Formatter('%(asctime)s - %(filename)s.%(funcName)s:%(lineno)s - %(levelname)s - %(message)s')
        # add formatter to dir
        dir.setFormatter(formatter)
        log = logging.getLogger('allegro_project')
        log.setLevel(logging.DEBUG)
        log.addHandler(dir)
        # create a file handler
        log.info('Logging start recording...')
        self.log = log

    @staticmethod
    def getLogger():
        if LoggerClass.log is None:
            LoggerClass.log = LoggerClass().log
        return LoggerClass.log


log = LoggerClass.getLogger()
