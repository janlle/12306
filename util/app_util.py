# coding:utf-8

import datetime
import locale
import os
import re
import telnetlib
import time
import urllib
import hashlib
import base64

GMT_FORMAT = '%a %b %d %Y %H:%M:%S GMT+0800 (中国标准时间)'
locale.setlocale(locale.LC_CTYPE, 'chinese')


def get_root_path():
    """获取项目根路径"""
    project_name = "12306"
    current_path = os.path.abspath(os.path.dirname(__file__))
    return current_path[:current_path.find(project_name) + len(project_name)]


def timestamp():
    return int(round(time.time() * 1000))


def current_timestamp():
    return int(round(time.time() * 1000))


def current_hour():
    return datetime.datetime.now().hour


def current_date():
    return datetime.datetime.now().strftime('%Y-%m-%d')


def current_date_time():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def check_date(text):
    match = re.compile(r'^\d{4}-\d{1,2}-\d{1,2}$').match(text)
    if match:
        return match.group() is not None
    else:
        return False


def decode_secret_str(code):
    return urllib.parse.unquote(code).replace('\n', '')


def proxy_test(proxy):
    try:
        telnetlib.Telnet(proxy.get('ip'), proxy.get('port'), timeout=1)
        return True
    except BaseException as e:
        return False


def get_gmt_time(text):
    """
    Fri Oct 025 2019 00:00:00 GMT+0800 (中国标准时间)
    Sun Oct 06 2019 00:00:00 GMT+0800 (中国标准时间)
    :param text:
    :return:
    """
    return datetime.datetime.strptime(text, '%Y-%m-%d').strftime(GMT_FORMAT)


def sha256(content=None):
    if content:
        m = hashlib.sha256()
        m.update(b'content')
        return m.hexdigest(), base64.urlsafe_b64encode(m.digest()).decode()
    return ""


if __name__ == '__main__':
    print(sha256(
        'aclcdsj2F1n0s0fe8i1l8a7A0c4638844d94bb3372dacbi4e5y8e05cd27s2i5uapeE3m0o4t3ld20n6Wco646sci035p3a7f8r1W0B5laganbd622asbp1T8mfme86729731cb20ac166s6r7v6i1Sbz5184txo9s00reSbrneaSaz02oxs1e8hxa9f0wtnrnDkialToosot3m1ZIns-ctdulhauEpiro9c1U5nfe0a1g3a5rbs6o7b0k5o7bda83u0efA0e2t5o8i0l3/8.8 7W5n3o2sfNI r0m0b wi367;5xi4a ap l0W.b0i3/038./6m(rHCM),klek eGic oL ThKo e377.5.t9K4e1e8pSAf)r6/ 34.n6We;S.a1tTD bw5d0ia(10e50a2l3zcMan9g5r6s576ed4l8c50dr7wae0L7n3u7gbed-1S9otkoepnSbceo18uetoDe3id1N1t1r1cbuekoosn2l1s0V0rxi4nejivnEe'))
