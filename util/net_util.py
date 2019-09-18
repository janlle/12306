# coding:utf-8


import requests
from fake_useragent import UserAgent
import config.urls


class Http(object):

    def __init__(self):
        self.header = {"User-Agent": UserAgent().random}
        self.session = requests.Session()
        self.session.headers = self.header

    def get(self, url, data=None):
        if not data:
            self.session.get(url=url, data=data)
        self.session.post(url=url)

    def post(self, url, data=None):
        if not data:
            return self.session.post(url=url, data=data)
        else:
            return self.session.post(url=url)

