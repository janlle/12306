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
from train.order import Order

log = Logger(__name__)

seat_mapping = {
    0: '无座',
    1: '硬座',
    2: '软座',
    3: '硬卧',
    4: '动卧',
    5: '软卧',
    6: '高级软卧',
    7: '二等座',
    8: '一等座',
    9: '商务座',
}

if __name__ == '__main__':
    login = Login()
    while True:
        hour = util.current_hour()
        if hour > 22 or hour < 6:
            time.sleep(1)
            continue
        else:
            login.login()
            ticket_list = search_stack(from_station=config.FROM_STATION, to_station=config.TO_STATION,
                                       train_date=config.DATE)
            # show_tickets(ticket_list)
            log.info('There are qualified trains total %d' % len(ticket_list))
            if config.SEAT_TYPE:
                ticket_list = [i for i in ticket_list if i.train_no in config.TRAINS_NO]
                show_tickets(ticket_list)
                log.info('There are qualified trains total %d' % len(ticket_list))
                seat_level_all = [([0] * len(config.TRAINS_NO)) for i in range(len(config.SEAT_TYPE))]
                """
                [[0, 0], [0, 0], [0, 0]]
                0 {'train_no': 'K635', 0: 'no'}
                1 {'train_no': 'K635', 1: 'yes'}
                2 {'train_no': 'K635', 3: 'no'}
                
                0 {'train_no': 'K81', 0: 'yes'}
                1 {'train_no': 'K81', 1: 'yes'}
                2 {'train_no': 'K81', 3: 'yes'}
                
                [[{'train_no': 'K635', 3: 'no'}, {'train_no': 'K81', 3: 'yes'}], [{'train_no': 'K635', 1: 'yes'}, {'train_no': 'K81', 1: 'yes'}], [{'train_no': 'K635', 0: 'no'}, {'train_no': 'K81', 0: 'yes'}]]
                
                """
                for j, ticket in enumerate(ticket_list):
                    ticket_seat = ticket.get_seat_level(config.SEAT_TYPE)
                    for i, seat in enumerate(ticket_seat):
                        seat_level_all[i][j] = seat
                # Choose a ticket that you can order
                usable_ticket = {}
                for i in seat_level_all:
                    for j in i:
                        train_no = j['train_no']
                        usable = j['usable']
                        seat_type = j['type']
                        if usable != 'no' and usable != '--':
                            usable_ticket = {'train_no': train_no, 'type': seat_type}
                            break
                    else:
                        continue
                    break
                if usable_ticket:
                    log.info(
                        'Find a suitable ticket: ' + usable_ticket['train_no'] + ', seat type: ' + seat_mapping.get(
                            usable_ticket['type']))
                    order_ticket = None
                    for ticket in ticket_list:
                        if ticket.train_no == usable_ticket['train_no']:
                            order_ticket = ticket
                            break
                    order_ticket.seat_type = usable_ticket['type']
                    order = Order(order_ticket)
                    log.info(order)
                    order.submit()
                    log.info('Ticket order line is in progress,please wait...')
                    order.order_callback()
                else:
                    log.warning('There is no proper ticket')
                    break

            elif config.SEAT_TYPE:
                pass
            break
