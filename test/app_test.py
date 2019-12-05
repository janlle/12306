# coding:utf-8

from train.logger import Logger

log = Logger('debug')

if __name__ == "__main__":

    log.info("info")
    log.debug("debug")
    log.warning("warning")
    log.error("error")
    # log.error("error")
    # logging.error("hello")

    for i in range(10):
        if i == 5:
            log.info('hello')
