# coding:utf-8

import config.urls as urls
import tickst_config as config
import util.logger
import util.app_util as util
import requests
import json
import time
from verify import verify_code
from util.net_util import *
from fake_useragent import UserAgent

log = logger.Logger(__name__)
urllib3.disable_warnings()


class Login(object):

    def __init__(self):
        self.account, self.password = config.ACCOUNT, config.PASSWORD
        self.captcha_url = urls.URLS.get('captcha_url')
        self.device_id_url = urls.URLS.get('devices_id_url')
        self.check_login_url = urls.URLS.get('check_login_url')
        self.answer = ''

    def login(self):
        if not self.account or not self.password:
            log.warning('请完善账号或密码信息!')
            return
        login_count = 0
        api.clear_cookie()
        self.init_cookie()
        self.check_login_status()
        while True:
            login_count += 1
            self.check_verify_code()
            params = urls.URLS.get('login').get('params')
            params['username'] = self.account
            params['password'] = self.password
            params['answer'] = self.answer

            # 登陆
            try:
                login_response = api.post(urls.URLS.get('login').get('request_url'), body=params)
                content_type = login_response.headers.get('Content-Type')
                if 'application/json' in content_type and login_response.json()['result_code'] == 0:
                    log.info('登陆成功,登陆次数: {}'.format(login_count))
                    api.save_cookie()
                    break
                elif login_response.headers.get('Content-Type') == 'text/html':
                    log.error('登陆失败!')
                    time.sleep(2)
            except Exception as e:
                log.error(e)

    def init_cookie(self):
        """
        set device sign
        :return:
        """
        request_url = self.device_id_url.get('request_url').format(UserAgent().random, util.timestamp())
        device_info_response = api.get(request_url)
        if device_info_response.status_code == 200:
            try:
                device_info = json.loads(device_info_response.text[18:-2])
                api.set_cookie(RAIL_DEVICEID=device_info.get('dfp'), RAIL_EXPIRATION=device_info.get('exp'))
            except Exception as e:
                log.error(e)
        else:
            log.error('获取设备指纹失败')

    def check_login_status(self):
        """
        检查登录状态
        :return:
        """
        request_url = self.check_login_url.get('request_url').format(UserAgent().random, util.timestamp())
        request_params = self.check_login_url.get('params')
        check_login_response = api.post(request_url, request_params)
        if check_login_response.status_code == 200:
            log.info(check_login_response.json())

    def check_verify_code(self):
        """校验验证码"""
        # 获取一个图片验证码
        base64_code = self.get_verify_code()
        # 获取验证码坐标
        location = verify_code.verify(base64_code)
        log.info('答案为: {}'.format(location))

        # 识别图片正确选项的坐标
        self.coordinate(location)

        # 校验验证码 parse.quote(self.answer)
        url = urls.URLS.get('validate_captcha').get('request_url').format(self.answer, util.timestamp())
        check_captcha_response = api.get(url)
        if check_captcha_response.status_code == 200:
            log.info(check_captcha_response.json()['result_message'])
        else:
            log.error('验证码校验失败')

    def get_verify_code(self):
        """获取12306图形验证码的base63数据"""
        url = self.captcha_url.get('request_url')
        return api.get(url).json()['image']

    def coordinate(self, location=None, auto=True):
        """获取验证码选项坐标"""
        options = []
        if auto:
            if isinstance(location, list):
                options = location
            else:
                options = location.split(',')
        else:
            print(u"""
                        *****************
                        | 1 | 2 | 3 | 4 |
                        *****************
                        | 5 | 6 | 7 | 8 |
                        *****************
                        """)
            res = input('请输入答案的位置: ')
            options = res.split(',')
        x = '0'
        y = '0'
        result = []
        for option in options:
            if option == '1':
                y = '77'
                x = '40'
            elif option == '2':
                y = '77'
                x = '112'
            elif option == '3':
                y = '77'
                x = '184'
            elif option == '4':
                y = '77'
                x = '256'
            elif option == '5':
                y = '149'
                x = '40'
            elif option == '6':
                y = '149'
                x = '112'
            elif option == '7':
                y = '149'
                x = '184'
            elif option == '8':
                y = '149'
                x = '256'
            result.append(x)
            result.append(y)
        self.answer = ','.join(result)


if __name__ == '__main__':
    login = Login()
    login.login()
    # login.init_cookie()
    # print(api.session.cookies.get_dict())

    # session = requests.Session()
    # print(session.cookies.get_dict())
    # res = session.get('https://www.12306.cn/index/')
    # if res.json():
    #     print('true')
    # else:
    #     print('false')
    # print(session.cookies.get_dict())
