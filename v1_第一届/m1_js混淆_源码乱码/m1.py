# -*- coding: utf-8 -*-
# @Time    : 2023/5/25 13:26
# @Author  : lzc
# @Email   : hybpjx@163.com
# @File    : m1.py
# @Software: PyCharm
# @blog    : https://www.cnblogs.com/zichliang

import time

import requests
import execjs

t = int(time.time()) * 1000 + 100000000


def get_sign():
    node = execjs.get()

    with open('m1.js', encoding='utf-8') as f:
        js_code = f.read()

    # 编译js代码
    ctx = node.compile(js_code)  # compile方法去加载js代码，参数cwd指定本地安装模块所在目录
    # 执行js函数，返回值给变量
    data1 = ctx.call("hex_md5", str(t))
    return data1


def get_data():
    headers = {
        'user-agent': 'yuanrenxue.project',
    }

    all_price = 0
    all_count = 0
    for i in range(1, 6):
        params = (
            ('page', i),
            ('m', get_sign() + "丨" + str(int(t / 1000))),
        )
        response = requests.get('https://match.yuanrenxue.com/api/match/1', headers=headers, params=params)
        price = 0
        count = len(response.json()["data"])
        for data in response.json()["data"]:
            price += data['value']

        all_price += price
        all_count += count

    print(all_price / all_count)


get_data()