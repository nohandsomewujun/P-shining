# -*- coding: utf-8 -*-
# @Time    : 2022/6/28 14:25
# @Author  : tzh
# @File    : joke.py
# 模块说明：先调用store_joke将网页爬取的笑话以json文件格式存储，随后调用load_one_joke随机读取一个笑话。
import requests
from bs4 import BeautifulSoup
import re
import json
import random


def get_req(url):
    head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)\
 Chrome/77.0.3865.120 Safari/537.36'}
    response = requests.get(url, headers=head)  # 爬取信息
    info_bs = BeautifulSoup(response.text, 'lxml')  # 利用bs解析
    return info_bs


def store_joke():
    origin_url = 'http://xiaohua.zol.com.cn/lengxiaohua/'
    info = get_req(origin_url)
    link_list = []
    for a_tag in info.find_all('a', string=re.compile('查看全文')):
        link = a_tag.get('href')
        if link:
            link_list.append(link)

    origin_url = origin_url.split('/')
    words_list = []
    for link in link_list:
        article_link = origin_url[0] + "//" + origin_url[2] + link
        mes = get_req(article_link)
        for article_text in mes.find_all(name="div", attrs={"class": "article-text"}):
            article = article_text.get_text()
            article = article.replace("\n", "")
            article = article.replace("\r", "")
            article = article.replace("\t", "")
            article = article.strip()
            article = re.sub(r"[0-9]", "*", article)
            article = article.split('*、')
            try:
                article = article.split('*.')
            except:
                None
            words_list.append(article)
        for i in range(len(words_list)):
            if len(words_list[i]) < 2:
                del words_list[i]
            # 提取笑话并格式化字符串，去除其中的转移符号,得到二维列表
    with open("joke.json", 'w') as f:
        json.dump(words_list, f)
    f.close()


def load_one_joke():
    with open("joke.json") as f:
        joke = json.load(f)
    f.close()
    i = random.randint(0, len(joke)-1)
    joke_i = joke[i]
    j = random.randint(1, len(joke_i)-1)
    return joke[i][j]


# store_joke()
# print(load_one_joke())
