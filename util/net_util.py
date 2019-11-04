# coding:utf-8

from http import cookiejar
import requests
import urllib3
from fake_useragent import UserAgent

import util.logger as logger
from sprider.free_proxy import proxy
from util.app_util import get_root_path
import random

cookie_path = get_root_path() + '/cookie.txt'
urllib3.disable_warnings()

log = logger.Logger(__name__)


class Http(object):

    def __init__(self, timeout=1000, retry=3):
        self.session = requests.Session()
        self.timeout = timeout
        self.retry_num = retry
        self.proxy_list = proxy.get_usable_proxy(5)
        self.session.headers = {'User-Agent': UserAgent().random, 'Accept': '*/*'}

    def get(self, url, headers=None, data=None):
        try:
            response = self.session.get(url=url, data=data, headers=headers, timeout=self.timeout, verify=False,
                                        allow_redirects=False, proxies=random.choice(self.proxy_list))
            if response.status_code == 200:
                return response
            else:
                log.error("GET error status code: %d url: %s" % (response.status_code, url))
                raise BaseException('get failed response status code is not 200')
        except Exception as e:
            log.error('GET ' + str(e) + ' url: ' + url)

    def post(self, url, json=None, headers=None, data=None):
        try:
            response = self.session.post(url=url, data=data, json=json, headers=headers, timeout=self.timeout,
                                         verify=False,
                                         allow_redirects=False, proxies=random.choice(self.proxy_list))
            if response.status_code == 200:
                return response
            else:
                log.error("POST error status code: %d url: %s" % (response.status_code, url))
                raise BaseException('post failed response status code is not 200')
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

    @staticmethod
    def save_cookie():
        new_cookie = cookiejar.LWPCookieJar(cookie_path)
        requests.utils.cookiejar_from_dict({c.name: c.value for c in api.session.cookies}, new_cookie)
        new_cookie.save(cookie_path, ignore_discard=True, ignore_expires=True)
        # log.info('save_cookie' + str(api.session.cookies.get_dict()))

    @staticmethod
    def load_cookie():
        old_cookie = cookiejar.LWPCookieJar()
        old_cookie.load(cookie_path, ignore_discard=True, ignore_expires=True)
        api.session.cookies = requests.utils.cookiejar_from_dict(requests.utils.dict_from_cookiejar(old_cookie))
        # log.info('load_cookie' + str(api.session.cookies.get_dict()))

    @staticmethod
    def set_cookie(m=None, **kwargs):
        if m and isinstance(m, dict):
            for k, v in m.items():
                api.session.cookies.set(k, v)
        else:
            for k, v in kwargs.items():
                api.session.cookies.set(k, v)
        # log.info('set_cookie' + str(api.session.cookies.get_dict()))

    @staticmethod
    def clear_cookie(key=None):
        api.session.cookies.set(key, None) if key else api.session.cookies.clear()


api = Http()

if __name__ == '__main__':
    r = api.get(
        'https://kyfw.12306.cn/passport/captcha/captcha-check?answer=40,77&rand=sjrand&login_site=E&_=1572501115466')
    print(r.json())
