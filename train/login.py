# coding:utf-8

import base64
import json
from io import BytesIO
from urllib.parse import quote

from PIL import Image

import config.urls as urls
import tickst_config as config
from config.stations import get_by_name
from util.app_util import *
from util.net_util import *
from verify import verify_code

log = logger.Logger(__name__)
urllib3.disable_warnings()
captcha_temp_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + '/image_captcha/'

fake_cookie = {
    '_jc_save_fromStation': quote(config.FROM_STATION + ',' + get_by_name(config.FROM_STATION), 'utf-8'),
    '_jc_save_toStation': quote(config.TO_STATION + ',' + get_by_name(config.FROM_STATION), 'utf-8'),
    '_jc_save_fromDate': config.DATE,
    '_jc_save_toDate': current_date(),
    '_jc_save_wfdc_flag': 'dc'
}


class Login(object):

    def __init__(self):
        self.account, self.password = config.ACCOUNT, config.PASSWORD
        self.auto_identify = config.CAPTCHA_IDENTIFY
        self.captcha_url = urls.URLS.get('captcha_url')
        self.device_id_url = urls.URLS.get('devices_id_url')
        self.check_login_url = urls.URLS.get('check_login_url')
        self.conf_url = urls.URLS.get('conf_url')
        self.login_url = urls.URLS.get('login_url')
        self.iconfont_url = urls.URLS.get('iconfont_url')
        self.check_captcha_url = urls.URLS.get('check_captcha_url')
        self.captcha_url = urls.URLS.get('captcha_url')
        self.uamtk_url = urls.URLS.get('uamtk_url')
        self.uamauthclient_url = urls.URLS.get('uamauthclient_url')
        self.answer = ''

    def login(self):
        if not self.account or not self.password:
            log.warning('请完善账号或密码信息!')
            return
        login_count = 0

        api.clear_cookie()
        api.set_cookie(m=fake_cookie)
        self.init_cookie()

        request_url = self.login_url.get('request_url')

        request_params = self.login_url.get('params')
        request_params['username'] = self.account
        request_params['password'] = self.password
        request_params['answer'] = self.answer

        login_headers = self.login_url.get('headers')
        login_headers['User-Agent'] = UserAgent().random

        while True:
            login_count += 1
            self.check_captcha(self.auto_identify)
            # start login
            try:
                login_response = api.post(request_url, data=request_params,
                                          headers=login_headers)
                content_type = login_response.headers.get('Content-Type')
                if 'application/json' in content_type and login_response.json()['result_code'] == 0:
                    log.info('login success login frequency is {}'.format(login_count))
                    self.check_login_status()
                    api.save_cookie()
                    break
                elif login_response.headers.get('Content-Type') == 'text/html':
                    log.error('login failed!')
                    time.sleep(2)
            except Exception as e:
                log.error(e)

    def init_cookie(self):
        """
        set device sign
        :return:
        """
        # first
        request_url = self.iconfont_url.get('request_url').format(timestamp())
        api.get(request_url)

        # second
        request_url = self.conf_url.get('request_url')
        api.post(request_url)

        # third
        request_url = self.check_login_url.get('request_url')
        request_params = self.check_login_url.get('params')
        api.post(request_url, data=request_params)

        # fourth
        request_url = self.device_id_url.get('request_url').format(timestamp())
        device_info_response = api.get(request_url)

        if device_info_response.status_code == 200:
            try:
                device_info = json.loads(device_info_response.text[18:-2])
                api.set_cookie(RAIL_DEVICEID=device_info.get('dfp'), RAIL_EXPIRATION=device_info.get('exp'))
            except Exception as e:
                log.error(e)
        else:
            log.error('Failed to obtain device fingerprint')

    def check_login_status(self):
        """
        check login status
        :return:
        """
        try:
            request_url = self.uamtk_url.get('request_url')
            request_params = self.uamtk_url.get('params')
            response = api.post(request_url, data=request_params)
            if response and response.json()['result_code'] == 0:
                request_url = self.uamauthclient_url.get('request_url')
                request_params = self.uamauthclient_url.get('params')
                request_params['tk'] = response.json()['newapptk']
                response = api.post(request_url, data=request_params)
                if response:
                    log.info(response.json()['验证通过'])
                else:
                    log.info('user check failed')
        except BaseException as e:
            log.error(e)

    def check_captcha(self, auto_identify=0):
        """
        check captcha
        :param auto_identify: is auto identify
        :return:
        """
        # 获取一个图片验证码
        base64_code = self.get_captcha()
        # 获取验证码坐标
        location = []
        if auto_identify == 0:
            location = verify_code.verify(base64_code)
        elif auto_identify == 1:
            img = Image.open(BytesIO(base64.b64decode(base64_code)))
            img.show()
            print(u"""
                    *****************
                    | 1 | 2 | 3 | 4 |
                    *****************
                    | 5 | 6 | 7 | 8 |
                    *****************
                    """)
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

        check_captcha_response = api.get(request_url)
        if check_captcha_response.status_code == 200 and 'application/json' in check_captcha_response.headers.get(
                'Content-Type'):
            log.info(check_captcha_response.json()['result_message'])
        else:
            log.error('验证码校验失败')

    def get_captcha(self):
        """
        get a 12306 captcha
        """
        request_url = self.captcha_url.get('request_url')
        return api.get(request_url).json()['image']

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
    # login.check_captcha(1)

    pass
