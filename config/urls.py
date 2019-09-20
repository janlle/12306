# coding:utf-8

URLS = {
    "login": {
        "request_url": "http://kyfw.12306.cn/passport/web/login",
        "method": "post",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "page": "https://kyfw.12306.cn/otn/resources/login.html",
        "params": {"username": "", "password": "", "appid": "otn", "answer": ""}
    },
    "validate_captcha": {
        "request_url": "https://kyfw.12306.cn/passport/captcha/captcha-check?answer={}&rand=sjrand&login_site=E&_={}",
        "method": "get",
        "Content-Type": "",
        "page": "https://kyfw.12306.cn/otn/resources/login.html",
        "params": {"answer": "", "rand": "", "login_site": "otn"}
    },
    "captcha": {
        "request_url": "https://kyfw.12306.cn/passport/captcha/captcha-image64",
        "method": "get",
        "Content-Type": "",
        "page": "https://kyfw.12306.cn/otn/resources/login.html",
        "params": {}
    },
    "ticket_query": {
        "request_url": "https://kyfw.12306.cn/otn/leftTicket/queryA",
        "method": "get",
        "Content-Type": "",
        "page": "https://kyfw.12306.cn/otn/resources/login.html",
        "params": {
            "leftTicketDTO.train_date": "",
            "leftTicketDTO.from_station": "",
            "leftTicketDTO.to_station": "",
            "purpose_codes": "",
        }
    }

}
