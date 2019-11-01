# coding:utf8

import json
import re
import time

import util.app_util as util
from train.passenger import Passenger
from train.search_stack import *
from util.logger import Logger
from util.net_util import api
import tickst_config as config

log = Logger(__name__)
api.load_cookie()


class Order(object):

    def __init__(self, ticket):
        self.submit_order_request_url = urls.URLS.get('submit_order_request_url')
        self.passenger_url = urls.URLS.get('passenger_url')
        self.check_order_info = urls.URLS.get('check_order_info')
        self.init_dc_url = urls.URLS.get('init_dc_url')
        self.queue_count = urls.URLS.get('queue_count')
        self.confirm_submit_url = urls.URLS.get('confirm_submit_url')
        self.order_callback_url = urls.URLS.get('order_callback_url')
        self.unfinished_order_url = urls.URLS.get('unfinished_order_url')
        self.passenger_names = config.USER
        if len(self.passenger_names) < 1:
            raise BaseException('passenger must be not null')
        self.from_station = config.FROM_STATION
        self.to_station = config.TO_STATION
        self.train_no = config.TRAINS_NO[0]
        self.seat_type = config.SEAT_TYPE[0]
        self.date = config.DATE
        self.submit_token = None
        self.passenger_list = []
        self.ticket = ticket

    def submit(self):
        """提交车票信息"""
        submit_url = self.submit_order_request_url.get('request_url')
        ticket_params = self.submit_order_request_url.get('params')
        ticket_params['back_train_date'] = util.current_date()
        ticket_params['train_date'] = config.DATE
        ticket_params['secretStr'] = util.decode_secret_str(self.ticket.secret_str)
        ticket_params['query_from_station_name'] = self.ticket.from_station
        ticket_params['query_to_station_name'] = self.ticket.to_station
        submit_order_response = api.post(submit_url, data=ticket_params)
        if submit_order_response and submit_order_response.json()['httpstatus'] == 200:
            # get submit token
            self.submit_token = self.get_submit_token()
            # 获取乘车人
            if len(self.passenger_names) > self.ticket.seat_count:
                self.passenger_list = self.get_passenger(self.passenger_names[0:self.ticket.seat_count])
            else:
                self.passenger_list = self.get_passenger(self.passenger_names)
            self.check_order(self.ticket.seat_type)
        else:
            log.info('submit order error')

    def check_order(self, seat_type):
        """
        :return:
        """
        request_url = self.check_order_info.get('request_url')
        request_params = self.check_order_info.get('params')
        passenger_ticket_str = ''
        old_passenger_str = ''
        for passenger in self.passenger_list:
            passenger_ticket_str += (passenger.passenger_ticket_str(seat_type) + '_')
            old_passenger_str += passenger.old_passenger_str()

        passenger_ticket_str = passenger_ticket_str[0:-1]

        request_params['passengerTicketStr'] = passenger_ticket_str
        request_params['oldPassengerStr'] = old_passenger_str
        request_params['REPEAT_SUBMIT_TOKEN'] = self.submit_token['repeat_submit_token']

        check_order_response = api.post(request_url, data=request_params).json()
        if check_order_response.get('httpstatus') == 200:
            if check_order_response.get('data').get('submitStatus'):
                self.get_query_count(seat_type)
                self.confirm_submit(seat_type)
            else:
                log.info(check_order_response.get('data').get('errMsg'))
                import sys
                sys.exit(0)

    def get_passenger(self, name=None):
        """
        get account added passenger
        :param name:
        :return:
        """
        request_url = self.passenger_url.get('request_url')
        request_params = self.passenger_url.get('params')
        # api.session.cookies.clear()
        request_params['REPEAT_SUBMIT_TOKEN'] = self.submit_token['repeat_submit_token']
        passengers_data = api.post(request_url, request_params)
        if passengers_data.status_code == 200:
            passengers = passengers_data.json()['data']['normal_passengers']
            if passengers and len(passengers) > 0:
                passengers_list = []
                for p in passengers:
                    i = Passenger()
                    i.passenger_name = p['passenger_name']
                    i.sex_code = p['sex_code']
                    i.sex_name = p['sex_name']
                    i.born_date = p['born_date']
                    i.country_code = p['country_code']
                    i.passenger_id_type_code = p['passenger_id_type_code']
                    i.passenger_id_type_name = p['passenger_id_type_name']
                    i.passenger_id_no = p['passenger_id_no']
                    i.passenger_type = p['passenger_type']
                    i.passenger_flag = p['passenger_flag']
                    i.passenger_type_name = p['passenger_type_name']
                    i.mobile_no = p['mobile_no']
                    i.phone_no = p['phone_no']
                    i.email = p['email']
                    i.first_letter = p['first_letter']
                    i.total_times = p['total_times']
                    i.index_id = p['index_id']
                    i.all_enc_str = p['allEncStr']
                    passengers_list.append(i)
                if name and len(name) > 0:
                    return list(filter(lambda passenger: passenger.passenger_name in name, passengers_list))
                else:
                    return passengers_list

    def get_submit_token(self):
        """
        get submit ticket token from confirm passenger page
        :return:
        """

        request_url = self.init_dc_url.get('request_url')
        request_params = self.init_dc_url.get('params')
        html_page = api.post(request_url, data=request_params)
        html = str(html_page.content, encoding='utf-8')
        re_repeat_submit_token = re.compile(r"var globalRepeatSubmitToken = '(\S+)'")
        re_ticket_info_for_passenger_form = re.compile(r'var ticketInfoForPassengerForm=({.+})?')
        re_order_request_dto = re.compile(r'var orderRequestDTO=({.+})?')

        repeat_submit_token = re.search(re_repeat_submit_token, html).group(1)
        ticket_info_for_passenger_form = re.search(re_ticket_info_for_passenger_form, html).group(1)
        order_request_dto = re.search(re_order_request_dto, html).group(1)
        return {
            'repeat_submit_token': repeat_submit_token,
            'ticket_info_for_passenger_form': json.loads(ticket_info_for_passenger_form.replace('\'', '\"')),
            'order_request_params': json.loads(order_request_dto.replace('\'', '\"'))
        }

    def get_query_count(self, seat_type):
        """
        query order count
        :return:
        """
        ticket_info_for_passenger_form = self.submit_token['ticket_info_for_passenger_form']
        request_url = self.queue_count.get('request_url')
        request_params = self.queue_count.get('params')
        request_params['train_date'] = util.get_gmt_time(self.date)
        request_params['fromStationTelecode'] = stations.get_by_name(self.from_station)
        request_params['toStationTelecode'] = stations.get_by_name(self.to_station)
        request_params['stationTrainCode'] = self.train_no
        request_params['seatType'] = seat_type
        request_params['leftTicketStr'] = ticket_info_for_passenger_form['leftTicketStr']
        request_params['purpose_codes'] = ticket_info_for_passenger_form['purpose_codes']
        request_params['train_location'] = ticket_info_for_passenger_form['train_location']
        request_params['train_no'] = ticket_info_for_passenger_form['queryLeftTicketRequestDTO']['train_no']
        request_params['REPEAT_SUBMIT_TOKEN'] = self.submit_token['repeat_submit_token']
        query_count = api.post(request_url, data=request_params)
        if query_count and query_count.json()['httpstatus'] == 200:
            log.info('get Queue Count success')
        else:
            log.error('get_query_count error')

    def confirm_submit(self, seat_type):
        """
        confirm submit order
        :return:
        """
        ticket_info_for_passenger_form = self.submit_token['ticket_info_for_passenger_form']

        request_url = self.confirm_submit_url.get('request_url')
        request_params = self.confirm_submit_url.get('params')
        passenger_ticket_str = ''
        old_passenger_str = ''
        for passenger in self.passenger_list:
            passenger_ticket_str += (passenger.passenger_ticket_str(seat_type) + '_')
            old_passenger_str += passenger.old_passenger_str()

        passenger_ticket_str = passenger_ticket_str[0:-1]

        request_params['oldPassengerStr'] = old_passenger_str
        request_params['passengerTicketStr'] = passenger_ticket_str

        request_params['purpose_codes'] = ticket_info_for_passenger_form['purpose_codes']
        request_params['key_check_isChange'] = ticket_info_for_passenger_form['key_check_isChange']
        request_params['leftTicketStr'] = ticket_info_for_passenger_form['leftTicketStr']
        request_params['train_location'] = ticket_info_for_passenger_form['train_location']
        request_params['leftTicketStr'] = ticket_info_for_passenger_form['leftTicketStr']
        request_params['REPEAT_SUBMIT_TOKEN'] = self.submit_token['repeat_submit_token']

        confirm_submit_response = api.post(request_url, data=request_params)
        if confirm_submit_response:
            log.info('confirm submit success')
        else:
            log.error('confirm_submit error')

    def order_callback(self):
        count = 1
        request_url = self.order_callback_url.get('request_url')
        request_url = request_url.format(util.timestamp(), 'dc')
        while True:
            order_callback_response = api.get(request_url).json()
            if order_callback_response.get('data', None):
                if order_callback_response.get('data').get('orderId', None):
                    log.info('下单成功,请登录 12306 订单中心 -> 火车票订单 -> 未完成订单，支付订单!')
                    break
                else:
                    count += 1
                    log.info('购票结果查询中，第 {} 次查询...'.format(count))
            else:
                log.info('下单失败')
            time.sleep(2)

    def __str__(self):
        return '[乘车人: %s, 出发站: %s, 到达站: %s, 车次: %s, 座位: %s, 出发时间: %s %s:00]' % (
            self.passenger_names, self.from_station, self.to_station, self.train_no, self.seat_type, self.date,
            self.ticket.leave_time)

    def search_unfinished_order(self):
        """
        this is search unfinished order
        :return:
        """
        request_url = self.unfinished_order_url.get('request_url')
        request_params = self.unfinished_order_url.get('params')
        response = api.post(request_url, data=request_params)
        if response and response.json()['httpstatus'] == 200:
            response_json = response.json()
            if 'data' in response_json.keys():
                ticket_list = response.json()['data']['orderDBList']
                if len(ticket_list) > 0:
                    log.info('You have an outstanding order please cancel it or pay it')
                return not len(ticket_list) > 0
        return True


if __name__ == '__main__':
    t = Ticket()
    t.leave_time = '2019-11-07'
    t.secret_str = 'kFb1rqYphydFW/FWBN6NAXE2rZ5BvA7sWvrhfphQ32m65fnQ9zBfNKcG64A9i0RQvSj9zbLJtza13uQ82gRN03TYraKALaC1OOmSs5BcF/P3N5C27XpGcqwRV1mkq+F5a6G+nHE9CBz1+QQPukvnuHCTkNXYNO5Jf4M8UNjuGoi7W6C3G+7GcExnWFXMtRpSvUrtiz/6UsEVBBlBmw++xuMKT7tNdxhx7hacczWV1ViEJ02whoPONM7Y9SzodsDE+T7ZpLd59MbOl+ajlbhZ1UHIX9mGlXZ2tF6Ji1g2DdRGtAjnES/1Cg=='
    t.train_no = 'K81'
