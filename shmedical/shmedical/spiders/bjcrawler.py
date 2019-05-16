# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urlencode

from ..items import ShmedicalItem


class BjcrawlerSpider(scrapy.Spider):
    name = 'bjcrawler'
    allowed_domains = ['www.bjrbj.gov.cn']
    start_url = 'http://www.bjrbj.gov.cn/LDJAPP/search/ddyy/ddyy_01_outline_new.jsp?'

    def start_requests(self):
        self.epage = 141
        self.curr = 1
        self.params = {
            'sno': 0,
            'spage': 0,
            'epage': 10,
            'leibie': '00',
            'suoshu': '00',
            'sword': ''
        }
        args = urlencode(self.params)
        self.curr += 1
        yield scrapy.Request(self.start_url+args,callback=self.parse)

    def parse(self, response):
        table = response.css('table[width="96%"]')
        trs = table.css('tr')
        if trs is  None or len(trs) <= 3:
            return
        yield from self.parse_table(trs[5:-2])
        while self.curr <= self.epage:
            self.params['sno'] = (self.curr-1)*20
            args = urlencode(self.params)
            self.curr+=1
            yield scrapy.Request(self.start_url + args, callback=self.parse)
        pass

    def parse_table(self, datas):
        print(len(datas))
        if datas is None or len(datas) ==0:
            return
        for data in datas:
            aspan = data.css('td span a[href^="detail"]::attr(href)').extract_first()
            id = data.css('td span a::text').extract_first()
            yield scrapy.Request('http://www.bjrbj.gov.cn/LDJAPP/search/ddyy/'+aspan, callback=self._parse_detail, meta={'id':id})


    def _parse_detail(self,response):
        fields = response.css('table[width="90%"] tr td>font::text').extract()
        item = ShmedicalItem()
        item['name'] = fields[0]
        item['address'] = fields[4]
        item['ssq'] = fields[1]
        item['level'] = fields[3]
        item['type'] = fields[2]
        item['memo'] = response.meta['id']
        yield item

