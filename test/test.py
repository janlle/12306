# coding:utf-8

import logging
from logging.handlers import RotatingFileHandler
import time
import datetime
import os
import requests
from fake_useragent import UserAgent
from urllib import request
from urllib import parse
from http import cookiejar
from util.net_util import *
from prettytable import PrettyTable
from colorama import init, Fore

init(autoreset=False)

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


def pretty_table_test():
    from prettytable import PrettyTable

    x = PrettyTable(["name", "Area", "Population", "Annual Rainfall"])
    x.align = 'l'
    # x.align["name"] = "l"  # Left align city names
    x.padding_width = 1  # One space between column edges and contents (default)
    x.add_row(["Adelaide", 1295, 1158259, 600.5])
    x.add_row(["Brisbane", 5905, 1857594, 1146.4])
    x.add_row(["Darwin", 112, 120900, 1714.7])
    x.add_row(["Hobart", 1357, 205556, 619.5])
    x.add_row(["Sydney", 2058, 4336374, 1214.8])
    x.add_row(["Melbourne", 1566, 3806092, 646.9])
    x.add_row(["Perth", 5386, 1554769, 869.4])
    print(x)


def pretty_print2():
    my_list1 = [11, 12, 13, 14, 15, 16, 17]
    my_list2 = [21, 22, 23, 24, 25, 26, 27]
    my_list3 = [31, 32, 33, 34, 35, 36, 37]
    infos = [my_list1, my_list2, my_list3]
    # 改变列表中第一个元素的颜色
    # 并高亮显示，加上最后的Fore.RESET，会使得之后的元素不受影响，保持原样
    my_list1[0] = Fore.LIGHTRED_EX + str(my_list1[0])  # 没有加 Fore.RESET，之后的颜色都为红色
    my_list2[0] = Fore.LIGHTGREEN_EX + str(my_list2[0]) + Fore.RESET
    my_list3[0] = Fore.LIGHTYELLOW_EX + str(my_list3[0]) + Fore.RESET

    ptable = PrettyTable('list1 list2 list3 list4 list5 list6 list7'.split())
    for info in infos:
        ptable.add_row(info)
    print(ptable)


def call_back():
    count = 1
    if 100 / 50 == 0:
        print("success")
    else:
        count += 1
        print(count)
        call_back()


if __name__ == "__main__":
    call_back()
    pass
