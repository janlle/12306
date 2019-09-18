# coding:utf-8
import config.urls as urls
import tickst_config as config
import util.logger as logger
import time
import requests
from fake_useragent import UserAgent
import util.net_util as http

log = logger.Logger(__name__)


class Login(object):

    def __init__(self):
        self.account, self.password = config.ACCOUNT, config.PASSWORD

    def login(self):
        if not self.account or not self.password:
            log.warning("请完善账号或密码信息!")
            return
        login_count = 0
        params = urls.URLS.get("login").get("params")
        params["username"] = self.account
        params["password"] = self.password
        params["answer"] = self.account

        res = http.Http().post(urls.URLS.get("login").get("request_url"), data=params)
        print(res)
        # while True:
        #
        #     requests.post("http://125.90.206.248/passport/web/login")
        #     time.sleep(0.5)
        #     login_count += 1


if __name__ == '__main__':
    login = Login()
    login.login()
