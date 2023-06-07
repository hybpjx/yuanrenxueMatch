# -*- coding: utf-8 -*-
# @Time    : 2023/5/29 13:54
# @Author  : lzc
# @Email   : hybpjx@163.com
# @File    : m13.py
# @Software: PyCharm
# @blog    : https://www.cnblogs.com/zichliang
import re

import requests
from requests.cookies import cookiejar_from_dict


def get_text():
    all_count = 0
    session = requests.session()
    session.headers = {
        "user-agent": "yuanrenxue.project"
    }
    session.cookies = cookiejar_from_dict({
        "sessionid": "0c663ochdm65kj1ush13txto1jkojn3d"
    })
    for i in range(1, 6):
        text = session.get("https://match.yuanrenxue.com/match/13").text
        params = re.findall(r"document\.cookie=(.*?)\+';", text)[0]

        cookies = str(params).replace("(", "").replace(")", "").replace("+", "").replace("'", "")

        cookies_list = str(cookies).split("=")

        response = session.get(f"https://match.yuanrenxue.com/api/match/13?page={i}", cookies={
            cookies_list[0]: cookies_list[1]
        })
        try:
            for data in response.json()["data"]:
                all_count += int(data['value'])
        except:
            print(response.text)

    return all_count


print(get_text())
