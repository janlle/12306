# coding:utf-8
import config.urls as urls
import tickst_config as config
import util.logger as logger
import util.app_util as util
import requests
import time
from fake_useragent import UserAgent
from util.net_util import Http
from verify import verify_code
import urllib3

log = logger.Logger(__name__)
urllib3.disable_warnings()

headers = {
    "Cookie": "_passport_session=677a797721a74720af6bb52c808933b92456; _passport_ct=15fa567abc3b416d88270c9367cd624at9519; _jc_save_wfdc_flag=dc; RAIL_DEVICEID=cqB4pPFnBKE85FlMa0qFSZj5DLtacLUcXIq5-8b8nfCRoBzn4Lo9WcOkLHxM9xLp0LL2kYq59jad3r0PbJWeP75uNjgHVqhOtz1a6-2Xb1x1sQq17wQbMirB22UogoIPCRK41j-80NxOI7B8SFeNNWmx-IMRXNIM; RAIL_EXPIRATION=1568956001186; _jc_save_fromStation=%u5E7F%u5DDE%2CGZQ; _jc_save_toDate=2019-09-18; _jc_save_toStation=%u97F6%u5173%2CSNQ; _jc_save_fromDate=2019-09-30; BIGipServerpool_passport=250413578.50215.0000; route=9036359bb8a8a461c164a04f8f50b252; BIGipServerotn=602931722.64545.0000"
}


class Login(object):

    def __init__(self):
        self.account, self.password = config.ACCOUNT, config.PASSWORD
        self.http = Http(timeout=15, retry=3)
        self.answer = ""

    def login(self):
        if not self.account or not self.password:
            log.warning("请完善账号或密码信息!")
            return
        login_count = 0
        while True:
            login_count += 1
            self.check_verify_code()
            params = urls.URLS.get("login").get("params")
            params["username"] = self.account
            params["password"] = self.password
            params["answer"] = self.answer

            # 登陆
            try:
                res = self.http.post(urls.URLS.get("login").get("request_url"), body=params, headers=headers)

                # log.info(str(res.content, encoding="utf-8"))
                content_type = res.headers.get("Content-Type")
                log.info(content_type)
                if content_type == "application/json" and res.json()["result_code"] == 4:
                    log.info("登陆成功!登陆次数: {}".format(login_count))
                    break
                elif res.headers.get("Content-Type") == "text/html":
                    log.error("登陆失败!")

                time.sleep(3)
            except Exception as e:
                log.error(e)

    def check_verify_code(self):
        """校验验证码"""

        # 获取一个图片验证码
        base64_code = self.get_verify_code()

        # 获取验证码坐标
        location = verify_code.verify(base64_code)
        log.info("答案为: {}".format(location))

        # 识别图片正确选项的坐标
        self.coordinate(location)

        # 校验验证码 parse.quote(self.answer)
        url = urls.URLS.get("validate_captcha").get("request_url").format(self.answer, util.timestamp())
        result = self.http.get(url)
        log.info(str(result.content, encoding="utf-8"))

    def get_verify_code(self):
        """获取12306图形验证码的base63数据"""
        url = urls.URLS.get("captcha").get("request_url")
        return self.http.get(url).json()["image"]

    def coordinate(self, location=None, auto=True):
        """获取验证码选项坐标"""
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
        x = "0"
        y = "0"
        result = []
        for option in options:
            if option == "1":
                y = "77"
                x = "40"
            elif option == "2":
                y = "77"
                x = "112"
            elif option == "3":
                y = "77"
                x = "184"
            elif option == "4":
                y = "77"
                x = "256"
            elif option == "5":
                y = "149"
                x = "40"
            elif option == "6":
                y = "149"
                x = "112"
            elif option == "7":
                y = "149"
                x = "184"
            elif option == "8":
                y = "149"
                x = "256"
            result.append(x)
            result.append(y)
        self.answer = ",".join(result)


if __name__ == '__main__':
    login = Login()
    login.login()
    a = "hello"
    b = "hello"
    # print(a == b)
    # res = requests.get("https://www.12306.cn/index/", headers)
