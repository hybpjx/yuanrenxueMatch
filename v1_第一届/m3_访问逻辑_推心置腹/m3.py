# -*- coding: utf-8 -*-
# @Time    : 2023/5/25 13:33
# @Author  : lzc
# @Email   : hybpjx@163.com
# @File    : m3.py
# @Software: PyCharm
# @blog    : https://www.cnblogs.com/zichliang
from collections import Counter

import requests

# 关闭ssl验证提示
from urllib3.exceptions import InsecureRequestWarning
import requests.packages.urllib3

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
headers = {
    'Host': 'match.yuanrenxue.cn',
    'Connection': 'keep-alive',
    'Content-Length': '0',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    'sec-ch-ua-platform': '"Windows"',
    'Accept': '*/*',
    'Origin': 'https://match.yuanrenxue.cn',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://match.yuanrenxue.cn/match/3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cookie': ''
}


def get_data(pageNum):
    session = requests.session()
    session.headers = headers
    params = {
        "page": str(pageNum)
    }
    res1 = session.post("https://match.yuanrenxue.com/jssm", verify=False)
    session.headers['Cookie'] = "sessionid=" + res1.cookies.get_dict()['sessionid']
    res2 = session.get("https://match.yuanrenxue.com/api/match/3", params=params)

    try:
        return [data['value'] for data in res2.json()["data"]]
    except:
        print(res2.text)
        print("某些headers参数错了 校验参数后再运行吧")
        exit(1)


if __name__ == '__main__':

    all_data = []
    set_data = {}
    for pageNum in range(1, 6):
        all_data.append(get_data(pageNum))

    for k in all_data:
        set_data[k] = all_data.count(k)
    cl = Counter(all_data)
    for k, v in cl.items():
        if v > 1:
            print("元素{}, 重复{}次".format(k, v))

    print(set_data)