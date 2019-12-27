# coding:utf-8

import datetime
from util.logger import Logger
from util.app_util import datetime_str_timestamp, current_timestamp
import ticket_config as config

log = Logger('debug')

if __name__ == "__main__":
    start_time = datetime_str_timestamp('2019-12-27 12:01:00')
    while True:
        current_time = current_timestamp()
        print(start_time - current_time)
        if start_time - current_time < 0:
            print("It's time")
            break
