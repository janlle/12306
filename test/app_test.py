# coding:utf-8

from urllib import request

from util.net_util import *
import time
from functools import lru_cache


def args_test(**kwargs):
    for k, v in kwargs.items():
        print(k, v)


if __name__ == "__main__":
    import requests
    from fake_useragent import UserAgent

    h = {"Referer": "https://www.12306.cn/index/", "Origin": "https://www.12306.cn",
         "Cookie": "JSESSIONID=09659CD206AEDE334842154ADAF8F14B; BIGipServerotn=284164618.50210.0000; BIGipServerpool_passport=300745226.50215.0000; RAIL_EXPIRATION=1575514714021; RAIL_DEVICEID=J92fVZVxR-_zpE49sNi89b75NraaEsBL9H7NcXXAy1DzylZrtEqDs8iYifa7Ov8C912XTMHMHfQcRntc5NWAS8Ohe2v447WWg3d0QwxLjCuNJff9Q8KWXGNO5A5HNSXJ7wRxvYKmzHLYBdE4FZtu-T9ihC_L4pk-; route=6f50b51faa11b987e576cdb301e545c4; BIGipServerpool_index=787481098.43286.0000"}
    res = requests.post('https://kyfw.12306.cn/passport/web/auth/uamtk-static', headers=h,
                        data={'appid': 'otn', 'username': 'wealip', 'password': '12306FF0',
                              'answer': '184%2C112%2C111%2C107'}, verify=False)
    print(res)
    print(res.text)
