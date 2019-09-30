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
        self._address = '',
        self._postalcode = '',
        self._first_letter = '',
        self._recordCount = '',
        self._total_times = '',
        self._index_id = '',
        self._allEncStr = '',
        self._isAdult = '',
        self._isYongThan10 = '',
        self._isYongThan14 = '',
        self._isOldThan60 = '',
        self._gat_born_date = '',
        self._gat_valid_date_start = '',
        self._gat_valid_date_end = '',
        self._gat_version = ''

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
    def address(self):
        return self._address

    @address.setter
    def address(self, value):
        self._address = value

    @property
    def postalcode(self):
        return self._postalcode

    @postalcode.setter
    def postalcode(self, value):
        self._postalcode = value

    @property
    def first_letter(self):
        return self._first_letter

    @first_letter.setter
    def first_letter(self, value):
        self._first_letter = value

    @property
    def recordCount(self):
        return self._recordCount

    @recordCount.setter
    def recordCount(self, value):
        self._recordCount = value

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

    def __str__(self):
        return '[name: %s,' \
               'sex: %s' \
               'birth: %s' \
               'id: %s' \
               'phone: %s' \
               'email: %s' \
               'passengerType: %s]' % (self._passenger_name or '',
                                       self._sex_name or '',
                                       self._born_date or '',
                                       self._passenger_id_no or '',
                                       self._mobile_no or '',
                                       self._email or '',
                                       self._passenger_type or '')

    __repr__ = __str__
