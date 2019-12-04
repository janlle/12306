# 12306 

A fast Chinese railway ticket application.

[![12306](https://img.shields.io/badge/build-passing-green)](https://github.com/janlle/12306)
[![version](https://img.shields.io/badge/12306-1.0.0-orange)](https://github.com/janlle/12306)
[![issues](https://img.shields.io/badge/issues-open-blue)](https://github.com/janlle/12306/issues)

English | [简体中文](./README-zh_CN.md)

## Table of contents

- [Features](#Features)
- [Environment](#Environment)
- [Usage](#Usage)
- [Contributing](#Contributing)


## Features

- 1.Support fast ticket booking
- 2.Machine automatic identification verification code
- 3.Multi-person and multi-car purchase tickets
- 4.Very convenient and stable to use

## Environment

```shell script
System: Windows\Max\Linux
Python: 3.6
```

## Usage

First you need to create a virtual environment for Python3.6

1. Clone project code

```shell script
git clone https://github.com/janlle/12306.git 12306
cd 12306
```

2. Installation dependence

```shell script

python install -r requirements.txt

```

3. Run application

```shell script
python start.py
```

4. Running log

```buildoutcfg

[root@localhost 12306]# python start.py
Using TensorFlow backend.
Corrupt JPEG data: 17 extraneous bytes before marker 0xd9
2019-12-04 13:44:59,196 INFO      7675  [line: 29]: 题目为: ['樱桃']
2019-12-04 13:45:01,872 INFO      7675  [line: 29]: 选项1.茶几
2019-12-04 13:45:01,872 INFO      7675  [line: 29]: 选项2.电子秤
2019-12-04 13:45:01,872 INFO      7675  [line: 29]: 选项3.蒸笼
2019-12-04 13:45:01,873 INFO      7675  [line: 29]: 选项4.茶几
2019-12-04 13:45:01,873 INFO      7675  [line: 29]: 选项5.蒸笼
2019-12-04 13:45:01,873 INFO      7675  [line: 29]: 选项6.电子秤
2019-12-04 13:45:01,873 INFO      7675  [line: 29]: 选项7.樱桃
2019-12-04 13:45:01,873 INFO      7675  [line: 29]: 选项8.安全帽
2019-12-04 13:45:01,873 INFO      7675  [line: 29]: 答案为: ['7']
2019-12-04 13:45:02,439 INFO      7675  [line: 29]: 验证码校验成功
2019-12-04 13:45:02,805 INFO      7675  [line: 29]: 登录成功，共登录 1 次
2019-12-04 13:45:04,765 INFO      7675  [line: 29]: 验证通过，用户名: 张三
+------+-------------------+-----------------------+-------+--------+--------+--------+----------+------+------+------+------+------+------+
| 车次 | 出发站 - 到达站   | 出发时间 - 到达时间　 | 历时  | 商务座 | 一等座 | 二等座 | 高级软卧 | 软卧 | 动卧 | 硬卧 | 软座 | 硬座 | 无座 |
+------+-------------------+-----------------------+-------+--------+--------+--------+----------+------+------+------+------+------+------+
| Z89  | 武昌 - 长沙　　　 | 01:34 - 04:49         | 03:15 | --     | --     | --     | --       | no   | --   | 2    | --   | 8    | 2    |
+------+-------------------+-----------------------+-------+--------+--------+--------+----------+------+------+------+------+------+------+
2019-12-04 13:45:14,249 INFO      7675  [line: 29]: [乘车人: ['张三', '李四'], 出发站: 武昌, 到达站: 长沙, 车次: Z89, 座位: 硬卧, 出发时间: 2019-12-24 01:34:00]
2019-12-04 13:45:14,249 INFO      7675  [line: 29]: 车票订单提交成功，请稍后...
2019-12-04 13:45:14,866 INFO      7675  [line: 29]: 下单成功,请登录 12306 订单中心 -> 火车票订单 -> 未完成订单，支付订单!
[root@localhost 12306]# 

```

## Contributing

This is a open source project. Everyone is welcome to contribute their own code, gradually improve it thanks.