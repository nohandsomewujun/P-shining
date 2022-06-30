# -*- coding: utf-8 -*-
# @Time    : 2022/6/30 9:15
# @Author  : tzh
# @File    : pipelines.py
from scrapy import signals
import json


class Tutorial2Pipeline(object):
    def process_item(self, item, spider):
        return item
