# -*- coding: utf-8 -*-
# @Time    : 2022/6/26 15:37
# @Author  : tzh
# @File    : get_weather.py
# 模块说明：没啥好说的
import requests
from bs4 import BeautifulSoup


def get_Weather(city):
    getback = {}
    url = "http://wthrcdn.etouch.cn/WeatherApi?city={}".format(city)
    req = requests.get(url)
    content = req.text
    soup = BeautifulSoup(content, 'lxml')
    getback['当前温度'] = soup.wendu.text + '°C'
    getback['当前湿度'] = soup.shidu.text
    getback['当前风向'] = soup.fengxiang.text
    getback['今日最高温度'] = soup.forecast.high.text[3:]
    getback['今日最低温度'] = soup.forecast.low.text[3:]
    return getback


city = input("输入一个城市")
info = get_Weather(city)
