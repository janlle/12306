# coding:utf-8

from io import BytesIO
from PIL import Image
from config.url_config import URLS
from util.app_util import *
from util.net_util import *
from verify import verify_code
from train.logdevice import generate_advice
from util.logger import Logger
log = Logger('INFO')

captcha_temp_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + '/image_captcha/'


class Login(object):

    def __init__(self):
        self.account, self.password = config.ACCOUNT, config.PASSWORD
        self.auto_identify = config.CAPTCHA_IDENTIFY
        self.captcha_url = URLS.get('captcha_url')
        self.device_id_url = URLS.get('devices_id_url')
        self.check_login_url = URLS.get('check_login_url')
        self.conf_url = URLS.get('conf_url')
        self.login_url = URLS.get('login_url')
        self.iconfont_url = URLS.get('iconfont_url')
        self.check_captcha_url = URLS.get('check_captcha_url')
        self.captcha_url = URLS.get('captcha_url')
        self.uamtk_url = URLS.get('uamtk_url')
        self.uamauthclient_url = URLS.get('uamauthclient_url')
        self.answer = ''

    def login(self):
        if not self.account or not self.password:
            log.warning('请完善账号或密码信息!')
            return
        login_count = 0

        clear_local_cookie()

        self.init_cookie()

        while True:
            login_count += 1

            # Check captcha
            self.check_captcha(self.auto_identify)

            # Start login
            try:
                request_url = self.login_url.get('request_url')
                request_params = self.login_url.get('params')
                request_params['username'] = self.account
                request_params['password'] = self.password
                request_params['answer'] = self.answer

                login_response = api.post(request_url, data=request_params).json()

                message = login_response['result_message']
                if login_response['result_code'] == 0:
                    log.info('{}，共登录 {} 次'.format(message, login_count))
                    self.check_login_status()
                    break
                else:
                    log.error(login_response['result_message'])
                    if message.startswith('您的用户已经被锁定'):
                        t = re.findall(r'[1-9]\d*', message)
                        if t and len(t) > 0:
                            print('sleep' + str(t[0]))
                            time.sleep(int(t[0]) * 60)
                        else:
                            time.sleep(5)
                    else:
                        time.sleep(5)
            except Exception as e:
                log.error(e)

    def init_cookie(self):
        """
        set device sign
        :return:
        """
        # First
        request_url = self.iconfont_url.get('request_url').format(timestamp())
        api.single_get(request_url)

        # Second
        request_url = self.conf_url.get('request_url')
        api.single_post(request_url)

        # Third
        request_url = self.check_login_url.get('request_url')
        request_params = self.check_login_url.get('params')
        h = {"Referer": "https://www.12306.cn/index/", "Origin": "https://www.12306.cn"}
        api.single_post(request_url, data=request_params, headers=h)

        # Fourth
        try:
            device_info = generate_advice()
            save_cookie(RAIL_DEVICEID=device_info.get('dfp'), RAIL_EXPIRATION=device_info.get('exp'))
        except Exception as e:
            log.error('Failed to obtain device fingerprint ' + str(e))

    def check_login_status(self):
        """
        check login status
        :return:
        """
        try:
            request_url = self.uamtk_url.get('request_url')
            request_params = self.uamtk_url.get('params')
            h = {"Referer": "https://www.12306.cn/index/", "Origin": "https://www.12306.cn"}
            response = api.post(request_url, headers=h, data=request_params).json()
            if response['result_code'] == 0:
                request_url = self.uamauthclient_url.get('request_url')
                request_params = self.uamauthclient_url.get('params')
                request_params['tk'] = response['newapptk']
                response = api.single_post(request_url, data=request_params).json()
                if response.get('result_code') == 0:
                    log.info('{}，用户名: {}'.format(response.get('result_message'), response.get('username')))
                else:
                    log.info(response.get('result_message', 'error'))
            elif response['result_code'] == 1:
                log.error(response['result_message'])
        except BaseException as e:
            log.error(e)

    def check_captcha(self, auto_identify=0):
        """
        Check captcha
        :param auto_identify: is auto identify
        :return:
        """
        # 获取一个图片验证码
        base64_code, cookies = self.get_captcha()
        # 获取验证码坐标
        location = []
        if auto_identify == 0:
            location = verify_code.verify(base64_code)
        elif auto_identify == 1:
            img = Image.open(BytesIO(base64.b64decode(base64_code)))
            img.show()
            log.info('*****************')
            log.info('| 1 | 2 | 3 | 4 |')
            log.info('*****************')
            log.info('| 5 | 6 | 7 | 8 |')
            log.info('*****************')
            res = input('请输入答案的位置(多个答案使用英文逗号分隔): ')
            try:
                location = res.split(',')
            except Exception as e:
                log.error(e)

        log.info('答案为: {}'.format(location))

        # 识别图片正确选项的坐标
        self.coordinate(location)
        # 校验验证码 parse.quote(self.answer)
        request_url = self.check_captcha_url.get('request_url').format(self.answer, timestamp())

        check_captcha_response = api.single_get(request_url, cookies=cookies).json()

        log.info(check_captcha_response['result_message'])

    def get_captcha(self):
        """
        Get a 12306 captcha
        """
        request_url = self.captcha_url.get('request_url')
        res = api.single_get(request_url)
        return res.json()['image'], res.cookies.get_dict()

    def coordinate(self, options=None):
        """获取验证码选项坐标"""
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
    # pass
