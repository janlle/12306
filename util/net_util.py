# coding:utf-8

from http import cookiejar
from urllib import parse

import requests
import urllib3
from fake_useragent import UserAgent

import util.logger as logger
from sprider.get_proxy import ProxySpider
from util.app_util import get_root_path

cookie_path = get_root_path() + '/cookie.txt'
urllib3.disable_warnings()

log = logger.Logger(__name__)


class Http(object):

    def __init__(self, timeout=30, retry=3):
        self.session = requests.Session()
        self.timeout = timeout
        self.retry_num = retry
        self.proxy_spider = ProxySpider()
        # self.proxy = self.proxy_spider.get_able_proxy()
        self.session.headers = {'User-Agent': UserAgent().random}
        self.proxy = None

    def get(self, url, data=None, headers=None, params=None):
        result = None
        try:
            if isinstance(params, dict):
                url += ("?" + parse.urlencode(params))
            # log.info('GET: ' + url)
            response = self.session.get(url=url, data=data, headers=headers, timeout=self.timeout, verify=False,
                                        allow_redirects=False, proxies=self.proxy)
            if response.status_code == 200:
                result = response
            else:
                log.error("GET error status code: %d url: %s" % (response.status_code, url))
        except Exception as e:
            log.error('GET ' + str(e) + ' url: ' + url)
        return result

    def post(self, url, json=None, headers=None, data=None):
        result = None
        # log.info('POST: ' + url)
        try:
            response = self.session.post(url=url, data=data, json=json, headers=headers, timeout=self.timeout,
                                         verify=False,
                                         allow_redirects=False, proxies=self.proxy)
            if response.status_code == 200:
                result = response
            else:
                log.error("POST error status code: %d url: %s" % (response.status_code, url))
        except Exception as e:
            log.error('POST ' + str(e) + ' url: ' + url)
        return result

    def request(self, url, method='GET', headers=None, data=None):
        return self.session.request(method=method,
                                    url=url,
                                    proxies=self.proxy,
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
    r = api.get('https://www.baidu.com')
    print(r.status_code)
