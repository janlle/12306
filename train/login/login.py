# coding:utf-8
import config.urls as urls
import tickst_config as config
import util.logger as logger
import time
import util.app_util as util
import requests
from fake_useragent import UserAgent
from util.net_util import Http
from verify import verify_code

log = logger.Logger(__name__)


class Login(object):

    def __init__(self):
        self.account, self.password = config.ACCOUNT, config.PASSWORD
        self.http = Http(timeout=15, retry=3)

    def login(self):
        if not self.account or not self.password:
            log.warning("请完善账号或密码信息!")
            return
        login_count = 0
        params = urls.URLS.get("login").get("params")
        params["username"] = self.account
        params["password"] = self.password
        params["answer"] = "187%2C50%2C187%2C114%2C40%2C38"

        # res = http.Http().post(urls.URLS.get("login").get("request_url"), data=params)

        header = {
            "User-Agent": UserAgent().random,
            "Content-Type": "application/x-www-form-urlencoded",
            "Cookie": "_passport_session=5ad8c0f4192e47919aeb3aed72ff8c710927; _passport_ct=8504f917798945fa941176c7aa52161ct7936; _jc_save_wfdc_flag=dc; RAIL_DEVICEID=cqB4pPFnBKE85FlMa0qFSZj5DLtacLUcXIq5-8b8nfCRoBzn4Lo9WcOkLHxM9xLp0LL2kYq59jad3r0PbJWeP75uNjgHVqhOtz1a6-2Xb1x1sQq17wQbMirB22UogoIPCRK41j-80NxOI7B8SFeNNWmx-IMRXNIM; RAIL_EXPIRATION=1568956001186; _jc_save_fromStation=%u5E7F%u5DDE%2CGZQ; BIGipServerpool_passport=367854090.50215.0000; route=9036359bb8a8a461c164a04f8f50b252; BIGipServerotn=1173357066.50210.0000; _jc_save_toStation=%u97F6%u5173%2CSNQ; _jc_save_toDate=2019-09-18; _jc_save_fromDate=2019-09-30"
        }

        res = requests.post(urls.URLS.get("login").get("request_url"), params, headers=header, verify=False)
        print(urls.URLS.get("login").get("request_url"))
        print(str(res.content, encoding="utf-8"))
        # while True:
        #     requests.post("http://125.90.206.248/passport/web/login")
        #     time.sleep(0.5)
        #     login_count += 1

    @staticmethod
    def check_verify_code(self):
        answer = ""
        url = urls.URLS.get("validate_captcha").get("request_url").format(util.timestamp(), answer, util.timestamp())
        pass

    def get_verify_code(self):
        url = urls.URLS.get("captcha").get("request_url")
        return self.http.get(url).json()["image"]

    def coordinate(self, location=None, auto=True):
        options = []
        if auto:
            if isinstance(location, list):
                options = location
            else:
                options = location.split(",")

        else:
            print(u"""
                        *****************
                        | 1 | 2 | 3 | 4 |
                        *****************
                        | 5 | 6 | 7 | 8 |
                        *****************
                        """)
            print("请输入答案的位置")
        x = 0
        y = 0
        result = []
        for option in options:
            if option == 1:
                x = "77"
                y = "40"
            elif option == 2:
                x = "77"
                y = "112"
            elif option == 3:
                x = "77"
                y = "184"
            elif option == 4:
                x = "77"
                y = "256"
            elif option == 5:
                x = "149"
                y = "40"
            elif option == 6:
                x = "149"
                y = "112"
            elif option == 7:
                x = "149"
                y = "184"
            elif option == 8:
                x = "149"
                y = "256"
            result.append(x)
            result.append(y)
        return ",".join(result)


if __name__ == '__main__':
    login = Login()
    # login.login()
    res = login.get_verify_code();
    print(res)
    verify_code.verify(res)

    # print(login.coordinate(["1", "2", "3"]))
