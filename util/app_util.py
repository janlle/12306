# coding:utf-8

import os

project_name = "12306"


def get_root_path():
    """获取项目根路径"""
    current_path = os.path.abspath(os.path.dirname(__file__))
    return current_path[:current_path.find(project_name) + len(project_name)]


if __name__ == '__main__':
    print(get_root_path())
