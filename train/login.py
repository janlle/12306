# coding:utf-8

import json
import time

from fake_useragent import UserAgent
import config.urls as urls
import tickst_config as config
from util.app_util import *
import util.logger
from util.net_util import *
from verify import verify_code

log = logger.Logger(__name__)
urllib3.disable_warnings()


class Login(object):

    def __init__(self):
        self.account, self.password = config.ACCOUNT, config.PASSWORD
        self.captcha_url = urls.URLS.get('captcha_url')
        self.device_id_url = urls.URLS.get('devices_id_url')
        self.check_login_url = urls.URLS.get('check_login_url')
        self.conf_url = urls.URLS.get('conf_url')
        self.login_url = urls.URLS.get('login_url')
        self.iconfont_url = urls.URLS.get('iconfont_url')
        self.check_captcha_url = urls.URLS.get('check_captcha_url')
        self.captcha_url = urls.URLS.get('captcha_url')
        self.answer = ''

    def login(self):
        if not self.account or not self.password:
            log.warning('请完善账号或密码信息!')
            return
        login_count = 0

        api.clear_cookie()
        self.init_cookie()

        while True:
            login_count += 1
            self.check_captcha()
            request_url = self.login_url.get('request_url')

            request_params = self.login_url.get('params')
            request_params['username'] = self.account
            request_params['password'] = self.password
            request_params['answer'] = self.answer

            login_headers = self.login_url.get('headers')
            login_headers['User-Agent'] = UserAgent().random

            # 登陆
            try:
                api.session.cookies.set('RAIL_DEVICEID',
                                        'mM4mccxvjLRfZIKhTC-6baQsQ-l8atAzpaMz4IkAknh1afM460mD1VQdKrLm9Zh_B0wcCOXe2vZPU96x2NuLylOwmn7e2WRax0HoIQwkcf1Yn2ytGXQyr2mvicIBFhmq7PNsPBrsdNKgts9ahSwYmVS1_oDpPhMc')
                # api.load_cookie()
                print('login' + str(api.session.cookies.get_dict()))

                login_response = api.post(request_url, body=request_params,
                                          headers=login_headers)
                content_type = login_response.headers.get('Content-Type')
                print(login_response.text)
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
        # first
        request_url = self.iconfont_url.get('request_url').format(current_timestamp())
        api.get(request_url)

        # second
        request_url = self.conf_url.get('request_url')
        api.post(request_url)

        # third
        request_url = self.check_login_url.get('request_url').format(UserAgent().random, timestamp())
        request_params = self.check_login_url.get('params')
        api.post(request_url, body=request_params)

        # five
        request_url = self.device_id_url.get('request_url').format(UserAgent().random, timestamp())
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
        request_url = self.check_login_url.get('request_url').format(UserAgent().random, timestamp())
        request_params = self.check_login_url.get('params')
        check_login_response = api.post(request_url, body=request_params,
                                        headers={'Content-Type': 'application/x-www-form-urlencoded'})
        print(check_login_response.text)
        if check_login_response.status_code == 200 and 'application/json' in check_login_response.headers.get(
                'Content-Type'):
            log.info(check_login_response.json())

    def check_captcha(self):
        """校验验证码"""
        # 获取一个图片验证码
        base64_code = self.get_captcha()
        # 获取验证码坐标
        location = verify_code.verify(base64_code)
        log.info('答案为: {}'.format(location))

        # 识别图片正确选项的坐标
        self.coordinate(location)

        # 校验验证码 parse.quote(self.answer)
        request_url = self.check_captcha_url.get('request_url').format(self.answer, timestamp())
        api.save_cookie()
        api.session.cookies.set('RAIL_DEVICEID', None)
        check_captcha_response = api.get(request_url)
        print('check_captcha' + str(api.session.cookies.get_dict()))
        if check_captcha_response.status_code == 200 and 'application/json' in check_captcha_response.headers.get(
                'Content-Type'):
            log.info(check_captcha_response.json()['result_message'])
        else:
            log.error('验证码校验失败')

    def get_captcha(self):
        """
        get 12306 captcha
        """

        api.session.cookies.set('JSESSIONID', None)
        api.session.cookies.set('BIGipServerpool_index', None)
        api.session.cookies.set('BIGipServerpool_passport', None)
        api.session.cookies.set('_passport_session', None)

        api.session.cookies.set('BIGipServerotn', None)
        api.session.cookies.set('route', None)

        request_url = self.captcha_url.get('request_url')
        print('get_captcha' + str(api.session.cookies.get_dict()))
        return api.get(request_url).json()['image']

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

    # print(str(api.session.cookies.get_dict()))
    # api.session.cookies.set('RAIL_EXPIRATION','1570782222357')
    # api.session.cookies.set('BIGipServerotn','217055754.50210.0000')
    # api.session.cookies.set('BIGipServerpool_passport','384631306.50215.0000')
    # api.session.cookies.set('route','495c805987d0f5c8c84b14f60212447d')
    # api.session.cookies.set('_passport_session','601aa0349f084ce0aeccd6b792f900584421')
    # api.session.cookies.set('_passport_ct','47c2819332334a33a48c3edbcc87cdf5t6759')
    # api.session.cookies.set('RAIL_DEVICEID','mlwmNL6ykLPHgT7jCPCxQjF9GrPdiDDP4oEO6YYHYINUhrcnf5uNfuZMdr0ERHMJqQRdrc_NkB2RYtYqJAHIgDqKU-FDWOa_jVH3R1d9ijy9X1ffcNvX_Fkmoapb0AOOOa1I7yxzZGUTCP_WCunX-_RA3RdPBKy-')

    # r = api.post('http://kyfw.12306.cn/passport/web/login',
    #              headers={'Referer': 'https://kyfw.12306.cn/otn/resources/login.html',
    #                       'User-Agent': UserAgent().random}, body={}
    #              )
    #
    # print(r)
    # print(str(api.session.cookies.get_dict()))

    # login.conf()
    # print(str(api.session.cookies.get_dict()))

    # session = requests.Session()
    # res = session.post('http://kyfw.12306.cn/passport/web/login',
    #                    headers={'Referer': 'https://kyfw.12306.cn/otn/resources/login.html',
    #                             'User-Agent': UserAgent().random}
    #                    , data={})
    # print(res.content)
    # print(session.headers)
    # print(res.headers)

    pass
