# coding:utf-8

import logging
import os
import time

from util.app_util import get_root_path


class Logger:
    def __init__(self, log_level="INFO", name='12306', log_name=time.strftime("%Y-%m-%d.log", time.localtime()),
                 log_path=get_root_path(), stdout=True):
        """
        :param log_level: 日志级别["NOTSET"|"DEBUG"|"INFO"|"WARNING"|"ERROR"|"CRITICAL"]，默认为INFO
        :param name: 日志中打印的name，默认为运行程序的name
        :param log_name: 日志文件的名字，默认为当前时间（年-月-日.log）
        :param log_path: 日志文件夹的路径，默认为logger.py同级目录中的log文件夹
        :param stdout: 是否在控制台打印，默认为True
        """

        self.__logger = logging.getLogger(name)
        self.setLevel(
            getattr(logging, log_level.upper()) if hasattr(logging, log_level.upper()) else logging.INFO)  # 设置日志级别
        # 创建日志目录
        if not os.path.exists(log_path):
            os.makedirs(log_path)

        if not self.handlers:
            formatter = logging.Formatter(
                "%(asctime)s %(levelname)-8s %(process)-5d - %(filename)-16s[line:%(lineno)3d]: %(message)s")
            handler_list = [logging.FileHandler(os.path.join(log_path, log_name), encoding="utf-8")]
            if stdout:
                handler_list.append(logging.StreamHandler())

            for handler in handler_list:
                handler.setFormatter(formatter)
                self.addHandler(handler)

    def __getattr__(self, item):
        return getattr(self.logger, item)

    @property
    def logger(self):
        return self.__logger

    @logger.setter
    def logger(self, func):
        self.__logger = func


if __name__ == '__main__':
    log = Logger('debug')
    log.debug("hello debug")
    log.info("hello info")
    log.error("hello error")
    log.warning("hello warning 日志")
    log.critical("hello critical")
