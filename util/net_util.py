# coding:utf-8

import random
from http import cookiejar

import requests
import urllib3
from fake_useragent import UserAgent
from requests import Session

import ticket_config as config
import util.logger as logger
from sprider.free_proxy import proxy
from util.app_util import get_root_path

urllib3.disable_warnings()
cookie = cookiejar.LWPCookieJar(get_root_path() + '/cookie.txt')

log = logger.Logger(__name__)


class Http(object):

    def __init__(self, timeout=1000, retry=3):
        self.session = Session()
        self.timeout = timeout
        self.retry_num = retry
        if config.USE_PROXY:
            self.proxy_list = proxy.get_usable_proxy(5)
        else:
            self.proxy_list = [None]
        self.session.headers = {'User-Agent': UserAgent().random, 'Accept': '*/*'}

    def get(self, url, headers=None, data=None):
        load_cookie()
        try:
            response = self.session.get(url=url, data=data, headers=headers, timeout=self.timeout, verify=False,
                                        allow_redirects=False, proxies=random.choice(self.proxy_list))
            if response.status_code == 200:
                save_cookie(**response.cookies.get_dict())
                return response
            else:
                raise BaseException(
                    'Get request failed response status code is {} url: '.format(response.status_code, url))
        except Exception as e:
            log.error('GET ' + str(e) + ' url: ' + url)

    def post(self, url, json=None, headers=None, data=None):
        load_cookie()
        try:
            response = self.session.post(url=url, data=data, json=json, headers=headers, timeout=self.timeout,
                                         verify=False,
                                         allow_redirects=False, proxies=random.choice(self.proxy_list))
            if response.status_code == 200:
                save_cookie(**response.cookies.get_dict())
                return response
            else:
                raise BaseException(
                    'Post request failed response status code is %d url: %s' % (response.status_code, url))
        except Exception as e:
            log.error('POST ' + str(e) + ' url: ' + url)

    def request(self, url, method='GET', headers=None, data=None, params=None):
        return self.session.request(method=method,
                                    url=url,
                                    params=params,
                                    proxies=random.choice(self.proxy_list),
                                    data=data,
                                    headers=headers,
                                    timeout=self.timeout,
                                    allow_redirects=False
                                    )

    def single_get(self, url, headers=None, cookies=None):
        res = requests.get(url, verify=False, cookies=cookies, proxies=random.choice(self.proxy_list), headers=headers,
                           allow_redirects=False)
        save_cookie(**res.cookies.get_dict())
        return res

    def single_post(self, url, headers=None, cookies=None, data=None, json=None):
        res = requests.post(url=url, headers=headers, cookies=cookies, data=data, json=json, verify=False,
                            allow_redirects=False, proxies=random.choice(self.proxy_list))
        save_cookie(**res.cookies.get_dict())
        return res


def save_cookie(**kwargs):
    requests.utils.cookiejar_from_dict({k: v for k, v in kwargs.items()}, cookie)
    cookie.save(ignore_discard=True, ignore_expires=True)
    # log.info('save_cookie: ' + str(api.session.cookies.get_dict()))


def load_cookie():
    cookie.load(ignore_discard=True, ignore_expires=True)
    api.session.cookies = requests.utils.cookiejar_from_dict(requests.utils.dict_from_cookiejar(cookie))
    # log.info('load_cookie: ' + str(api.session.cookies.get_dict()))


def clear_local_cookie(key=None):
    api.session.cookies.set(key, None) if key else api.session.cookies.clear()


def clear_session_cookie():
    cookie.clear()
    cookie.save()


api = Http()

if __name__ == '__main__':
    r = api.get(
        'https://kyfw.12306.cn/passport/captcha/captcha-check?answer=40,77&rand=sjrand&login_site=E&_=1572501115466')
    print(r.json())
