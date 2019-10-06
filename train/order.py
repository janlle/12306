# coding:utf8

import json
import re

import config.urls as urls
import tickst_config as config
import util.app_util as util
from train.passenger import Passenger
from train.search_stack import *
from util.logger import Logger
from util.net_util import api

log = Logger(__name__)

headers = {
    "Cookie": "JSESSIONID=153BC91041E6A05386BD0D58B83D812E; _jc_save_wfdc_flag=dc; _jc_save_fromStation=%u6B66%u660C%2CWCN; _jc_save_toStation=%u957F%u6C99%2CCSQ; BIGipServerotn=653263370.24610.0000; RAIL_EXPIRATION=1570596001182; RAIL_DEVICEID=QpBR0-Dv71ZjiueC0I29kqdexiMb1hpE6Wbq-e29e4f7z05D9MvtlaP8tyfVRzQcGEumaHWSRkACeCQm2FfxMPZWpwTWHAm1Yli-8I_uAMnrAh4d-Pxx6O0iqh2o6H4G1fD-dn5F8Xgccjh0fs1M-EqVSFsA82qq; route=6f50b51faa11b987e576cdb301e545c4; _jc_save_toDate=2019-10-06; _jc_save_fromDate=2019-10-15"
}


class Order(object):

    def __init__(self):
        self.order_url = urls.URLS.get('submit_order')
        self.passenger = urls.URLS.get('passenger_url')
        self.check_order_info = urls.URLS.get('check_order_info')
        self.confirm_passenger = urls.URLS.get('confirm_passenger')
        self.queue_count = urls.URLS.get('queue_count')
        self.confirm_submit = urls.URLS.get('confirm_submit')
        self.passenger_name = config.USER[0]
        self.from_station = config.FROM_STATION
        self.to_station = config.TO_STATION
        self.train_no = config.TRAINS_NO[0]
        self.seat_type = config.SEAT_TYPE_CODE[0]
        self.date = config.DATE
        self.ticket = search_stack(self.from_station, self.to_station, train_no=self.train_no, train_date=self.date)[0]

    def submit(self):
        """提交车票信息"""
        submit_url = self.order_url.get('request_url')
        ticket_params = self.order_url.get('params')
        ticket_params['back_train_date'] = util.current_date()
        ticket_params['train_date'] = config.DATE
        ticket_params['secretStr'] = util.decode_secret_str(self.ticket.secret_str)
        ticket_params['query_from_station_name'] = self.ticket.from_station
        ticket_params['query_to_station_name'] = self.ticket.to_station
        submit_order_response = api.post(submit_url, ticket_params, headers=headers)
        if submit_order_response.status_code == 200 and submit_order_response.json()['httpstatus'] == 200:
            print(submit_order_response.json())
            self.check_order(self.passenger_name)
        else:
            log.info('submit order error')

    def check_order(self, passenger_name):
        """
        :return:
        """
        # get submit params
        submit_token = self.get_submit_token()

        # get passenger
        passenger = self.get_passenger(passenger_name)

        request_url = self.check_order_info.get('request_url')
        request_params = self.check_order_info.get('params')
        request_params['passengerTicketStr'] = passenger[0].passenger_ticket_str(self.seat_type)
        request_params['oldPassengerStr'] = passenger[0].old_passenger_str()
        request_params['REPEAT_SUBMIT_TOKEN'] = submit_token['repeat_submit_token']

        check_order_response = api.post(request_url, body=request_params, headers=headers)
        print(check_order_response.json())
        if check_order_response.status_code == 200 and check_order_response.json()['httpstatus'] == 200:
            self.get_query_count(submit_token)

    def get_passenger(self, name=None):
        """
        get account added passenger
        :param name:
        :return:
        """
        request_url = self.passenger.get('request_url')
        request_params = self.passenger.get('params')
        passengers_data = api.post(request_url, request_params, headers=headers)
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
        url = self.confirm_passenger.get('request_url')
        html_page = api.get(url, headers=headers)
        html = str(html_page.content, encoding='utf-8')
        re_repeat_submit_token = re.compile(r"var globalRepeatSubmitToken = '(\S+)'")
        re_ticket_info_for_passenger_form = re.compile(r'var ticketInfoForPassengerForm=({.+})?')
        re_order_request_dto = re.compile(r'var orderRequestDTO=({.+})?')

        repeat_submit_token = re.search(re_repeat_submit_token, html).group(1)
        ticket_info_for_passenger_form = re.search(re_ticket_info_for_passenger_form, html).group(1)
        order_request_dto = re.search(re_order_request_dto, html).group(1)
        print(ticket_info_for_passenger_form)
        print(order_request_dto)

        return {
            'repeat_submit_token': repeat_submit_token,
            'ticket_info_for_passenger_form': json.loads(ticket_info_for_passenger_form.replace('\'', '\"')),
            'order_request_params': json.loads(order_request_dto.replace('\'', '\"'))
        }

    def get_query_count(self, submit_token):
        """
        query order count
        :param submit_token:
        :return:
        """
        ticket_info_for_passenger_form = submit_token['ticket_info_for_passenger_form']
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
        request_params['REPEAT_SUBMIT_TOKEN'] = submit_token['repeat_submit_token']
        query_count = api.post(request_url, body=request_params, headers=headers)
        if query_count.status_code == 200 and query_count.json()['httpstatus'] == 200:
            log.info(query_count.json())
        else:
            log.error('get_query_count error')

    def confirm_submit(self):
        """
        confirm submit order

        _json_at
        choose_seats
        dwAll
        key_check_isChange
        leftTicketStr
        oldPassengerStr
        passengerTicketStr
        purpose_codes
        randCode
        REPEAT_SUBMIT_TOKEN
        roomType
        seatDetailType
        train_location
        whatsSelect

        :return:
        """
        request_url = self.queue_count.get('request_url')
        request_params = self.queue_count.get('params')
        request_params['oldPassengerStr'] = ''
        request_params[''] = ''
        request_params[''] = ''
        request_params[''] = ''
        request_params[''] = ''
        request_params[''] = ''
        request_params[''] = ''
        request_params[''] = ''
        request_params[''] = ''
        request_params[''] = ''

        confirm_submit_response = api.post(request_url, body=request_params, headers=headers)
        if confirm_submit_response.status_code == 200:
            log.info(confirm_submit_response.json())
        else:
            log.error('confirm_submit error')

    def __str__(self):
        return '[乘车人: %s, 出发站: %s, 到达站: %s, 车次: %s, 座位: %s, 出发时间: %s %s:00]' % (
            self.passenger_name, self.from_station, self.to_station, self.train_no, self.seat_type, self.date,
            self.ticket.leave_time)


if __name__ == '__main__':
    order = Order()
    print(order)
    order.submit()
