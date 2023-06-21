# -*- coding: utf-8 -*-
# @Time    : 2023/6/14 15:08
# @Author  : lzc
# @Email   : hybpjx@163.com
# @File    : m8.py
# @Software: PyCharm
# @blog    : https://www.cnblogs.com/zichliang
import base64
import re
import time

import cv2
import easyocr
import numpy as np
import requests

from requests.utils import add_dict_to_cookiejar

# 映射坐标位置
coordinate_map = {1: '126', 2: '137', 3: '146', 4: '455', 5: '466', 6: '476', 7: '755', 8: '766', 9: '776'}


def init_session():
    session = requests.session()
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.43",
    }

    cookies = {
        "sessionid": "dvkrmesp4116oqysh5x847tzki0ep0ro",
    }
    session.headers = headers

    add_dict_to_cookiejar(session.cookies, cookies)

    return session


def base64toJPG(base64_data, pic_name):
    data = base64.b64decode(base64_data)
    with open(pic_name, 'wb') as f:
        f.write(data)


def get_verify(s: requests.Session):
    res1 = s.get("https://match.yuanrenxue.cn/api/match/8_verify")
    html = res1.json()['html']
    word_list = re.findall("<p>(.*?)</p>", html)
    if not (pattern := re.search('src=\"(.*?)\" alt=""', html)):
        raise Exception("正则匹配失败")
    base64_str_img = pattern.group(1)

    base64toJPG(base64_str_img.replace("data:image/jpeg;base64,", ""), "captcha.jpg")
    return word_list


def handle_pic():
    im = cv2.imread('captcha.jpg')
    # 读取图片高，宽
    h, w = im.shape[0:2]

    # np.unique()该函数是去除数组中的重复数字，并进行排序之后输出，这里返回的是所有像素rgb值，以及对应的数量
    colors, counts = np.unique(np.array(im).reshape(-1, 3), axis=0, return_counts=True)

    # 挑选图片中背景最多的两种颜色对应的像素个数
    ct = np.sort(counts)
    top2_counts = ct[-2:].tolist()

    # 把频率最高的两种颜色筛掉
    info_dict = {counts[i]: colors[i].tolist() for i, v in enumerate(counts) if not v in top2_counts}
    colors_select = np.array([v for v in info_dict.values()])

    # 移除了背景的图片,赋值为去了黑色背景的colors就不会出现少一个字的情况
    remove_background_rgbs = colors_select
    mask = np.zeros((h, w, 3), np.uint8) + 255  # 生成一个全是白色的图片

    # 通过循环将不是噪点的像素,赋值给一个白色的图片,最后到达移除背景图片的效果
    for rgb in remove_background_rgbs:
        mask[np.all(im == rgb, axis=-1)] = im[np.all(im == rgb, axis=-1)]
    # 去掉线条,全部像素黑白化
    line_list = []  # 首先创建一个空列表,用来存放出现在间隔当中的像素点
    # 两个for循环,遍历9000次
    for y in range(h):
        for x in range(w):
            tmp = mask[x, y].tolist()
            if tmp != [0, 0, 0]:
                if 0 < y < 20 or 110 < y < 120 or 210 < y < 220:
                    line_list.append(tmp)
                if 0 < x < 10 or 100 < x < 110 or 200 < x < 210:
                    line_list.append(tmp)
    remove_line_rgbs = np.unique(np.array(line_list).reshape(-1, 3), axis=0)
    for rgb in remove_line_rgbs:
        mask[np.all(mask == rgb, axis=-1)] = [255, 255, 255]
    # 把所有字体颜色统一替换为黑色
    mask[np.any(mask != [255, 255, 255], axis=-1)] = [0, 0, 0]
    # 生成一个2行三列数值全为1的二维数字,作为腐蚀操作中的卷积核
    kernel = np.ones((2, 3), 'uint8')
    # iterations 迭代的次数,也就是进行多少次腐蚀操作，卷积核越大，迭代次数越多字体会被处理的越粗
    erode_img = cv2.erode(mask, kernel, iterations=2)
    # cv2.waitKey(0)
    # cv2.imwrite(r"capchta_yuan_processed.jpg", erode_img)
    return erode_img


# 图片切割
def image_clip(cv_img):
    clip_imgs = []
    # num=0
    for y in range(0, 300, 100):
        for x in range(10, 300, 100):
            cropped = cv_img[y:y + 100, x:x + 100]  # 裁剪坐标为[y0:y1, x0:x1]
            clip_imgs.append(cropped)
            # cv2.imwrite(r"...\{0}.jpg".format(str(num)), cropped)
            # num+=1
    return clip_imgs


def ocr_identify(processed_img):
    imglist = image_clip(processed_img)
    ocr_words = []
    '''easyocr识别图片，设置识别中英文两种语言'''
    reader = easyocr.Reader(['ch_sim'], gpu=False)
    for img in imglist:
        text = reader.readtext(img, detail=0)

        ocr_words += text

    return ocr_words


# 通过ocr方式获取返回坐标
def word_match(words, ocr_words):
    answer_str = ''
    for ind, ocr in enumerate(ocr_words):
        for word in words:
            if ocr == word:
                answer_str += str(coordinate_map[ind]) + '|'

    return answer_str


def manual_identify(processed_img):
    cv2.imwrite(r"capchta_yuan_processed.jpg", processed_img)
    # cv2.imshow("Image processed", processed_img)  # 移除了背景的图片
    # cv2.waitKey(0)
    loc = input("手动输入坐标的索引：")
    answer = ''
    for l in loc:
        answer += coordinate_map[int(l)] + '|'

    return answer


def find_repeat_data(_list):
    """
    查找列表中重复的数据
    :return: 一个重复数据的列表，列表中字典的key 是重复的数据，value 是重复的次数
    """
    repeat_list = []
    for i in set(_list):
        ret = _list.count(i)  # 查找该数据在原列表中的个数
        if ret > 1:
            item = dict()
            item[i] = ret
            repeat_list.append(item)
    return repeat_list


def get_data(page):
    session = init_session()
    word_list = get_verify(session)
    print(word_list)
    processed_img = handle_pic()
    # 代码识别
    # ocr_word_list = ocr_identify(processed_img)
    # print(ocr_word_list)
    # answer = word_match(word_list, ocr_word_list)

    # 手动识别
    answer = manual_identify(processed_img)

    url = "https://match.yuanrenxue.cn/api/match/8"
    params = {
        "page": str(page),
        "answer": answer
    }
    print(answer)
    response = session.get(url, params=params)
    print(response.text)
    return [int(d.get('value')) for d in response.json()['data']]


if __name__ == '__main__':
    total = []
    for i in range(1, 6):
        total += get_data(i)
        time.sleep(3)

    r = find_repeat_data(total)
    print("出现频率最高的数字是>>>>", r)
