# -*- coding: utf-8 -*-
# @Time    : 2022/6/30 10:35
# @Author  : tzh
# @File    : spi_douban.py
# @Software: PyCharm
import scrapy
import urllib.request
import json
from random import randint


class doubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ["douban.com"]
    start_list = []
    i = randint(1, 100)
    url = 'https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%83%AD%E9%97%A8&sort=recommend&page_limit=20' \
          '&page_start=' + str(i)
    start_list.append(url)
    start_urls = start_list  # 定义start_urls为一个存储链接的列表

    def start_requests(self):
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 ' \
                     'Safari/537.36 SE 2.X MetaSr 1.0 '
        headers = {'User-Agent': user_agent}
        # for url in self.start_urls:
        return scrapy.Request(url=self.start_urls[0], headers=headers, method='GET', callback=self.parse)


