# coding:utf-8

"""
start rob task good luck!
python start.py
"""

from util.logger import Logger
from train.login import Login
from train.search_stack import *
import tickst_config as config
import util.app_util as util

log = Logger(__name__)

if __name__ == '__main__':
    while True:
        hour = util.current_hour()
        if hour > 23 or hour < 6:
            continue
        else:
            login = Login()
            # login.login()
            ticket_list = search_stack(config.FROM_STATION, config.TO_STATION, config.DATE)

            show_tickets(ticket_list)
            if config.TRAINS_NO:
                if config.SEAT_TYPE_CODE:
                    ticket_list = [i for i in ticket_list if i.train_no in config.TRAINS_NO]
                    show_tickets(ticket_list)
            elif config.SEAT_TYPE_CODE:
                pass
        break
