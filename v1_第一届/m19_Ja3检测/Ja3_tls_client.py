# -*- coding: utf-8 -*-
# @Time    : 2023/6/14 15:02
# @Author  : lzc
# @Email   : hybpjx@163.com
# @File    : Ja3_tls_client.py
# @Software: PyCharm
# @blog    : https://www.cnblogs.com/zichliang
import tls_client

session = tls_client.Session(client_identifier="Chrome110", random_tls_extension_order=True)
session.headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "DNT": "1",
    "Pragma": "no-cache",
    "Referer": "http://192.168.2.10/",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.43",
    "sec-ch-ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Microsoft Edge\";v=\"114\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\""
}


def get_page(page):
    r = session.get(f'https://ggzy.jiangxi.gov.cn/xwdt/001002/sec1.html')
    print(r.text)

    res = r.json()
    data = res.get('data')
    # print(123123, s)
    return [int(d.get('value')) for d in data]


if __name__ == '__main__':
    end = 0
    for i in range(1, 6):
        temp = get_page(i)

        end += sum(temp)
    print('end', end)
