# -*- coding: utf-8 -*-
import json

import scrapy

from ..items import ShmedicalItem


class CqydybSpider(scrapy.Spider):
    name = 'cqydyb'
    allowed_domains = ['ggfw.cqhrss.gov.cn']
    start_urls = ['http://ggfw.cqhrss.gov.cn/ggfw/QueryBLH_mainSmXz.do?code=034']
    provinces = {"110000":"北京市","120000":"天津市","130000":"河北市","140000":"山西省","150000":"内蒙古自治区","210000":"辽宁省","220000":"吉林省","230000":"黑龙江省","310000":"上海市","320000":"江苏省","330000":"浙江省",
						   "340000":"安徽省","350000":"福建省","360000":"江西省","370000":"山东省","410000":"河南省","420000":"湖北省","430000":"湖南省","440000":"广东省","450000":"广西壮族自治区","460000":"海南省","500000":"重庆市",
						   "510000":"四川省","520000":"贵州省","530000":"云南省","540000":"西藏自治区","610000":"陕西省","620000":"甘肃省","630000":"青海省","640000":"宁夏回族自治区","650000":"新疆维吾尔自治区","660000":"新疆生产建设兵团"}

    def parse(self, response):
        for code in self.provinces.keys():
            formdata = {
                'code': '034',
                'asjbm': code,
                'bfwjgmc': ''
            }
            # yield scrapy.FormRequest(url='http://ggfw.cqhrss.gov.cn/ggfw/QueryBLH_querySmXz.do', formdata=formdata, callback=self.parse_yl,meta={'currentpage':1,'code':code})
            yield scrapy.FormRequest(url='http://ggfw.cqhrss.gov.cn/ggfw/QueryBLH_querySmXz.do', formdata=formdata,
                                     callback=self.parse_hospital, meta={'currentpage': 1, 'code': code})
        pass

    def parse_hospital(self,response):
        try:
            datas = json.loads(response.body,encoding='utf-8') #type: dict
            if datas.get('message') == '操作成功!':
                results = datas.get('result')
                for result in results:
                    print(result)
                    item = ShmedicalItem()
                    item['name'] = result.get('fwjgmc')
                    item['address'] = result.get('dz')
                    item['type'] = result.get('sjmc')
                    item['level'] = result.get('yydj')
                    item['ssq'] = result.get('qxmc')
                    item['telephone'] = result.get('lxdh','')
                    item['memo'] = result.get('fwjgbh')
                    yield item
                page = datas.get('page')
                tp = page['pageCount']
                if response.meta['currentpage'] < tp:
                    currentpage = response.meta['currentpage']+1
                    code = response.meta['code']
                    formdata = {
                        'code': '034',
                        'asjbm': code,
                        'bfwjgmc': '',
                        'currentPage': str(currentpage),
                        'goPage': ''
                    }
                    yield scrapy.FormRequest(url='http://ggfw.cqhrss.gov.cn/ggfw/QueryBLH_querySmXz.do',
                                             formdata=formdata,
                                             callback=self.parse_hospital,
                                             meta={'currentpage':currentpage,'code':code})
        except Exception as e:
            print(e)