# -*- coding: utf-8 -*-
# @Time    : 2023/6/2 16:40
# @Author  : lzc
# @Email   : hybpjx@163.com
# @File    : m7.py
# @Software: PyCharm
# @blog    : https://www.cnblogs.com/zichliang
import base64
import re

import execjs
import requests
from fontTools.ttLib import TTFont
from lxml import etree


class M7:
    def __init__(self):
        self.woff_file_name = "decrypt_woff_data.woff"
        self.xml_file_name = "font_xml.xml"

        self.session = requests.session()
        self.session.headers = {
            "user-agent": "yuanrenxue.project",
            "cookies": "sessionid=94hkmtl47z6i4pb57gwikd3eaxv247ev"
        }

        self.url = "https://match.yuanrenxue.cn/api/match/7"

        self.rank_list = []

    def get_data(self, page):
        params = {
            "page": page
        }
        response = self.session.get(self.url, params=params)

        base64_woff = response.json()['woff']

        font_encrypt_list = [str(d['value']).replace("&#x", "").replace(" ", "") for d in response.json()['data']]
        # 获取详情页 返回base64编码的数据 和加密后的字体数据
        return base64_woff, font_encrypt_list

    def downLoad_woff(self, base64_woff):
        # 下载woff文件
        data = base64.b64decode(base64_woff)
        with open(self.woff_file_name, 'wb') as f:
            f.write(data)

    def parse_woff_data(self):
        # 用xml提取出来 on值和value值.
        font_obj = TTFont(self.woff_file_name)
        font_obj.saveXML(self.xml_file_name)
        _xml = etree.parse(self.xml_file_name)
        map_value = {}
        for xm in _xml.xpath("//TTGlyph")[1:]:
            on_value = ''.join(xm.xpath('.//pt/@on'))
            key = str(xm.xpath("./@name")[0]).replace("uni", '')
            # print(on_value, key)
            map_value[on_value] = key

        # 找出映射关系
        map_number = {
            '10100100100101010010010010': '0',
            '1001101111': '1',
            '100110101001010101011110101000': '2',
            '10101100101000111100010101011010100101010100': '3',
            '111111111111111': '4',
            '1110101001001010110101010100101011111': '5',
            '10101010100001010111010101101010010101000': '6',
            '1111111': '7',
            '101010101101010001010101101010101010010010010101001000010': '8',
            '10010101001110101011010101010101000100100': '9',
        }

        # 然后map_value 和 map_number 重新拼接出一个正确的映射关系表.
        new_map_rs = {}
        for k, v in map_number.items():
            if map_value.get(k):
                new_map_rs[map_value.get(k)] = v

        return new_map_rs

        # return map_rs

    def get_zhs_name(self, page):
        # 获得每页的召唤师姓名
        ctx = execjs.compile(open("m7.js", "r", encoding="utf-8").read())
        zhs_name = ctx.call("get_name", page)
        return zhs_name

    def v1_main(self):
        true_map = {}
        for i in range(1, 6):
            # 调用方法
            base64_woff, font_encrypt_list = self.get_data(i)
            # 下载
            self.downLoad_woff(base64_woff)
            map_rs = self.parse_woff_data()
            print(map_rs)
            for k, v in map_rs.items():
                # print(f.replace(k,v))
                font_encrypt_list = re.sub(k, v, str(font_encrypt_list))
            zhs_name_list = self.get_zhs_name(i)
            print(font_encrypt_list)
            # 然后用胜点和召唤师姓名 得到一个对应的表
            for zhs, sd in zip(zhs_name_list, eval(font_encrypt_list)):
                true_map[zhs] = sd

        # 计算出胜点最多的那一个字典。
        max_value = max(zip(true_map.values(), true_map.keys()))
        print(f"所以胜点最高的召唤师是{max_value[1]}，胜点为{max_value[0]}")


if __name__ == '__main__':
    M7().v1_main()
