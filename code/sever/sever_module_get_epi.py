# -*- coding: utf-8 -*-
# @Time    : 2022/6/27 14:20
# @Author  : tzh
# @File    : get_epi.py
# 模块说明：输入一个省份或城市名，返回包含相关疫情信息的字典
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import json
import requests
from datetime import datetime


# 主函数
def get_epi(position):
    content = get_data()
    info = display_province(content, position)
    if info == {}:
        info = display_city(content, position)
    return info


# 获取省份疫情信息
def display_province(content, province):
    json_data = json.loads(content)
    info = {}
    # 省份数据展示
    for i in json_data:
        if province in i['provinceName']:
            info["省份"] = i["provinceName"]

            recent_data(i['statisticsData'], info)
            # 获取今日疫情变化情况

            info["现存确诊"] = i["currentConfirmedCount"]
            info["累计确诊"] = i["confirmedCount"]
            info["累计死亡"] = i["deadCount"]
            info["累计治愈"] = i["curedCount"]
            return info
    return info


# 获取城市疫情信息
def display_city(json_content, city_name):
    json_data = json.loads(json_content)
    flag = 0
    info = {}
    # 省份数据展示
    for i in json_data:
        cities = i["cities"]
        for city in cities:
            if city_name in city['cityName']:
                flag = 1
                break
        if flag == 1:
            info["城市"] = city["cityName"]
            info["现存确诊"] = city["currentConfirmedCount"]
            info["累计确诊"] = city["confirmedCount"]
            info["累计死亡"] = city["deadCount"]
            info["累计治愈"] = city["curedCount"]
            return info
            break
    if flag == 0:
        print("没有相应的省份或城市信息!")
        return {}


# 爬取网页信息并经过处理改成列表+字典格式
def get_data():
    article_url = "https://ncov.dxy.cn/ncovh5/view/pneumonia"
    url = urlopen(article_url)
    soup = BeautifulSoup(url, 'html.parser')  # parser解析
    f_content = str(soup)

    # json字符串前后关键词
    json_start = "try { window.getAreaStat = "
    # 字符串包含的括号要进行转义
    json_end = "}catch\(e\){}"
    # json字符串正则匹配
    # (.*?)是匹配所有内容
    regular_key = json_start + "(.*?)" + json_end
    # 参数rs.S可以无视换行符，将所有文本视作一个整体进行匹配
    re_content = re.search(regular_key, f_content, re.S)
    # group()用于获取正则匹配后的字符串
    content = re_content.group()
    # 去除json字符串的前后关键词
    content = content.replace(json_start, '')
    # 尾巴去掉转义符号
    json_end = "}catch(e){}"
    content = content.replace(json_end, '')
    return content


# 获取最近信息
def recent_data(url, info):
    req = requests.get(url, timeout=30)
    dic_info = req.json()
    history_data = dic_info['data']
    date = get_date()
    yesterday = int(date)-1
    for day in history_data:
        if day['dateId'] == yesterday:
            info["新增确诊"] = day["confirmedIncr"]
            info["新增治愈"] = day["curedIncr"]
            info["新增死亡"] = day["deadIncr"]
            info["高风险地区"] = day['highDangerCount']
            info["中风险地区"] = day['midDangerCount']


# 获取今天日期
def get_date():
    today = str(datetime.today())
    dateregex = re.compile(r'(\d{4})-(\d{2})-(\d{2})')
    mo = dateregex.search(today)
    date = mo.group(1) + mo.group(2) + mo.group(3)
    return date

