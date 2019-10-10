# coding:utf-8

# ====================== 必填项 ======================
# 账号
ACCOUNT = 'xxx'

# 密码
PASSWORD = 'xxx'

# 出发站
FROM_STATION = 'xxx'

# 到达站
TO_STATION = 'xxx'

# 出发时间,例如: 2019-10-15
DATE = '2019-11-03'

# 乘车人
USER = ['xxx']

# 车次
TRAINS_NO = ['xxx', 'xxx']

# ====================== 非必填项 ======================

# 座位类别: 商务座(9),一等座(9),二等座(7),高级软卧(6),软卧(5),动卧(4),硬卧(3),软座(2),硬座(1),无座(0) (未填会选择随机选择)
SEAT_TYPE = [1, 0, 3]

# 验证码识别方式（0：自动，1：手动）
CAPTCHA_IDENTIFY = 0

# 通知手机号
PHONE = ''
