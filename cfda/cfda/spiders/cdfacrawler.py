# -*- coding: utf-8 -*-
import csv
import json
import os
import re

import scrapy
from urllib.parse import urlencode

import sys

from scrapy.http import Response

from ..items import CfdaItem


class CdfacrawlerSpider(scrapy.Spider):
    name = 'cdfacrawler'
    allowed_domains = ['appcfda.drugwebcn.com']
    start_urls = ['http://appcfda.drugwebcn.com/']

    def __init__(self):
        self.pagenum = 33177
        self.current = 0
        self.page_args = {
            'tableId': 41,
            'searchF': 'Quick Search',
            'searchK': '',
            'pageSize': 15
        }
        self.errorpage = []

    def start_requests(self):
        for i in range(0,self.pagenum):
            self.current = i+1
            self.page_args['pageIndex'] = self.current
            args = urlencode(self.page_args)
            yield scrapy.Request(url='http://appcfda.drugwebcn.com/datasearch/QueryList?'+args, callback=self.parse,meta={'page':self.current})

    def parse(self, response: Response):
        try:
            datas = json.loads(response.body)
            pattern = '\.(?P<name>.*)\s\((?P<license>.*)\)'
            for data in datas:

                item = CfdaItem()
                item['id'] = data.get("ID")
                content = data.get('CONTENT') #type:str
                item['content'] = content
                try:
                    r = re.search(pattern,content)
                    item['name'] = r.group('name')
                    item['license'] = r.group('license')
                except Exception:
                    pass
                finally:
                    yield item
        except Exception as e:
            self.errorpage.append(response.meta['page'])


    def close(spider, reason):
        errorpages = spider.errorpage
        with open('/Users/wangshaohu/Desktop/cdfaerror.csv','w') as f:
            writer = csv.writer(f)
            writer.writerows(errorpages)