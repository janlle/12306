# coding:utf-8

from urllib import request
from util.net_util import *
from prettytable import PrettyTable
from colorama import Fore
import requests


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


if __name__ == "__main__":
    # res = requests.get(
    #     'https://kyfw.12306.cn/passport/captcha/captcha-check?answer=40,77&rand=sjrand&login_site=E&_=1572501115466',
    #     verify=False)
    # print(res.json())

    for i in range(5):
        print(i)
    else:
        print(u"循环完整执行一次。")
    pass
