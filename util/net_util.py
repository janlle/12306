# coding:utf-8

from http import cookiejar
from urllib import parse
import requests
import urllib3
import util.logger as logger

cookie_path = '../cookie.txt'
urllib3.disable_warnings()

log = logger.Logger(__name__)


class Http(object):

    def __init__(self, timeout=30, retry=3):
        self.session = requests.Session()
        self.timeout = timeout
        self.retry_num = retry

    def get(self, url, data=None, headers=None, params=None):
        result = None
        try:
            if isinstance(params, dict):
                url += ("?" + parse.urlencode(params))
            log.info('GET: ' + url)
            response = self.session.get(url=url, data=data, headers=headers, timeout=self.timeout, verify=False,
                                        allow_redirects=False)
            if response.status_code == 200:
                result = response
            else:
                log.error("GET request error: %d" % response.status_code)
        except Exception as e:
            log.error(e)
        return result

    def post(self, url, body=None, headers=None):
        result = None
        log.info('POST: ' + url)
        try:
            response = self.session.post(url=url, data=body, headers=headers, timeout=self.timeout, verify=False,
                                         allow_redirects=False)
            if response.status_code == 200:
                result = response
            else:
                log.error("POST request error: %d" % response.status_code)
        except Exception as e:
            log.error(e)
        return result

    def request(self, url, method='GET', headers=None, data=None, proxy=None):
        if proxy is None:
            proxy = {}
        else:
            proxy = {"http": "http://{}".format(proxy)}
        return self.session.request(method=method,
                                    url=url,
                                    proxies=proxy,
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
    def set_cookie(**kwargs):
        for k, v in kwargs.items():
            api.session.cookies.set(k, v)
        # log.info('set_cookie' + str(api.session.cookies.get_dict()))

    @staticmethod
    def clear_cookie(key=None):
        api.session.cookies.set(key, None) if key else api.session.cookies.clear()


api = Http()

if __name__ == '__main__':
    http = Http()
