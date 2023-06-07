# -*- coding: utf-8 -*-
# @Time    : 2023/5/29 13:45
# @Author  : lzc
# @Email   : hybpjx@163.com
# @File    : m15.py
# @Software: PyCharm
# @blog    : https://www.cnblogs.com/zichliang
import json
import math
import random
import time
import requests

import pywasm


def env_abort(_: pywasm.Ctx):
    return


def get_time():
    t = int(time.time())
    t1 = int(t / 2)
    t2 = int(t / 2 - math.floor(random.random() * 50 + 1))
    return t1, t2


def get_params_m():
    t1, t2 = get_time()

    runtime = pywasm.load('main.wasm', {
        'env': {
            'abort': env_abort,
        }
    })

    r = runtime.exec('encode', [t1, t2])

    return str(r) + '|' + str(t1) + '|' + str(t2)


def get_data(page):
    headers = {
        "authority": "match.yuanrenxue.cn",
        "accept": "application/json, text/javascript, */*; q=0.01",
        "User-Agent": "yuanrenxue.project",
        "x-requested-with": "XMLHttpRequest"
    }
    cookies = {
        "sessionid": "0c663ochdm65kj1ush13txto1jkojn3d",
    }
    url = "https://match.yuanrenxue.cn/api/match/15"

    m = get_params_m()

    params = {
        "m": m,
        "page": page
    }
    response = requests.get(url, headers=headers, cookies=cookies, params=params)
    try:
        sum_number = sum([data["value"] for data in response.json()['data']])
    except json.decoder.JSONDecodeError:
        print(response.text)
        return
    return sum_number


if __name__ == '__main__':
    total = 0
    for i in range(1, 6):
        total += get_data(i)
    print("总数字是>>>", total)
