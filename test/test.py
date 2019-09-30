# coding:utf-8
# coding:utf-8
import logging
from logging.handlers import RotatingFileHandler  # 按文件大小滚动备份
import time
import datetime
import os
import requests
from fake_useragent import UserAgent

cur_path = os.path.dirname(os.path.realpath(__file__))  # log_path是存放日志的路径
log_path = os.path.join(os.path.dirname(cur_path), 'logs')
if not os.path.exists(log_path): os.mkdir(log_path)  # 如果不存在这个logs文件夹，就自动创建一个
logName = os.path.join(log_path, '%s.log' % time.strftime('%Y-%m-%d'))  # 文件的命名

log_colors_config = {
    'DEBUG': 'cyan',
    'INFO': 'green',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'red',
}

if __name__ == "__main__":
    headers = {'User-Agent': UserAgent().random, 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*',
               'Connection': 'keep-alive'}

    session = requests.Session()
    session.headers = headers

    print(session.cookies.get_dict())
    res = session.get('https://www.12306.cn/index/', headers=headers)
    print(session.cookies.get_dict())
    print(session.headers)
