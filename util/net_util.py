# coding:utf-8

from urllib import parse
import requests
from fake_useragent import UserAgent
import util.logger as logger

log = logger.Logger(__name__)

cookie = "_passport_session=677a797721a74720af6bb52c808933b92456; _passport_ct=15fa567abc3b416d88270c9367cd624at9519; _jc_save_wfdc_flag=dc; RAIL_DEVICEID=cqB4pPFnBKE85FlMa0qFSZj5DLtacLUcXIq5-8b8nfCRoBzn4Lo9WcOkLHxM9xLp0LL2kYq59jad3r0PbJWeP75uNjgHVqhOtz1a6-2Xb1x1sQq17wQbMirB22UogoIPCRK41j-80NxOI7B8SFeNNWmx-IMRXNIM; RAIL_EXPIRATION=1568956001186; _jc_save_fromStation=%u5E7F%u5DDE%2CGZQ; _jc_save_toDate=2019-09-18; _jc_save_toStation=%u97F6%u5173%2CSNQ; _jc_save_fromDate=2019-09-30; BIGipServerpool_passport=250413578.50215.0000; route=9036359bb8a8a461c164a04f8f50b252; BIGipServerotn=602931722.64545.0000"


class Http(object):

    def __init__(self, timeout=30, retry=3):
        self.session = requests.Session()
        self.headers = {"User-Agent": UserAgent().random, "Cookie": cookie}
        self.timeout = timeout
        self.retry_num = retry
        self.error_msg = ""
        self.session.headers = self.headers

    def set_header(self, headers):
        if isinstance(headers, dict):
            for key, value in headers.items():
                self.headers[key] = value

    def remove_header(self, headers):
        if isinstance(headers, dict):
            for key, value in headers.items():
                del self.headers[key]

    def get(self, url, data=None, headers=None):
        log.info(url)
        result = None
        self.set_header(headers=headers)
        try:
            if isinstance(data, dict):
                url += ("?" + parse.urlencode(data))
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
        log.info(url)
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


if __name__ == '__main__':
    http = Http()
    # res = http.post("http://localhost:8080/test2")
    # res = requests.post(url="https://kyfw.12306.cn/passport/web/login")
    # print(str(res.content, encoding="utf-8"))
