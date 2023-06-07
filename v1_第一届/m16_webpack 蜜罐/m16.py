# -*- coding: utf-8 -*-
# @Time    : 2023/5/29 14:38
# @Author  : lzc
# @Email   : hybpjx@163.com
# @File    : m16.py
# @Software: PyCharm
# @blog    : https://www.cnblogs.com/zichliang
import time

import execjs
import requests
requests.packages.urllib3.disable_warnings()

headers = {
    "authority": "match.yuanrenxue.cn",
    "accept": "application/json, text/javascript, */*; q=0.01",
    "referer": "https://match.yuanrenxue.cn/match/16",
    "user-agent": "yuanrenxue.project",
}
cookies = {
    "sessionid":"0c663ochdm65kj1ush13txto1jkojn3d"
}
num = 0
for i in range(1, 6):
    url = "https://match.yuanrenxue.cn/api/match/16"
    timeStamp = int(time.time()) * 1000
    m = execjs.compile(open("m16.js", "r", encoding="utf-8").read()).call("getSDK", str(timeStamp))
    params = {
        "page": str(i),
        "m": m,
        "t": str(timeStamp)
    }
    response = requests.get(url, headers=headers, cookies=cookies, params=params, verify=False)
    # 投毒了
    try:
        for data in response.json()['data']:
            num += data['value']
    except:
        print(response.text)

print(num)
