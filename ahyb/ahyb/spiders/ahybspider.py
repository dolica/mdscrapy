# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector
from scrapy.http import Response


class AhybspiderSpider(scrapy.Spider):
    name = 'ahybspider'
    allowed_domains = ['www.ahhzyl.com']
    start_urls = ['http://www.ahhzyl.com/Hospital-list.aspx/']

    def __init__(self):
        self.total_page = 1123
        self.cur_page = 2

    def parse(self, response: Response):
        institutions = response.css('div#UpdatePanel1 tbody tr')
        if len(institutions) < 2:
            self.logger.error('[{}] data load error....'.format(response.url))
        else:
            self._parse_detail(institutions)
        view_state = response.css('input#__VIEWSTATE::attr("value")').extract_first()

        if self.cur_page <= self.total_page:
            post_args = {
                '_VIEWSTATE': view_state,
                '__EVENTTARGET': 'AspNetPager1',
                '__EVENTARGUMENT': str(self.cur_page),
                'ScriptManager1': 'UpdatePanel1|AspNetPager1'
            }
            self.cur_page += 1
            yield scrapy.FormRequest(self.start_urls[0] ,callback=self.parse,formdata=post_args)


    def _parse_detail(self, institutions):
        for institute in institutions[:-1]: #过滤掉最后一个翻页行
            fields = institute.css('td')
            for field in fields:  #type: Selector
                print(field)
        pass