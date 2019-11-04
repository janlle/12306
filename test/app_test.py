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
    import time
    from fake_useragent import UserAgent

    """
    https://www.12306.cn/index/otn/login/conf
    BIGipServerotn=233832970.24610.0000; 
    
    RAIL_EXPIRATION=1572968435087; 
    RAIL_DEVICEID=kdng2b84v92-79xY4juA7QEvWVblAQPRkBtqKLIpnvcGHuZyulrPaDC7tD1v7qugQ3RyHydqsxXuGGm44x-SVx2S2XIZgu-ElpUpMKX69zEx-63qDIZuVvtDE-V3vExTD0njilTT2TJXyE6ZsZTt2HJ4w5auAx_f; 
    
    https://kyfw.12306.cn/passport/web/auth/uamtk-static
    BIGipServerpool_passport=233636362.50215.0000
    """

    # user_agent = UserAgent()
    # for i in range(100):
    #     headers = {'User-Agent': user_agent.random,
    #                'Cookie': 'BIGipServerotn=233832970.24610.0000; RAIL_EXPIRATION=1572968435087; RAIL_DEVICEID=kdng2b84v92-79xY4juA7QEvWVblAQPRkBtqKLIpnvcGHuZyulrPaDC7tD1v7qugQ3RyHydqsxXuGGm44x-SVx2S2XIZgu-ElpUpMKX69zEx-63qDIZuVvtDE-V3vExTD0njilTT2TJXyE6ZsZTt2HJ4w5auAx_f; BIGipServerpool_passport=233636362.50215.0000'}
    #     res = requests.get(
    #         'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=2019-11-26&leftTicketDTO.from_station=WHN&leftTicketDTO.to_station=CSQ&purpose_codes=ADULT',
    #         verify=False, headers=headers)
    #     print(res.text)
    #     time.sleep(0.2)

    # res = requests.get('https://kyfw.12306.cn/otn/login/conf', verify=False)
    # print(res.cookies.get_dict().get('BIGipServerotn', None))
    l = ['a', 'b', 'c']
    import random

    print(random.choice([None]))
