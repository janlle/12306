# coding:utf-8

import os
import time
import datetime
import re
import urllib

project_name = "12306"


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


if __name__ == '__main__':
    print(check_date('2020-02-26'))
