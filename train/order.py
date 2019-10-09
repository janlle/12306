# coding:utf8

import json
import re
import time

import util.app_util as util
from train.passenger import Passenger
from train.search_stack import *
from util.logger import Logger
from util.net_util import api

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
        self.passenger_name = config.USER[0]
        self.from_station = config.FROM_STATION
        self.to_station = config.TO_STATION
        self.train_no = config.TRAINS_NO[0]
        self.seat_type = config.SEAT_TYPE[0]
        self.date = config.DATE
        self.submit_token = None
        self.ticket = ticket
        self.passenger = None

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
            self.passenger = self.get_passenger(self.passenger_name)[0]
            log.info(submit_order_response.json())
            self.check_order()
        else:
            log.info('submit order error')

    def check_order(self):
        """
        :return:
        """
        request_url = self.check_order_info.get('request_url')
        request_params = self.check_order_info.get('params')
        request_params['passengerTicketStr'] = self.passenger.passenger_ticket_str(self.seat_type)
        request_params['oldPassengerStr'] = self.passenger.old_passenger_str()
        request_params['REPEAT_SUBMIT_TOKEN'] = self.submit_token['repeat_submit_token']

        check_order_response = api.post(request_url, data=request_params)
        log.info(check_order_response.json())
        if check_order_response and check_order_response.json()['httpstatus'] == 200:
            self.get_query_count()
            self.confirm_submit()

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
        print(api.session.cookies.get_dict())
        passengers_data = api.post(request_url, request_params)
        print(passengers_data.json())
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
                if name:
                    return list(filter(lambda passenger: passenger.passenger_name == name, passengers_list))
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

    def get_query_count(self):
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
        request_params['seatType'] = self.seat_type
        request_params['leftTicketStr'] = ticket_info_for_passenger_form['leftTicketStr']
        request_params['purpose_codes'] = ticket_info_for_passenger_form['purpose_codes']
        request_params['train_location'] = ticket_info_for_passenger_form['train_location']
        request_params['train_no'] = ticket_info_for_passenger_form['queryLeftTicketRequestDTO']['train_no']
        request_params['REPEAT_SUBMIT_TOKEN'] = self.submit_token['repeat_submit_token']
        query_count = api.post(request_url, data=request_params)
        if query_count and query_count.json()['httpstatus'] == 200:
            log.info(query_count.json())
        else:
            log.error('get_query_count error')

    def confirm_submit(self):
        """
        confirm submit order
        :return:
        """
        ticket_info_for_passenger_form = self.submit_token['ticket_info_for_passenger_form']

        request_url = self.confirm_submit_url.get('request_url')
        request_params = self.confirm_submit_url.get('params')
        request_params['oldPassengerStr'] = self.passenger.old_passenger_str()
        request_params['passengerTicketStr'] = self.passenger.passenger_ticket_str(self.seat_type)
        request_params['purpose_codes'] = ticket_info_for_passenger_form['purpose_codes']
        request_params['key_check_isChange'] = ticket_info_for_passenger_form['key_check_isChange']
        request_params['leftTicketStr'] = ticket_info_for_passenger_form['leftTicketStr']
        request_params['train_location'] = ticket_info_for_passenger_form['train_location']
        request_params['leftTicketStr'] = ticket_info_for_passenger_form['leftTicketStr']
        request_params['REPEAT_SUBMIT_TOKEN'] = self.submit_token['repeat_submit_token']

        confirm_submit_response = api.post(request_url, data=request_params)
        if confirm_submit_response:
            log.info(confirm_submit_response.json())
        else:
            log.error('confirm_submit error')

    def order_callback(self):
        count = 1
        request_url = self.order_callback_url.get('request_url')
        request_url = request_url.format(util.timestamp(), 'dc')
        order_callback_response = api.get(request_url)
        if order_callback_response:
            response_json = order_callback_response.json()
            if response_json['data']['orderId']:
                log.info('抢票成功,请登录12306我的火车票订单支付车票!')
                return 'success'
            else:
                time.sleep(1)
                count += 1
                log.info('第: {} 次查询'.format(count))
                self.order_callback()

    def __str__(self):
        return '[乘车人: %s, 出发站: %s, 到达站: %s, 车次: %s, 座位: %s, 出发时间: %s %s:00]' % (
            self.passenger_name, self.from_station, self.to_station, self.train_no, self.seat_type, self.date,
            self.ticket.leave_time)

    def search_unfinished_order(self):
        """
        this is search unfinished order
        :return:
        """
        request_url = self.unfinished_order_url.get('request_url')
        request_params = self.unfinished_order_url.get('params')
        print(request_url)
        print(request_params)
        response = api.post(request_url, data=request_params)
        if response:
            print(response.json())
        pass


if __name__ == '__main__':
    t = Ticket()
    t.leave_time = '2019-11-07'
    t.secret_str = 'kFb1rqYphydFW/FWBN6NAXE2rZ5BvA7sWvrhfphQ32m65fnQ9zBfNKcG64A9i0RQvSj9zbLJtza13uQ82gRN03TYraKALaC1OOmSs5BcF/P3N5C27XpGcqwRV1mkq+F5a6G+nHE9CBz1+QQPukvnuHCTkNXYNO5Jf4M8UNjuGoi7W6C3G+7GcExnWFXMtRpSvUrtiz/6UsEVBBlBmw++xuMKT7tNdxhx7hacczWV1ViEJ02whoPONM7Y9SzodsDE+T7ZpLd59MbOl+ajlbhZ1UHIX9mGlXZ2tF6Ji1g2DdRGtAjnES/1Cg=='
    t.from_station = '武昌'
    t.to_station = '长沙'
    t.train_no = 'K81'
    order = Order(t)
    api.load_cookie()
    print(api.session.cookies.get_dict())
    order.search_unfinished_order()
    # log.info('车票购买排队中,请稍后...')
    # order.order_callback()
