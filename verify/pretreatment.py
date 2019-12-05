# coding:utf-8

import base64
import hashlib
import os
import requests
from util.logger import Logger

log = Logger('info')
PATH = "images"


def download_image(count=1):
    # 文件名为图像的MD5
    url = "https://kyfw.12306.cn/passport/captcha/captcha-image64"
    for i in range(count):
        response = requests.get(url)
        file_name = hashlib.md5(bytes(response.json()['image'], encoding="utf-8")).hexdigest()
        with open(f'{PATH}/{file_name}.jpg', 'wb') as file:
            file.write(base64.b64decode(response.json()["image"]))
            log.info("downloading " + file_name + ".jpg")


def del_image(path):
    for i in os.listdir(path):
        path_file = os.path.join(path, i)
        if os.path.isfile(path_file):
            os.remove(path_file)
        else:
            del_image(path_file)


if __name__ == '__main__':
    # del_image(PATH)
    # download_image(count=5)
    pass
