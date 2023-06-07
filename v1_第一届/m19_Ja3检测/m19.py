# -*- coding: utf-8 -*-
# @Time    : 2023/5/29 11:23
# @Author  : lzc
# @Email   : hybpjx@163.com
# @File    : m19.py
# @Software: PyCharm
# @blog    : https://www.cnblogs.com/zichliang
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.ssl_ import create_urllib3_context

# This is the 2.11 Requests cipher string, containing 3DES.
CIPHERS = (
    'ECDH+AESGCM:DH+AESGCM:ECDH+AES256:RSA+3DES:!aNULL:'
    '!eNULL:!MD5'
)
headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'user-agent': 'yuanrenxue.project',
    'x-requested-with': 'XMLHttpRequest',
    'cookie': 'sessionid=0c663ochdm65kj1ush13txto1jkojn3d'
}


class DESAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = create_urllib3_context(ciphers=CIPHERS)
        kwargs['ssl_context'] = context
        return super(DESAdapter, self).init_poolmanager(*args, **kwargs)

    def proxy_manager_for(self, *args, **kwargs):
        context = create_urllib3_context(ciphers=CIPHERS)
        kwargs['ssl_context'] = context
        return super(DESAdapter, self).proxy_manager_for(*args, **kwargs)


def get_page(s, page):
    r = s.get(f'https://match.yuanrenxue.cn/api/match/19?page={page}', headers=headers)
    res = r.json()
    print(res)
    data = res.get('data')
    s = [int(d.get('value')) for d in data]
    # print(123123, s)
    return s


def get_data(s):
    end = 0
    for i in range(1, 6):
        temp = get_page(s, i)

        end += sum(temp)
    print('end', end)
    return end


if __name__ == '__main__':
    s = requests.Session()
    s.mount('https://match.yuanrenxue.cn', DESAdapter())
    get_data(s)