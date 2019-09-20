# coding:utf-8

import datetime
import prettytable
import config.stations as stations
import config.urls as urls
from train.ticket.ticket import Ticket
from util.net_util import api

ticket_data_index = {
    # 车次: 3
    "INDEX_TRAIN_NO": 3,
    # 起始站: 4
    "INDEX_TRAIN_START_STATION_CODE": 4,
    # 终点站: 5
    "INDEX_TRAIN_END_STATION_CODE": 5,
    # 出发站: 6,
    "INDEX_TRAIN_FROM_STATION_CODE": 6,
    # to_station_code:到达站: 7,
    "INDEX_TRAIN_TO_STATION_CODE": 7,
    #  出发时间: 8,
    "INDEX_TRAIN_LEAVE_TIME": 8,
    # arrive_time:达到时间: 9,
    "INDEX_TRAIN_ARRIVE_TIME": 9,
    # 历时: 10,
    "INDEX_TRAIN_TOTAL_CONSUME": 10,
    # 车票出发日期,
    "INDEX_START_DATE": 13,
    # 商务特等座: 32,
    "INDEX_TRAIN_BUSINESS_SEAT": 32,
    # 一等座: 31,
    "INDEX_TRAIN_FIRST_CLASS_SEAT": 31,
    # 二等座: 30,
    "INDEX_TRAIN_SECOND_CLASS_SEAT": 30,
    # 高级软卧: 21,
    "INDEX_TRAIN_ADVANCED_SOFT_SLEEP": 21,
    # 软卧: 23,
    "INDEX_TRAIN_SOFT_SLEEP": 23,
    # 动卧: 33,
    "INDEX_TRAIN_MOVE_SLEEP": 33,
    # 硬卧: 28,
    "INDEX_TRAIN_HARD_SLEEP": 28,
    # 软座: 24,
    "INDEX_TRAIN_SOFT_SEAT": 24,
    # 硬座: 29,
    "INDEX_TRAIN_HARD_SEAT": 29,
    # 无座: 26,
    "INDEX_TRAIN_NO_SEAT": 28,
    # 其他: 22,
    "INDEX_TRAIN_OTHER": 22,
    # 备注: 1,
    "INDEX_TRAIN_MARK": 1,
    # SECRET
    "INDEX_SECRET_STR": 0,
}


def search_stack(from_station, to_station, purpose="ADULT",
                 train_date=(datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')):
    """查询车票"""
    result = []
    params = urls.URLS.get("ticket_query").get("params")
    params['leftTicketDTO.train_date'] = train_date
    params['leftTicketDTO.from_station'] = stations.get_by_name(from_station)
    params['leftTicketDTO.to_station'] = stations.get_by_name(to_station)
    params['purpose_codes'] = purpose

    url = urls.URLS.get("ticket_query").get("request_url")

    response = api.get(url, params=params)
    if response.headers.get('Content-Type') == 'application/json;charset=UTF-8':
        body = response.json()
        if body['httpstatus'] == 200:
            result = body['data']['result']
    return result


def decode_data(tickets_list, purpose=None):
    """解析起始站"""
    table = prettytable.PrettyTable()
    table.field_names = Ticket().get_display_title()
    table.align = 'l'
    table.valign = 't'
    table.padding_width = 2
    tickets = []
    for ticket_line in tickets_list:
        ticket_item = ticket_line.split('|')
        ticket = Ticket()
        ticket.passenger_type = purpose
        ticket.train_no = ticket_item[ticket_data_index.get("INDEX_TRAIN_NO")]

        ticket.start_station = stations.get_by_code(
            ticket_item[ticket_data_index.get("INDEX_TRAIN_START_STATION_CODE")])
        ticket.end_station = stations.get_by_code(ticket_item[ticket_data_index.get("INDEX_TRAIN_END_STATION_CODE")])
        ticket.from_station = stations.get_by_code(ticket_item[ticket_data_index.get("INDEX_TRAIN_FROM_STATION_CODE")])
        ticket.to_station = stations.get_by_code(ticket_item[ticket_data_index.get("INDEX_TRAIN_TO_STATION_CODE")])

        ticket.start_station_code = ticket_item[ticket_data_index.get("INDEX_TRAIN_START_STATION_CODE")]
        ticket.end_station_code = ticket_item[ticket_data_index.get("INDEX_TRAIN_END_STATION_CODE")]
        ticket.from_station_code = ticket_item[ticket_data_index.get("INDEX_TRAIN_FROM_STATION_CODE")]
        ticket.to_station_code = ticket_item[ticket_data_index.get("INDEX_TRAIN_TO_STATION_CODE")]

        ticket.total_consume = ticket_item[ticket_data_index.get("INDEX_TRAIN_TOTAL_CONSUME")]
        ticket.leave_time = ticket_item[ticket_data_index.get("INDEX_TRAIN_LEAVE_TIME")]
        ticket.arrive_time = ticket_item[ticket_data_index.get("INDEX_TRAIN_ARRIVE_TIME")]
        ticket.business_seat = ticket_item[ticket_data_index.get("INDEX_TRAIN_BUSINESS_SEAT")]
        ticket.first_class_seat = ticket_item[ticket_data_index.get("INDEX_TRAIN_FIRST_CLASS_SEAT")]
        ticket.second_class_seat = ticket_item[ticket_data_index.get("INDEX_TRAIN_SECOND_CLASS_SEAT")]
        ticket.advanced_soft_sleep = ticket_item[ticket_data_index.get("INDEX_TRAIN_ADVANCED_SOFT_SLEEP")]
        ticket.soft_sleep = ticket_item[ticket_data_index.get("INDEX_TRAIN_SOFT_SLEEP")]
        ticket.move_sleep = ticket_item[ticket_data_index.get("INDEX_TRAIN_MOVE_SLEEP")]
        ticket.hard_sleep = ticket_item[ticket_data_index.get("INDEX_TRAIN_HARD_SLEEP")]
        ticket.soft_seat = ticket_item[ticket_data_index.get("INDEX_TRAIN_SOFT_SEAT")]
        ticket.hard_seat = ticket_item[ticket_data_index.get("INDEX_TRAIN_HARD_SEAT")]
        ticket.no_seat = ticket_item[ticket_data_index.get("INDEX_TRAIN_NO_SEAT")]
        ticket.other = ticket_item[ticket_data_index.get("INDEX_TRAIN_OTHER")]
        ticket.mark = ticket_item[ticket_data_index.get("INDEX_TRAIN_MARK")]
        ticket.secret_str = ticket_item[ticket_data_index.get("INDEX_SECRET_STR")]
        ticket.start_date = ticket_item[ticket_data_index.get("INDEX_START_DATE")]
        tickets.append(ticket)
        table.add_row(ticket.get_display_field())
    print(table)
    return ticket


if __name__ == '__main__':
    res = search_stack('广州', '武昌')
