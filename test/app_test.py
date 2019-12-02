# coding:utf-8

from urllib import request

from util.net_util import *
import time
from functools import lru_cache


if __name__ == "__main__":
    import requests
    from fake_useragent import UserAgent

    # h = {"Referer": "https://www.12306.cn/index/", "Origin": "https://www.12306.cn"}
    #     # res = requests.post('https://kyfw.12306.cn/passport/web/auth/uamtk-static', headers=h,
    #     #                     data={'appid': 'otn'})
    #     # print(res)
    #     # print(res.cookies.get_dict())
    #     # print(res.text)
    # res = requests.get("https://kyfw.12306.cn/passport/captcha/captcha-image64", verify=False)
    # print(res.cookies)

