# coding:utf8

import config.urls as urls
import tickst_config as config
import util.logger as logger
import util.app_util as util
import requests
import time
from fake_useragent import UserAgent
from util.net_util import api
from verify import verify_code
from train import search_stack

headers = {
    "Cookie": "JSESSIONID=52FD5F844A88DD8C97ABCC97BAC2D19F; tk=otK-HoFzMYjocB-hyRPjTf1CpAS5T7lOsdw1w0; _jc_save_wfdc_flag=dc; _jc_save_fromStation=%u6B66%u660C%2CWCN; _jc_save_toStation=%u957F%u6C99%2CCSQ; BIGipServerotn=1257243146.38945.0000; BIGipServerpool_passport=183304714.50215.0000; RAIL_EXPIRATION=1570118166032; RAIL_DEVICEID=i9FsYRm1kJeeX2ebORk2ObIofE9MzyOhzd9d3YCMjOKgfw8tm_KAdtg0G1GOJMlyENKUtUH5ZMgkGc9-8rRY3_LnVONNLajjCchatRNaZVu8CLqBNgRUL6vvWRLbG_S5gbJ_-xyIXCiQJBx2O6Xf7xJ1ekv9rCG9; route=6f50b51faa11b987e576cdb301e545c4; _jc_save_fromDate=2019-10-25; _jc_save_toDate=2019-09-30"
}


class Order(object):

    def __init__(self):
        self.order_url = urls.URLS.get('submit_order')
        self.passenger = urls.URLS.get('passenger_url')
        self.check_order_info = urls.URLS.get('check_order_info')

    def prepare(self):
        pass

    def submit(self, ticket):
        """提交车票信息"""
        submit_url = self.order_url.get('request_url')
        ticket_params = self.order_url.get('params')
        ticket_params['back_train_date'] = util.current_date()
        ticket_params['train_date'] = config.DATE
        ticket_params['secretStr'] = util.decode_secret_str(ticket.secret_str)
        ticket_params['query_from_station_name'] = ticket.from_station
        ticket_params['query_to_station_name'] = ticket.to_station
        print(ticket_params)
        res = api.post(submit_url, ticket_params, headers=headers)
        print(res.status_code)
        print(res.json())

    def check_order(self):
        request_url = self.check_order_info.get('request_url')
        request_params = self.check_order_info.get('params')
        request_params['passengerTicketStr'] = ''
        request_params['oldPassengerStr'] = ''
        request_params['REPEAT_SUBMIT_TOKEN'] = ''
        pass

    def get_passenger(self, name=None):
        """获取账号的乘车人信息"""
        request_url = self.passenger.get('request_url')
        request_params = self.passenger.get('params')
        passengers_data = api.post(request_url, request_params, headers=headers)
        if passengers_data.status_code == 200:
            passengers = passengers_data.json()['data']['normal_passengers']
            if passengers and len(passengers) > 0:
                if name:
                    return list(filter(lambda p: p['passenger_name'] == name, passengers))
                else:
                    return passengers


if __name__ == '__main__':
    order = Order()
    res = order.get_passenger('xxx')
    print(res)
    # order.submit(search_stack.search_stack('武昌', '长沙', train_no='K81')[0])
