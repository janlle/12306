# coding:utf-8

import logging
from util.app_util import get_root_path


formatter = "%(asctime)s %(levelname)-9s %(process)-5d [line:%(lineno)3d]: %(message)s"
log_path = get_root_path() + "/tickets.log"


class Logger(object):
    def __init__(self, name):
        self.f = logging.Formatter(formatter)
        # 创建一个屏幕输出流
        ch = logging.StreamHandler()

        # 创建一个文件输出流
        fh = logging.FileHandler(log_path)

        ch.setFormatter(self.f)
        fh.setFormatter(self.f)

        self.logger = logging.getLogger(name)
        self.logger.addHandler(ch)
        self.logger.addHandler(fh)
        self.logger.setLevel(logging.DEBUG)

    def info(self, message):
        self.logger.info(message)

    def critical(self, message):
        self.logger.critical(message)

    def debug(self, message):
        self.logger.debug(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)


if __name__ == '__main__':
    log = Logger(__name__)
    log.debug("hello info")
    log.info("hello info")
    log.error("hello info")
    log.warning("hello info")
    log.critical("hello info")
