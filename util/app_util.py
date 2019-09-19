# coding:utf-8

import os
import time

project_name = "12306"


def get_root_path():
    """获取项目根路径"""
    current_path = os.path.abspath(os.path.dirname(__file__))
    return current_path[:current_path.find(project_name) + len(project_name)]


def timestamp():
    return int(round(time.time() * 1000))


if __name__ == '__main__':
    print(get_root_path())
    print(timestamp())
