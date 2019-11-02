# coding:utf-8

"""
封装车票信息实体
"""


class Ticket(object):

    def __init__(self):
        self._train_no = ''
        self._from_station = ''
        self._start_station = ''
        self._end_station = ''
        self._to_station = ''
        self._start_station_code = ''
        self._end_station_code = ''
        self._from_station_code = ''
        self._to_station_code = ''
        self._total_consume = ''
        self._leave_time = ''
        self._arrive_time = ''

        self._business_seat = ''
        self._first_class_seat = ''
        self._second_class_seat = ''
        self._advanced_soft_sleep = ''
        self._soft_sleep = ''
        self._move_sleep = ''
        self._hard_sleep = ''
        self._soft_seat = ''
        self._hard_seat = ''
        self._no_seat = ''

        self._other = ''
        self._mark = ''
        self._passenger_type = ''
        self._secret_str = ''
        self._start_date = ''

        self._seat_type = ''
        self._seat_count = 0

    def get_seat_level(self, level):
        """
        商务座(9), 一等座(8), 二等座(7), 高级软卧(6), 软卧(5), 动卧(4), 硬卧(3), 软座(2), 硬座(1), 无座(0)
        :return:
        """
        result = []
        seat_map = {
            0: self.no_seat,
            1: self.hard_seat,
            2: self.soft_seat,
            3: self.hard_sleep,
            4: self.move_sleep,
            5: self.soft_sleep,
            6: self.advanced_soft_sleep,
            7: self.second_class_seat,
            8: self.first_class_seat,
            9: self.business_seat
        }
        level.sort(reverse=True)
        for l in level:
            result.append({'train_no': self.train_no, 'type': l, 'usable': seat_map.get(l, 0)})
        return result

    @staticmethod
    def get_seat_name(key):
        """
        商务座(9), 一等座(8), 二等座(7), 高级软卧(6), 软卧(5), 动卧(4), 硬卧(3), 软座(2), 硬座(1), 无座(0)
        :param key:
        :return:
        """
        seat_map = {
            0: '无座',
            1: '硬座',
            2: '软座',
            3: '硬卧',
            4: '动卧',
            5: '软卧',
            6: '高级软卧',
            7: '二等座',
            8: '一等座',
            9: '商务座'
        }
        return seat_map.get(key)

    @property
    def train_no(self):
        return self._train_no

    @train_no.setter
    def train_no(self, value):
        self._train_no = value

    @property
    def from_station(self):
        return self._from_station

    @from_station.setter
    def from_station(self, value):
        self._from_station = value

    @property
    def to_station(self):
        return self._to_station

    @to_station.setter
    def to_station(self, value):
        self._to_station = value

    @property
    def start_station(self):
        return self._start_station

    @start_station.setter
    def start_station(self, value):
        self._start_station = value

    @property
    def end_station(self):
        return self._end_station

    @end_station.setter
    def end_station(self, value):
        self._end_station = value

    #  start_station_code:起始站：4
    @property
    def start_station_code(self):
        return self._start_station_code

    @start_station_code.setter
    def start_station_code(self, value):
        self._start_station_code = value

    #  end_station_code终点站：5
    @property
    def end_station_code(self):
        return self._end_station_code

    @end_station_code.setter
    def end_station_code(self, value):
        self._end_station_code = value

    #  from_station_code:出发站：6
    @property
    def from_station_code(self):
        return self._from_station_code

    @from_station_code.setter
    def from_station_code(self, value):
        self._from_station_code = value

    #  to_station_code:到达站：7
    @property
    def to_station_code(self):
        return self._to_station_code

    @to_station_code.setter
    def to_station_code(self, value):
        self._to_station_code = value

    #  start_time:出发时间：8
    @property
    def leave_time(self):
        return self._leave_time

    @leave_time.setter
    def leave_time(self, value):
        self._leave_time = value

    #  arrive_time:达到时间：9
    @property
    def arrive_time(self):
        return self._arrive_time

    @arrive_time.setter
    def arrive_time(self, value):
        self._arrive_time = value

    #  历时：10
    @property
    def total_consume(self):
        return self._total_consume

    @total_consume.setter
    def total_consume(self, value):
        self._total_consume = value

    #  商务特等座：32
    @property
    def business_seat(self):
        return self._business_seat

    @business_seat.setter
    def business_seat(self, value):
        if value == '':
            self._business_seat = '--'
        elif value == '无':
            self._business_seat = 'no'
        elif value == '有':
            self._business_seat = 'yes'
        else:
            self._business_seat = value

    #  一等座：31
    @property
    def first_class_seat(self):
        return self._first_class_seat

    @first_class_seat.setter
    def first_class_seat(self, value):
        if value == '':
            self._first_class_seat = '--'
        elif value == '无':
            self._first_class_seat = 'no'
        elif value == '有':
            self._first_class_seat = 'yes'
        else:
            self._first_class_seat = value

    #  二等座：30
    @property
    def second_class_seat(self):
        return self._second_class_seat

    @second_class_seat.setter
    def second_class_seat(self, value):
        if value == '':
            self._second_class_seat = '--'
        elif value == '无':
            self._second_class_seat = 'no'
        elif value == '有':
            self._second_class_seat = 'yes'
        else:
            self._second_class_seat = value

    #  高级软卧：21
    @property
    def advanced_soft_sleep(self):
        return self._advanced_soft_sleep

    @advanced_soft_sleep.setter
    def advanced_soft_sleep(self, value):
        if value == '':
            self._advanced_soft_sleep = '--'
        elif value == '无':
            self._advanced_soft_sleep = 'no'
        elif value == '有':
            self._advanced_soft_sleep = 'yes'
        else:
            self._advanced_soft_sleep = value

    #  软卧：23
    @property
    def soft_sleep(self):
        return self._soft_sleep

    @soft_sleep.setter
    def soft_sleep(self, value):
        if value == '':
            self._soft_sleep = '--'
        elif value == '无':
            self._soft_sleep = 'no'
        elif value == '有':
            self._soft_sleep = 'yes'
        else:
            self._soft_sleep = value

    #  动卧：33
    @property
    def move_sleep(self):
        return self._move_sleep

    @move_sleep.setter
    def move_sleep(self, value):
        if value == '':
            self._move_sleep = '--'
        elif value == '无':
            self._move_sleep = 'no'
        elif value == '有':
            self._move_sleep = 'yes'
        else:
            self._move_sleep = value

    #  硬卧：28
    @property
    def hard_sleep(self):
        return self._hard_sleep

    @hard_sleep.setter
    def hard_sleep(self, value):
        if value == '':
            self._hard_sleep = '--'
        elif value == '无':
            self._hard_sleep = 'no'
        elif value == '有':
            self._hard_sleep = 'yes'
        else:
            self._hard_sleep = value

    #  软座：24
    @property
    def soft_seat(self):
        return self._soft_seat

    @soft_seat.setter
    def soft_seat(self, value):
        if value == '':
            self._soft_seat = '--'
        elif value == '无':
            self._soft_seat = 'no'
        elif value == '有':
            self._soft_seat = 'yes'
        else:
            self._soft_seat = value

    #  硬座：29
    @property
    def hard_seat(self):
        return self._hard_seat

    @hard_seat.setter
    def hard_seat(self, value):
        if value == '':
            self._hard_seat = '--'
        elif value == '无':
            self._hard_seat = 'no'
        elif value == '有':
            self._hard_seat = 'yes'
        else:
            self._hard_seat = value

    #  无座：26
    @property
    def no_seat(self):
        return self._no_seat

    @no_seat.setter
    def no_seat(self, value):
        if value == '':
            self._no_seat = '--'
        elif value == '无':
            self._no_seat = 'no'
        elif value == '有':
            self._no_seat = 'yes'
        else:
            self._no_seat = value

    #  其他：22
    @property
    def other(self):
        return self._other

    @other.setter
    def other(self, value):
        self._other = value

    #  备注：1
    @property
    def mark(self):
        return self._mark

    @mark.setter
    def mark(self, value):
        self._mark = value

    @property
    def passenger_type(self):
        return self._passenger_type

    @passenger_type.setter
    def passenger_type(self, value):
        self._passenger_type = value

    @property
    def secret_str(self):
        return self._secret_str

    @secret_str.setter
    def secret_str(self, value):
        self._secret_str = value

    @property
    def start_date(self):
        return self._start_date

    @start_date.setter
    def start_date(self, value):
        self._start_date = value

    @property
    def seat_type(self):
        return self._seat_type

    @seat_type.setter
    def seat_type(self, value):
        self._seat_type = value

    @property
    def seat_count(self):
        return self._seat_count

    @seat_count.setter
    def seat_count(self, value):
        self._seat_count = value

    def __str__(self):
        return '[车次: %s, 出发站: %s, 到达站: %s, 出发时间: %s, 到达时间: %s]' % (
            self.train_no, self.from_station, self.to_station, self.leave_time, self.arrive_time)

    @staticmethod
    def get_display_title():
        return ["车次", "出发站", "到达站", "出发时间", "到达时间"]

    def get_display_field(self):
        return [self.train_no, self.from_station, self.to_station, self.leave_time, self.arrive_time]

    __repr__ = __str__
