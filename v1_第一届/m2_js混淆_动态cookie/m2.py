# -*- coding: utf-8 -*-
# @Time    : 2023/5/25 14:39
# @Author  : lzc
# @Email   : hybpjx@163.com
# @File    : m2.py
# @Software: PyCharm
# @blog    : https://www.cnblogs.com/zichliang
import execjs
import pandas as pd
import requests

headers = {
    "authority": "match.yuanrenxue.cn",
    "accept": "application/json, text/javascript, */*; q=0.01",
    "accept-language": "zh-CN,zh;q=0.9",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "referer": "https://match.yuanrenxue.cn/match/2",
    "sec-ch-ua": "\"Google Chrome\";v=\"113\", \"Chromium\";v=\"113\", \"Not-A.Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
    "x-requested-with": "XMLHttpRequest"
}


def get_cookie():
    ctx = execjs.compile(open("m2.js", "r", encoding="utf-8").read())
    cookies = {
        "m": ctx.call("getCookie")
    }
    return cookies


def get_data(page_num):
    cookies = get_cookie()
    url = "https://match.yuanrenxue.cn/api/match/2"

    if page_num == 1:
        params = {

        }
    else:
        params = {
            "page": page_num
        }
    print(cookies)
    response = requests.get(url, headers=headers, cookies=cookies, params=params)
    print(response.json())
    return [value['value'] for value in response.json()["data"]]


if __name__ == '__main__':
    total = 0
    for i in range(1, 6):
        total += sum(get_data(i))

    print(total)
