# -*- coding: utf-8 -*-
# @Time    : 2023/6/2 15:22
# @Author  : lzc
# @Email   : hybpjx@163.com
# @File    : m1.py
# @Software: PyCharm
# @blog    : https://www.cnblogs.com/zichliang
import requests
import execjs


def get_data(page):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
    }
    cookies = {
        "sessionid": "1u3ymswmdy00oo4vm2smjuhwg5tg31ty",
    }

    ctx = execjs.compile(open("m1.js", 'r', encoding="utf-8").read())

    payload = ctx.call("call", page)
    print(f"生成的加密payload:{payload}")
    url = f"https://match2023.yuanrenxue.cn/api/match2023/1"
    result = requests.post(url, headers=headers, data=payload, cookies=cookies).json()
    print(result)
    return sum([i['value'] for i in result['data']])


if __name__ == '__main__':
    num = 0
    for i in range(1, 6):
        num += get_data(i)
    print(f"最后结果为:{num}")
