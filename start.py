# coding:utf-8

"""
start rob task good luck!

> python start.py
"""

from util.logger import Logger
from train.login import Login
import ticket_config as config
from train.order import Order
import threadpool
from sys import version_info
import datetime
import time
from config.stations import check_station_exists
from train.ticket import Ticket
from util.app_util import current_date, validate_date_str, current_hour

log = Logger(__name__)

if __name__ == '__main__':
    if version_info.major != 3 or version_info.minor != 6:
        log.error("请使用Python3.6版本运行此程序")

    # Checking config information
    if not validate_date_str(config.DATE):
        log.error('出发时间格式不正确')
        exit(0)

    today = datetime.datetime.strptime(current_date(), '%Y-%m-%d')
    depart_day = datetime.datetime.strptime(config.DATE, '%Y-%m-%d')
    difference = (depart_day - today).days
    if difference > 29 or difference < 0:
        log.error('出发时间超出了12306的售票时间范围')
        exit(0)

    if not check_station_exists(config.FROM_STATION) or not check_station_exists(config.TO_STATION):
        log.error('车站不存在')
        exit(0)

    time.sleep(20)
    login = Login()
    while True:
        hour = current_hour()
        if hour > 22 or hour < 6:
            time.sleep(1.5)
            continue
        else:
            login.login()
            order = Order(None)
            if not order.search_unfinished_order():
                break
            count = 0
            while True:
                ticket_list = Ticket.search_stack(from_station=config.FROM_STATION, to_station=config.TO_STATION,
                                                  train_date=config.DATE)
                count += 1
                if config.SEAT_TYPE:
                    ticket_list = [i for i in ticket_list if i.train_no in config.TRAINS_NO]
                    Ticket.show_tickets(ticket_list)
                    seat_level_all = [([0] * len(config.TRAINS_NO)) for i in range(len(config.SEAT_TYPE))]
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
                            if usable == '--' or usable == 'no' or usable == '*':
                                usable = 0
                            elif usable == 'yes':
                                usable = 21
                            usable = int(usable)
                            if usable > 0:
                                usable_ticket = {'train_no': train_no, 'type': seat_type, 'seat_count': usable}
                                break
                        else:
                            continue
                        break
                    if usable_ticket:
                        order_ticket = None
                        for ticket in ticket_list:
                            if ticket.train_no == usable_ticket['train_no']:
                                order_ticket = ticket
                                break
                        order_ticket.seat_type = usable_ticket['type']
                        order_ticket.seat_count = usable_ticket['seat_count']
                        order = Order(order_ticket)
                        order.submit()
                        log.info(order)
                        log.info('车票订单提交成功，请稍后...')
                        order.order_callback()
                        break
                    else:
                        log.warning('没有找到合适的车票，正尝试再次查询，查询次数: {}'.format(count))
                        time.sleep(1)
            break


def start_thread_pool():
    pool = threadpool.ThreadPool(10)
    reqs = threadpool.makeRequests(None, None)
    [pool.putRequest(req) for req in reqs]
    pool.wait()
    pass
