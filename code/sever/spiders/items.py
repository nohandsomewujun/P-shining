# -*- coding: utf-8 -*-
# @Time    : 2022/6/30 9:48
# @Author  : tzh
# @File    : items.py

import scrapy

from scrapy.item import Item, Field


class Tutorial2Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    info = scrapy.Field()
    pic = scrapy.Field()
    score = scrapy.Field()
    title = scrapy.Field()
