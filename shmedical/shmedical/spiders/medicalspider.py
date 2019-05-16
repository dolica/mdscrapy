# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector

from ..items import ShmedicalItem


class MedicalspiderSpider(scrapy.Spider):
    name = 'medicalspider'
    allowed_domains = ['ybj.sh.gov.cn']
    start_urls = ['http://ybj.sh.gov.cn/xxcx/ddyy.jsp?lm=5']


    def parse(self, response):
        for qxcode in ['01','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','22']:


            form_data = {
                'pageno': '1',
                'qxcode':qxcode,
                'grade':'',
                'unitname':'',
                'address':''
            }
            yield scrapy.FormRequest('http://ybj.sh.gov.cn/xxcx/ddyy.jsp',formdata=form_data, callback=self.parseqx,meta={'qx':qxcode})


    def parseqx(self, response):
        data_table = response.css('table')[2]
        hospitals = data_table.css('tr')
        if hospitals is not None:
            yield from self.__parse_detail(hospitals)

        qxcode = response.meta['qx']
        curr_page = response.css('span.current::text').extract_first()
        last_a = response.css('div.yypages a::text').extract()[-1]
        if last_a.strip() != '>':
            return
        next_page = int(curr_page) + 1
        form_data = {
            'pageno': str(next_page),
            'qxcode': qxcode,
            'grade': '',
            'unitname': '',
            'address': ''
        }
        yield scrapy.FormRequest('http://ybj.sh.gov.cn/xxcx/ddyy.jsp', formdata=form_data, callback=self.parseqx,
                                 meta={'qx': qxcode})

    def __parse_detail(self, hospitals):
        for i in range(0, len(hospitals)):
            tds = hospitals[i].css('td::text').extract()
            if len(hospitals[i].css('td')) == 5:
                if tds[0] in ['所属区县','地址']:
                    continue
                item = ShmedicalItem()
                item['ssq'] = tds[0].strip()
                item['name'] = tds[1].strip()
                item['address'] = tds[2].strip()
                item['level'] = tds[3].strip()
                yield item
