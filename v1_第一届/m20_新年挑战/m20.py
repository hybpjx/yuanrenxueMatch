# -*- coding: utf-8 -*-
# @Time    : 2023/6/1 18:11
# @Author  : lzc
# @Email   : hybpjx@163.com
# @File    : m20.py
# @Software: PyCharm
# @blog    : https://www.cnblogs.com/zichliang
import execjs
import requests


def get_data(page):
    headers = {

        "user-agent": "yuanrenxue.project",
    }
    cookies = {
        "sessionid":"frsqeuf01p1y3faoisvp7xh1b0ot5gg6"
    }
    url = "https://match.yuanrenxue.cn/api/match/20"

    ctx = execjs.compile(open("m20.js", "r", encoding="utf-8").read())
    params_sign = ctx.call("sign", page)

    params = {
        "page": page,
        "sign": params_sign['sign'],
        "t": params_sign['t']
    }
    response = requests.get(url, headers=headers, cookies=cookies, params=params)
    data = response.json()['data']
    print(data)
    return sum([int(d.get('value')) for d in data])


if __name__ == '__main__':
    all_count = 0
    for i in range(1, 6):
        all_count += get_data(i)
    print("总数字等于>>>>", all_count)
