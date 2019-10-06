# coding:utf-8

from http import cookiejar
from urllib import parse

import requests
import urllib3
from fake_useragent import UserAgent

import util.logger as logger

cookie_path = 'cookie.txt'
urllib3.disable_warnings()

log = logger.Logger(__name__)

cookie = "Cookie: _passport_session=967a7f2ff5874c39ba2767ab1eb7d9565362; _passport_ct=f5b0b27a2de8482884f917ba57fa2445t7920; _jc_save_wfdc_flag=dc; _jc_save_fromStation=%u6B66%u660C%2CWCN; _jc_save_toStation=%u957F%u6C99%2CCSQ; BIGipServerotn=653263370.24610.0000; RAIL_EXPIRATION=1570596001182; RAIL_DEVICEID=QpBR0-Dv71ZjiueC0I29kqdexiMb1hpE6Wbq-e29e4f7z05D9MvtlaP8tyfVRzQcGEumaHWSRkACeCQm2FfxMPZWpwTWHAm1Yli-8I_uAMnrAh4d-Pxx6O0iqh2o6H4G1fD-dn5F8Xgccjh0fs1M-EqVSFsA82qq; route=6f50b51faa11b987e576cdb301e545c4; _jc_save_toDate=2019-10-06; _jc_save_fromDate=2019-10-15; BIGipServerpool_passport=351076874.50215.0000"


class Http(object):

    def __init__(self, timeout=30, retry=3):
        self.session = requests.Session()
        self.headers = {"User-Agent": UserAgent().random, "Cookie": cookie}
        self.timeout = timeout
        self.retry_num = retry
        self.session.headers = self.headers

    def set_header(self, headers):
        if isinstance(headers, dict):
            for key, value in headers.items():
                self.headers[key] = value

    def remove_header(self, headers):
        if isinstance(headers, dict):
            for key, value in headers.items():
                del self.headers[key]

    def get(self, url, data=None, headers=None, params=None):
        result = None
        self.set_header(headers=headers)
        try:
            if isinstance(params, dict):
                url += ("?" + parse.urlencode(params))
            log.info('GET: ' + url)
            response = self.session.get(url=url, data=data, headers=self.headers, timeout=self.timeout, verify=False)
            if response.status_code == 200:
                result = response
            else:
                log.error("GET request error: %d" % response.status_code)
        except Exception as e:
            log.error(e)
        self.remove_header(headers=headers)
        return result

    def post(self, url, body=None, headers=None):
        result = None
        log.info('POST: ' + url)
        self.set_header(headers=headers)
        try:
            response = self.session.post(url=url, data=body, headers=self.headers, timeout=self.timeout, verify=False)
            if response.status_code == 200:
                result = response
            else:
                log.error("POST request error: %d" % response.status_code)
        except Exception as e:
            log.error(e)
        self.remove_header(headers=headers)
        return result


api = Http()


def save_cookie():
    new_cookie = cookiejar.LWPCookieJar(cookie_path)
    requests.utils.cookiejar_from_dict({c.name: c.value for c in api.session.cookies}, new_cookie)
    new_cookie.save(cookie_path, ignore_discard=True, ignore_expires=True)


def load_cookie():
    old_cookie = cookiejar.LWPCookieJar()
    old_cookie.load(cookie_path, ignore_discard=True, ignore_expires=True)
    api.session.cookies = requests.utils.cookiejar_from_dict(requests.utils.dict_from_cookiejar(old_cookie))


if __name__ == '__main__':
    http = Http()
