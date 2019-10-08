# coding:utf-8
# coding:utf-8
import logging
from logging.handlers import RotatingFileHandler  # 按文件大小滚动备份
import time
import datetime
import os
import requests
from fake_useragent import UserAgent
from urllib import request
from urllib import parse
from http import cookiejar
from util.net_util import *


log_colors_config = {
    'DEBUG': 'cyan',
    'INFO': 'green',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'red',
}


def cookie_test1():
    # 声明一个CookieJar对象实例来保存cookie
    cookie = cookiejar.CookieJar()
    # 利用urllib库中的request的HTTPCookieProcessor对象来创建cookie处理器
    handler = request.HTTPCookieProcessor(cookie)
    # 通过handler来构建opener
    opener = request.build_opener(handler)
    # 此处的open方法同urllib的urlopen方法，也可以传入request
    response = opener.open('https://www.12306.cn/index/')
    for item in cookie:
        print('Name: {} Value: {}'.format(item.name, item.value))


def cookie_test2():
    # 设置保存cookie的文件，同级目录下的cookie.txt
    filename = 'c.txt'
    # 声明一个MozillaCookieJar对象实例来保存cookie，之后写入文件
    cookie = cookiejar.MozillaCookieJar(filename)
    # 利用urllib库的HTTPCookieProcessor对象来创建cookie处理器
    handler = request.HTTPCookieProcessor(cookie)
    # 通过handler来构建opener
    opener = request.build_opener(handler)
    # 创建一个请求，原理同urllib2的urlopen
    response = opener.open("http://www.12306.cn")
    # 保存cookie到文件
    cookie.save(ignore_discard=True, ignore_expires=True)


def cookie_test3():
    cookie = cookiejar.MozillaCookieJar()
    cookie.load('c.txt', ignore_discard=True, ignore_expires=True)
    req = request.Request('http://www.12306.cn')
    opener = request.build_opener(request.HTTPCookieProcessor(cookie))
    response = opener.open(req)
    print(response.read())


def save_cookie_test():
    res = api.get('https://www.12306.cn/index/')


def remove_cookie_test():
    pass


if __name__ == "__main__":
    from prettytable import PrettyTable

    x = PrettyTable(["name", "Area", "Population", "Annual Rainfall"])

    x.align["name"] = "l"  # Left align city names

    x.padding_width = 1  # One space between column edges and contents (default)

    x.add_row(["Adelaide", 1295, 1158259, 600.5])

    x.add_row(["Brisbane", 5905, 1857594, 1146.4])

    x.add_row(["Darwin", 112, 120900, 1714.7])

    x.add_row(["Hobart", 1357, 205556, 619.5])

    x.add_row(["Sydney", 2058, 4336374, 1214.8])

    x.add_row(["Melbourne", 1566, 3806092, 646.9])

    x.add_row(["Perth", 5386, 1554769, 869.4])
    print(x)
    pass
