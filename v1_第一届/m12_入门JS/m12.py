# -*- coding: utf-8 -*-
# @Time    : 2023/5/29 13:53
# @Author  : lzc
# @Email   : hybpjx@163.com
# @File    : m12.py
# @Software: PyCharm
# @blog    : https://www.cnblogs.com/zichliang
import requests
import base64


def btoa(text):
    return base64.b64encode(text.encode('utf-8')).decode('utf-8').replace("=", "%3D")


def myspider(pages):
    total_count = 0
    for page in range(1, pages + 1):
        text = "yuanrenxue" + str(page)
        btoa_str = btoa(text)
        print(f"第{str(page)}页的m值为{btoa_str}")
        # 请求
        headers = {
            'User-Agent': 'yuanrenxue.project',
        }
        cookies = {
            'sessionid': '3mabax7wbz5h4i6c5wvjqwp3rbcfggao',
        }
        url = f"https://match.yuanrenxue.com/api/match/12?page={str(page)}&m={btoa_str}"
        response = requests.get(url, cookies=cookies, headers=headers)
        print(response.text)
        # 解析
        res_json_list = response.json().get('data', '')
        if res_json_list == '': continue
        per_page_count = 0
        for item in res_json_list:
            value0 = item.get('value', '')
            value = 0 if value0 == '' else int(value0)
            per_page_count += value
        print(f"第{page}页的和为：{per_page_count}")
        total_count += per_page_count
    return total_count


if __name__ == "__main__":
    total_count = myspider(5)
    print(f"五页数字总和为：{total_count}")