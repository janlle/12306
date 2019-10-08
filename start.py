# coding:utf-8

"""
start rob task good luck!

> python start.py
"""

from util.logger import Logger
from train.login import Login
from train.search_stack import *
import tickst_config as config
import util.app_util as util
import time
import train.order

log = Logger(__name__)

if __name__ == '__main__':
    login = Login()
    while True:
        hour = util.current_hour()
        if hour > 22 or hour < 6:
            time.sleep(1)
            continue
        else:
            login.login()
            ticket_list = search_stack(config.FROM_STATION, config.TO_STATION, config.DATE)
            show_tickets(ticket_list)
            log.info('A total of %d trains were found' % len(ticket_list))
            if config.TRAINS_NO and len(config.TRAINS_NO) > 0:
                if config.SEAT_TYPE:
                    ticket_list = [i for i in ticket_list if i.train_no in config.TRAINS_NO]
                    show_tickets(ticket_list)
                    log.info('There are qualified trains total %d' % len(ticket_list))

                    for ticket in ticket_list:
                        ticket_seat = ticket.get_seat_level(config.SEAT_TYPE)
                        print(ticket_seat)

            elif config.SEAT_TYPE:
                pass
            break
