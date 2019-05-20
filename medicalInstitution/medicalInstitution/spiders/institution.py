# -*- coding: utf-8 -*-
import pprint
from io import BytesIO

import scrapy
from PIL import Image
from pydispatch import dispatcher
from scrapy import Selector, signals
from scrapy.conf import settings
from scrapy.http import  HtmlResponse
from urllib.parse import urlencode

from scrapy.mail import MailSender

from ..items import MedicalinstitutionItem

mailer = MailSender.from_settings(settings)

class InstitutionSpider(scrapy.Spider):
    name = 'institution'
    allowed_domains = ['credit.wsjd.gov.cn']
    site_url = 'https://credit.wsjd.gov.cn'
    start_urls = ['https://credit.wsjd.gov.cn/portal/pubsearch/org/0114000000']

    headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Connection':'keep-alive',
        'Host':'credit.wsjd.gov.cn',
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
    }

    def __init__(self):
        dispatcher.connect(self.close, signals.spider_closed)


    def parse(self, response: HtmlResponse):
        captcha_url = response.css('.code-img > img::attr("src")').extract_first()
        yield scrapy.Request(response.urljoin(captcha_url),callback=self.input_captcha)

    def input_captcha(self,response: HtmlResponse):
        captcha_data = response.body
        with Image.open(BytesIO(captcha_data)) as img:
            img.show()
            captcha_code = input('captcha_code:\n')
        params = {
            'NAME':'女子医院', #责任公司,大学校医院，有限公司，社区服务，大学医学院，中西医结合医院，中西结合医院，骨科医院，口腔医院，妇幼保健,儿童医院，乡卫生院,镇卫生院,社区卫生
            'PASSCODE':'',
            'BEGIN_DATE':'',
            'END_DATE':'',
            'validCode':captcha_code
        }
        query_url = self.start_urls[0]+"?"+urlencode(params)
        print(query_url)
        yield scrapy.Request(query_url,callback=self.parse_detail)

    def parse_detail(self,response: HtmlResponse):
        trs = response.css('table#formresult tr')
        print(response.url)
        if len(trs) < 2:
            print('未发现可用数据')
            return
        for i in range(1,len(trs)):
            tr = trs[i] #type: Selector
            institution = MedicalinstitutionItem()
            institution['detail_link'] = tr.css('td:nth-child(1)>a::attr("href")').extract_first()
            institution['name'] = tr.css('a::text').extract_first()
            institution['type'] = tr.css('td:nth-child(2)::text').extract_first()
            institution['address'] = tr.css('td:nth-child(3)::text').extract_first()
            institution['postcode'] = tr.css('td:nth-child(4)::text').extract_first()
            institution['registry_authority'] =  tr.css('td:nth-child(5)::text').extract_first()
            institution['start_date'] = tr.css('td:nth-child(6)::text').extract_first()
            institution['end_date'] = tr.css('td:nth-child(7)::text').extract_first()
            yield institution
        next_page = response.css('a.next::attr("href")').extract_first()
        if next_page is not None:
            yield scrapy.Request(self.site_url+next_page,callback=self.parse_detail)

    def close(spider, reason):
        stats = spider.crawler.stats.get_stats()
        return mailer.send(
            subject='[{}] crawler spider end'.format(spider.name),
            to='wangshaohu@agilesc.com',
            body=pprint.pformat(stats)
        )