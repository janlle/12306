# coding:utf-8

# ====================== 必填项 ======================
# 账号
ACCOUNT = 'xxx'

# 密码
PASSWORD = 'xxx'

# 出发站
FROM_STATION = '武昌'

# 到达站
TO_STATION = '长沙'

# 出发时间,例如: 2019-10-15
DATE = '2019-10-15'

# 乘车人
USER = ['xxx']

# ====================== 非必填项 ======================

# 车次(车次未填写会选择当天最早的一个车次下单)
TRAINS_NO = ['K81']

# 座位类别: 商务座(9),特等座(P),一等座(M),二等座(O),高级软卧(6),软卧(4),硬卧(3),软座(2),硬座(1),无座(1) (未填会选择随机选择)
SEAT_TYPE_CODE = ['1']

# 通知手机号
PHONE = ''
