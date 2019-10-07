# coding:utf-8

URLS = {
    'login': {
        'request_url': 'http://kyfw.12306.cn/passport/web/login',
        'method': 'post',
        'params': {'username': '', 'password': '', 'appid': 'otn', 'answer': ''}
    },
    'validate_captcha': {
        'request_url': 'https://kyfw.12306.cn/passport/captcha/captcha-check?answer={}&rand=sjrand&login_site=E&_={}',
        'method': 'get'
    },
    'captcha_url': {
        'request_url': 'https://kyfw.12306.cn/passport/captcha/captcha-image64',
        'method': 'get'
    },
    'ticket_query': {
        'request_url': 'https://kyfw.12306.cn/otn/leftTicket/queryA',
        'method': 'get',
        'params': {
            'leftTicketDTO.train_date': '',
            'leftTicketDTO.from_station': '',
            'leftTicketDTO.to_station': '',
            'purpose_codes': '',
        }
    },
    'submit_order': {
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
            '_json_att': ''
        }
    },
    'confirm_passenger': {
        'request_url': 'https://kyfw.12306.cn/otn/confirmPassenger/initDc',
        'method': 'get'
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
        'request_url': 'https://kyfw.12306.cn/otn/HttpZF/logdevice?algID=fn5Y5BgTab&hashCode=xhF0ZDOw2W6GrtIBda-3GOblbRIfvp-Lw4dBoOfOy6U&FMQw=1&q4f3=zh-CN&VySQ=FGEvoin1a9U8qqP49kc9pmG2mUA2BUP3&VPIf=1&custID=133&VEek=unknown&dzuS=0&yD16=0&EOQP=382b3eb7cfc5d30f1b59cb283d1acaf3&lEnu=3232261143&jp76=52d67b2a5aa5e031084733d5006cc664&hAqN=Linux%20x86_64&platform=WEB&ks0Q=d22ca0b81584fbea62237b14bd04c866&TeRS=1003x1920&tOHY=24xx1080x1920&Fvje=i1l1o1s1&q5aJ=-8&wNLf=99115dfb07133750ba677d055874de87&0aew={}&timestamp={}',
        'method': 'get'
    }

}

submitUrls = {
    'dc': {
        'submitOrderRequest': {
            'url': r'https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest',
            'method': 'POST',
            'headers': {
                'Referer': 'https://kyfw.12306.cn/otn/leftTicket/init',
                'Content-Type': r'application/x-www-form-urlencoded; charset=UTF-8',
                'Host': r'kyfw.12306.cn',
                'X-Requested-With': 'XMLHttpRequest',
                'Origin': 'https://kyfw.12306.cn',
            },
        },
        'getPassengerDTOs': {
            'url': r'https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs',
            'method': 'POST',
        },
        'getExtraInfo': {
            'url': r'https://kyfw.12306.cn/otn/confirmPassenger/initDc',
            'method': 'POST',
            'headers': {
                'Referer': 'https://kyfw.12306.cn/otn/leftTicket/init',
                'Host': r'kyfw.12306.cn',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
            },
            'response': 'html',
        },
        'checkUser': {
            'url': r'https://kyfw.12306.cn/otn/login/checkUser',
            'method': 'POST',
            'headers': {
                'Referer': r'https://kyfw.12306.cn/otn/leftTicket/init',
                'Content-Type': r'application/x-www-form-urlencoded; charset=UTF-8',
            }
        },
        'checkOrderInfo': {
            'url': r'https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo',
            'method': 'POST',
            'headers': {
                'Referer': r'https://kyfw.12306.cn/otn/confirmPassenger/initDc',
            },
        },
        'getQueueCount': {
            'url': r'https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount',
            'method': 'POST',
            'headers': {
                'Referer': r'https://kyfw.12306.cn/otn/confirmPassenger/initDc',
            },
        },
        'confirmForQueue': {
            'url': r'https://kyfw.12306.cn/otn/confirmPassenger/confirmSingleForQueue',
            'method': 'POST',
            'headers': {
                'Referer': r'https://kyfw.12306.cn/otn/confirmPassenger/initDc',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            },
        },
        'queryOrderWaitTime': {
            'url': r'https://kyfw.12306.cn/otn/confirmPassenger/queryOrderWaitTime',
            'method': 'GET',
            'headers': {
                'Referer': r'https://kyfw.12306.cn/otn/confirmPassenger/initDc',
            },
        },
        'resultOrderForQueue': {
            'url': r'https://kyfw.12306.cn/otn/confirmPassenger/resultOrderForDcQueue',
            'method': 'POST',
            'headers': {
                'Referer': r'https://kyfw.12306.cn/otn/confirmPassenger/initDc',
            },
        },
        'queryMyOrderNoComplete': {
            'url': r'https://kyfw.12306.cn/otn/queryOrder/queryMyOrderNoComplete',
            'method': 'POST',
            'headers': {
                'Referer': r'https://kyfw.12306.cn/otn/queryOrder/initNoComplete',
            },
        }

    }
}
