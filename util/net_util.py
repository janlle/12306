# coding:utf-8

from urllib import parse
import requests
from fake_useragent import UserAgent
import util.logger as logger

log = logger.Logger(__name__)


class Http(object):

    def __init__(self, timeout=30, retry=3):
        self.session = requests.Session()
        self.headers = {"User-Agent": UserAgent().random}
        self.timeout = timeout
        self.retry_num = retry
        self.error_msg = ""
        self.session.headers = self.headers

    def set_header(self, headers):
        if isinstance(headers, dict):
            for key, value in headers:
                self.headers[key] = value

    def remove_header(self, headers):
        if isinstance(headers, dict):
            for key in headers:
                del self.headers[key]

    def get(self, url, data=None, headers=None):

        result = None
        self.set_header(headers=headers)
        try:
            if isinstance(data, dict):
                url += ("?" + parse.urlencode(data))
            print(url)
            response = self.session.get(url=url, data=data, headers=self.headers, timeout=self.timeout)
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
        self.set_header(headers=headers)
        try:
            response = self.session.post(url=url, data=body, headers=self.headers, timeout=self.timeout)
            if response.status_code == 200:
                result = response
            else:
                log.error("POST request error: %d" % response.status_code)
        except Exception as e:
            log.error(e)
        self.remove_header(headers=headers)
        return result


if __name__ == '__main__':
    http = Http()
    res = http.post("http://localhost:8080/test2")
