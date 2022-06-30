# -*- coding: utf-8 -*-
# @Time    : 2022/6/30 14:51
# @Author  : tzh
# @File    : movie_info.py
# 测试过程中小概率出错。建议加个异常判断

from spiders.spi_douban import doubanSpider
from bs4 import BeautifulSoup
from spiders.items import Tutorial2Item
import urllib.request
import json
import requests
from random import randint


# random_movie功能：通过导入spi_douban随机抽个大宝贝电影，并得到字典info
"""
info:
键：url——值：该电影的豆瓣主页
键：pic——值：该电影的宣传海报的url链接
键：score——值：豆瓣评分
键：title——值：电影名
键：director——值：导演
键：author——值：演员     # 列表
键：datePublished——值：上映时间
键：kind——值：电影类型
键：descrpition——值：电影简介
"""


def random_movie():
    spi = doubanSpider()
    url = spi.start_urls
    # print(url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE '
    }
    req = requests.get(url[0], headers=headers)
    content = req.text
    soup = BeautifulSoup(content, 'lxml')
    text = soup.body.text
    dic = json.loads(text)
    info = get_info(dic['subjects'])
    detail(info)
    # download_pic(info)
    # print(info['url'])
    # print(info)


# get_info和detail功能为爬取电影的具体信息
def get_info(movies_list):
    l = len(movies_list)
    i = randint(0, l - 1)
    lis = movies_list[i]
    info = {}
    info["url"] = lis['url']
    info["pic"] = lis['cover']
    info["score"] = lis['rate']
    info["title"] = lis['title']
    return info


# download_pic功能：将电影的海报下载到本地，命名有电影＋豆瓣评分构成
def download_pic(info):
    filename = info["title"] + '_评分：' + info["score"] + '分' + '.jpg'
    urllib.request.urlretrieve(info["pic"], filename)


def detail(info):
    info['director'] = []
    info['author'] = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE '
    }
    req = requests.get(info['url'], headers=headers)
    content = req.text
    soup = BeautifulSoup(content, "html.parser")
    scrpit = soup.find('script', {'type': 'application/ld+json'})
    text = scrpit.contents[0]
    # print(text)
    dic = json.loads(text)
    for man in dic['director']:
        info['director'].append(man['name'])
    for man in dic['author']:
        info['author'].append(man['name'])
    info['datePublished'] = dic['datePublished']
    info['kind'] = dic['genre']
    info['description'] = dic['description']

# 测试用
# random_movie()
