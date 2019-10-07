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
    save_cookie()


def remove_cookie_test():
    clear_cookie()


if __name__ == "__main__":
    save_cookie_test()
