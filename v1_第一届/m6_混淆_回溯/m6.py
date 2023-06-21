# -*- coding: utf-8 -*-
# @Time    : 2023/6/9 14:59
# @Author  : lzc
# @Email   : hybpjx@163.com
# @File    : m6.py
# @Software: PyCharm
# @blog    : https://www.cnblogs.com/zichliang
import execjs
import requests


def get_list_value(page):
    ctx = execjs.compile(open("m6.js", 'r', encoding='utf-8').read())
    get_params = ctx.call("get_params", page)
    return get_params


def get_data(page):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.41",
    }
    cookies = {
        "sessionid": "2imsvfaefnpprkfzd0h4t8x3m3qwmuak",
    }
    url = "https://match.yuanrenxue.cn/api/match/6"

    p_l = get_list_value(page)

    params = {
        "page": page,
        "m": p_l['m'],
        "q": p_l['q']
    }
    res = requests.get(url, headers=headers, cookies=cookies, params=params)
    print(res.text)
    return [data['value'] for data in res.json()['data']]


'''
html += puq.replace('caipiaohao', caipiao)
    .replace('date_twice', arg * window.page + 2020097)
    .replace('date_value', '0' + window.page)
    .replace('result_value3', val.value)
    .replace('total_value', val.value * 24)
    .replace('result_value2', val.value * 8)
    .replace('result_value1', val.value * 15);
'''
if __name__ == '__main__':
    total_value = []
    for i in range(1, 6):
        total_value += get_data(i)
    #   根据第43行代码 可以看出来  总数 是x24
    print(f"全部中奖金额的总金额是>>>{sum(total_value) * 24}")
