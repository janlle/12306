# coding:utf-8

import os
import time
import datetime
import re
import urllib
import locale

project_name = "12306"
GMT_FORMAT = '%a %b %d %Y %H:%M:%S GMT+0800 (中国标准时间)'
locale.setlocale(locale.LC_CTYPE, 'chinese')


def get_root_path():
    """获取项目根路径"""
    current_path = os.path.abspath(os.path.dirname(__file__))
    return current_path[:current_path.find(project_name) + len(project_name)]


def timestamp():
    return int(round(time.time() * 1000))


def current_hour():
    return datetime.datetime.now().hour


def current_date():
    return datetime.datetime.now().strftime('%y-%m-%d')


def check_date(text):
    match = re.compile(r'^\d{4}-\d{1,2}-\d{1,2}$').match(text)
    if match:
        return match.group() is not None
    else:
        return False


def decode_secret_str(code):
    return urllib.parse.unquote(code).replace('\n', '')


def get_gmt_time(text):
    """
    Fri Oct 025 2019 00:00:00 GMT+0800 (中国标准时间)
    Sun Oct 06 2019 00:00:00 GMT+0800 (中国标准时间)
    :param text:
    :return:
    """
    return datetime.datetime.strptime(text, '%Y-%m-%d').strftime(GMT_FORMAT)


if __name__ == '__main__':
    print(timestamp())
