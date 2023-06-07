# -*- coding: utf-8 -*-
# @Time    : 2023/5/29 14:40
# @Author  : lzc
# @Email   : hybpjx@163.com
# @File    : m17.py
# @Software: PyCharm
# @blog    : https://www.cnblogs.com/zichliang
import httpx

headers = {
    "user-agent": "yuanrenxue.project",
    "x-requested-with": "XMLHttpRequest"
}
cookies = {
    "sessionid": "0c663ochdm65kj1ush13txto1jkojn3d",
}


def get_data(page):
    url = "https://match.yuanrenxue.cn/api/match/17"
    params = {
        "page": str(page)
    }
    with httpx.Client(headers=headers, http2=True, cookies=cookies) as client:
        s = client.get(url, params=params)

        return sum([data['value'] for data in s.json()["data"]])


if __name__ == '__main__':
    all_count = 0
    for i in range(1, 6):
        all_count += get_data(i)
    print("总数字等于>>>>", all_count)
