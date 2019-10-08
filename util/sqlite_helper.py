# coding:utf-8

from util.app_util import proxy_test, get_root_path
import sqlite3


class SqliteHelper(object):
    def __init__(self):
        self.conn = sqlite3.connect(get_root_path() + '/ip.db')
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

    def execute(self, sql):
        self.cursor.execute(sql)

    def insert(self, sql):
        self.execute(sql)
        self.conn.commit()

    def update(self, sql):
        self.execute(sql)
        self.conn.commit()

    def delete(self, sql):
        self.execute(sql)
        self.conn.commit()

    def select(self, sql):
        self.execute(sql)
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()
