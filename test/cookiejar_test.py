# coding:utf-8

from http import cookiejar
import requests

cookie = cookiejar.LWPCookieJar('c.txt')


def save_cookie():
    res = requests.get('https://kyfw.12306.cn/passport/captcha/captcha-image64', verify=False)
    print(res.cookies)
    requests.utils.cookiejar_from_dict({c.name: c.value for c in res.cookies}, cookie)
    #
    res = requests.get('https://www.taobao.com/', verify=False)
    print(res.cookies)
    requests.utils.cookiejar_from_dict({c.name: c.value for c in res.cookies}, cookie)

    # res = requests.get('https://www.jd.com/', verify=False)
    # print(res.cookies)
    # requests.utils.cookiejar_from_dict({c.name: c.value for c in res.cookies}, cookie)

    cookie.save(ignore_discard=True, ignore_expires=True)


def load_cookie():
    # cookie = cookiejar.MozillaCookieJar()
    cookie.load(ignore_discard=True, ignore_expires=True)
    cookies = requests.utils.dict_from_cookiejar(cookie)
    print(cookies)


def clear_cookie():
    cookie.clear()
    cookie.save()


if __name__ == '__main__':
    # save_cookie()
    # load_cookie()
    clear_cookie()
