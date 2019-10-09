# coding:utf-8

URLS = {
    'login_url': {
        'request_url': 'http://kyfw.12306.cn/passport/web/login',
        'method': 'post',
        'headers': {
            'Referer': 'https://kyfw.12306.cn/otn/resources/login.html',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://kyfw.12306.cn'
        },
        'params': {'username': '', 'password': '', 'appid': 'otn', 'answer': ''}
    },
    'check_captcha_url': {
        'request_url': 'https://kyfw.12306.cn/passport/captcha/captcha-check?answer={}&rand=sjrand&login_site=E&_={}',
        'method': 'get'
    },
    'captcha_url': {
        'request_url': 'https://kyfw.12306.cn/passport/captcha/captcha-image64',
        'method': 'get'
    },
    'ticket_query': {
        'request_url': 'https://kyfw.12306.cn/otn/leftTicket/query',
        'method': 'get',
        'params': {
            'leftTicketDTO.train_date': '',
            'leftTicketDTO.from_station': '',
            'leftTicketDTO.to_station': '',
            'purpose_codes': '',
        }
    },
    'submit_order_request_url': {
        'request_url': 'https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest',
        'method': 'post',
        'params': {
            'secretStr': '',
            'train_date': '',
            'back_train_date': '',
            'tour_flag': 'dc',
            'purpose_codes': 'ADULT',
            'query_from_station_name': '',
            'query_to_station_name': '',
            'undefined': '',
        }
    },
    'check_order_info': {
        'request_url': 'https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo',
        'method': 'post',
        'params': {
            'bed_level_order_num': '000000000000000000000000000000',
            'passengerTicketStr': '',
            'oldPassengerStr': '',
            'tour_flag': 'dc',
            'randCode': '',
            'cancel_flag': '2',
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': ''
        }
    },
    'passenger_url': {
        'request_url': 'https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs',
        'method': 'post',
        'params': {
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': ''
        }
    },
    'init_dc_url': {
        'request_url': 'https://kyfw.12306.cn/otn/confirmPassenger/initDc',
        'method': 'post',
        'params': {
            '_json_att': ''
        }
    },
    'queue_count': {
        'request_url': 'https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount',
        'method': 'post',
        'params': {
            'train_date': '',
            'train_no': '',
            'stationTrainCode': '',
            'seatType': '',
            'fromStationTelecode': '',
            'toStationTelecode': '',
            'leftTicket': '',
            'purpose_codes': '',
            'train_location': '',
            'REPEAT_SUBMIT_TOKEN': '',
        }
    },
    'confirm_submit_url': {
        'request_url': 'https://kyfw.12306.cn/otn/confirmPassenger/confirmSingleForQueue',
        'method': 'post',
        'params': {
            '_json_at': '',
            'choose_seats': '',
            'dwAll': 'N',
            'key_check_isChange': '',
            'leftTicketStr': '',
            'oldPassengerStr': '',
            'passengerTicketStr': '',
            'purpose_codes': '',
            'randCode': '',
            'REPEAT_SUBMIT_TOKEN': '',
            'roomType': '00',
            'seatDetailType': '',
            'train_location': '',
            'whatsSelect': '1',
        }
    },
    'order_callback_url': {
        'request_url': 'https://kyfw.12306.cn/otn/confirmPassenger/queryOrderWaitTime?random={}&tourFlag={}&_json_att=',
        'method': 'get'
    },
    'check_login_url': {
        'request_url': 'https://kyfw.12306.cn/passport/web/auth/uamtk-static',
        'method': 'post',
        'params': {
            'appid': 'otn'
        }
    },
    'devices_id_url': {
        'request_url': 'https://kyfw.12306.cn/otn/HttpZF/logdevice?algID=WAa2rRuEOC&hashCode=t2O-sbPQxNjhorFZrexFYyG4eedlw15daI4Rbi-aKkM&FMQw=0&q4f3=en-US&VPIf=1&custID=133&VEek=unknown&dzuS=0&yD16=0&EOQP=8f58b1186770646318a429cb33977d8c&jp76=52d67b2a5aa5e031084733d5006cc664&hAqN=Win32&platform=WEB&ks0Q=d22ca0b81584fbea62237b14bd04c866&TeRS=1040x1920&tOHY=24xx1080x1920&Fvje=i1l1o1s1&q5aJ=-8&wNLf=99115dfb07133750ba677d055874de87&0aew=Mozilla/5.0%20(Windows%20NT%2010.0;%20Win64;%20x64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/77.0.3865.90%20Safari/537.36&E3gR=c9702ebf7b800d228a580c2897681aca&timestamp={}',
        'method': 'get'
    },
    'conf_url': {
        'request_url': 'https://kyfw.12306.cn/otn/login/conf',
        'method': 'post'
    },
    'iconfont_url': {
        'request_url': 'https://www.12306.cn/index/fonts/iconfont.ttf?t={}',
        'method': 'get'
    },
    'free_proxy_url': {
        'request_url': 'https://free-proxy-list.net/'
    },
    'uamtk_url': {
        'request_url': 'https://kyfw.12306.cn/passport/web/auth/uamtk',
        'method': 'post',
        'params': {
            'appid': 'otn'
        }
    },
    'uamauthclient_url': {
        'request_url': 'https://kyfw.12306.cn/otn/uamauthclient',
        'method': 'post',
        'params': {
            'tk': ''
        }
    },
    'unfinished_order_url': {
        'request_url': 'https://kyfw.12306.cn/otn/queryOrder/queryMyOrderNoComplete',
        'method': 'post',
        'params': {
            '_json_att': ''
        }
    }

}
