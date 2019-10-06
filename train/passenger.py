# coding:utf8


class Passenger(object):

    def __init__(self):
        self._passenger_name = '',
        self._sex_code = '',
        self._sex_name = '',
        self._born_date = '',
        self._country_code = '',
        self._passenger_id_type_code = '',
        self._passenger_id_type_name = '',
        self._passenger_id_no = '',
        self._passenger_type = '',
        self._passenger_flag = '',
        self._passenger_type_name = '',
        self._mobile_no = '',
        self._phone_no = '',
        self._email = '',
        self._first_letter = '',
        self._total_times = '',
        self._index_id = '',
        self._all_enc_str = '',

    @property
    def passenger_name(self):
        return self._passenger_name

    @passenger_name.setter
    def passenger_name(self, value):
        self._passenger_name = value

    @property
    def sex_code(self):
        return self._sex_code

    @sex_code.setter
    def sex_code(self, value):
        self._sex_code = value

    @property
    def sex_name(self):
        return self._sex_name

    @sex_name.setter
    def sex_name(self, value):
        self._sex_name = value

    @property
    def born_date(self):
        return self._born_date

    @born_date.setter
    def born_date(self, value):
        self._born_date = value

    @property
    def country_code(self):
        return self._country_code

    @country_code.setter
    def country_code(self, value):
        self._country_code = value

    @property
    def passenger_id_type_code(self):
        return self._passenger_id_type_code

    @passenger_id_type_code.setter
    def passenger_id_type_code(self, value):
        self._passenger_id_type_code = value

    @property
    def passenger_id_type_name(self):
        return self._passenger_id_type_name

    @passenger_id_type_name.setter
    def passenger_id_type_name(self, value):
        self._passenger_id_type_name = value

    @property
    def passenger_id_no(self):
        return self._passenger_id_no

    @passenger_id_no.setter
    def passenger_id_no(self, value):
        self._passenger_id_no = value

    @property
    def passenger_type(self):
        return self._passenger_type

    @passenger_type.setter
    def passenger_type(self, value):
        self._passenger_type = value

    @property
    def passenger_flag(self):
        return self._passenger_flag

    @passenger_flag.setter
    def passenger_flag(self, value):
        self._passenger_flag = value

    @property
    def passenger_type_name(self):
        return self._passenger_type_name

    @passenger_type_name.setter
    def passenger_type_name(self, value):
        self._passenger_type_name = value

    @property
    def mobile_no(self):
        return self._mobile_no

    @mobile_no.setter
    def mobile_no(self, value):
        self._mobile_no = value

    @property
    def phone_no(self):
        return self._phone_no

    @phone_no.setter
    def phone_no(self, value):
        self._phone_no = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = value

    @property
    def first_letter(self):
        return self._first_letter

    @first_letter.setter
    def first_letter(self, value):
        self._first_letter = value

    @property
    def total_times(self):
        return self._total_times

    @total_times.setter
    def total_times(self, value):
        self._total_times = value

    @property
    def index_id(self):
        return self._index_id

    @index_id.setter
    def index_id(self, value):
        self._index_id = value

    @property
    def all_enc_str(self):
        return self._all_enc_str

    @all_enc_str.setter
    def all_enc_str(self, value):
        self._all_enc_str = value

    def __str__(self):
        return '[name: %s, ' \
               'sex: %s, ' \
               'birth: %s, ' \
               'id_card: %s, ' \
               'phone: %s, ' \
               'email: %s, ' \
               'passenger_type: %s]' % (self.passenger_name or '',
                                        self.sex_name or '',
                                        self.born_date or '',
                                        self.passenger_id_no or '',
                                        self.mobile_no or '',
                                        self.email or '',
                                        self.passenger_type or '')

    __repr__ = __str__

    def old_passenger_str(self):
        """
        姓名,证件类别,证件号码,
        张三,1,4201***********130,1_
        :return:
        """
        return '%s,%s,%s,%s_' % (
            self.passenger_name or '', self.passenger_id_type_code or '', self.passenger_id_no or '',
            self.passenger_type or '')

    def passenger_ticket_str(self, seat_type):
        """
        座位类型,0,车票类型，姓名，身份正号，电话，N（多个的话，以逗号分隔）
        1,0,1,张三,1,4201***********130,15915642596,N,1e41e00b84cd034d45539fde97af937536f5b28216780a8dd64475afff4e6f2d6e904c90c9c2035d221f9d356b81f8fb
        :param seat_type: seat type
        :return:
        """
        return '%s,%s,%s,%s,%s,%s,%s,%s,%s' % (
            seat_type, 0, self.passenger_type or '', self.passenger_name or '', self.passenger_id_type_code or '',
            self.passenger_id_no, self.mobile_no or '', 'N',
            self.all_enc_str or '')
