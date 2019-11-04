# coding:utf-8

import bs4
import requests
from fake_useragent import UserAgent
from util.logger import Logger
from config.urls import URLS
from util.app_util import proxy_test, current_date_time
from util.sqlite_helper import SqliteHelper

log = Logger(__name__)


class ProxySpider(object):

    def __init__(self):
        self.free_proxy_url = URLS.get('free_proxy_url')
        self.proxy_list = []
        self.sqlite = SqliteHelper()

    def get_proxy_test(self):
        return list(filter(lambda l: l['enable'] == 'yes' and proxy_test(l), self.proxy_list))

    def save_proxy(self, proxy):
        # self.sqlite.execute('create table t_proxy (id integer primary key,ip varchar(48) UNIQUE, port integer, create_time varchar(48), enable tinyint)')
        # self.sqlite.execute('drop table t_proxy')
        # self.sqlite.insert('insert into t_proxy(ip, port, create_time, enable) values("129.205.160.111", "54789", "2019-09-23", 0)')
        self.sqlite.insert('insert into t_proxy(ip, port, create_time, enable) values("%s", %s, "%s", %d)' % (
            proxy['ip'], proxy['port'], current_date_time(), 0))

    def spider(self):
        self.proxy_list = []
        page_response = requests.get(self.free_proxy_url.get('request_url'), headers={'User-Agent': UserAgent().random})
        if page_response.status_code == 200:
            example_soup = bs4.BeautifulSoup(page_response.text, 'lxml')
            for b in example_soup.table.tbody:
                td_list = b.find_all('td')
                proxy = {'ip': td_list[0].text, 'port': td_list[1].text, 'enable': td_list[6].text}
                if proxy['enable'] == 'yes' and proxy_test(proxy):
                    log.info('save proxy: ' + str(proxy))
                    self.save_proxy(proxy=proxy)
                    self.proxy_list.append(proxy)

    def get_all_proxy(self):
        return self.sqlite.select('select * from t_proxy')

    def get_usable_proxy(self, count=1):
        result = []
        for p in self.get_all_proxy():
            if len(result) < count:
                if proxy_test({'ip': p['ip'], 'port': p['port']}):
                    result.append({'https': 'https://{}:{}'.format(p['ip'], p['port'])})
            else:
                break
        if not result:
            self.spider()
            return {'https': 'https://{}:{}'.format(self.proxy_list[0]['ip'], self.proxy_list[0]['port'])}
        return result

    def clear_ip_db(self):
        self.sqlite.delete('delete from t_proxy')


proxy = ProxySpider()

if __name__ == '__main__':
    print(proxy.get_usable_proxy(5))
