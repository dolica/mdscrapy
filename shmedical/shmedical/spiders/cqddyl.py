# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy.http import Response

from ..items import ShmedicalItem


class CqddylSpider(scrapy.Spider):
    name = 'cqddyl'
    allowed_domains = ['ggfw.cqhrss.gov.cn']
    start_urls = ['http://ggfw.cqhrss.gov.cn/ggfw/QueryBLH_mainSmXz.do?code=033']

    def __init__(self):
        self.area = {"5000000300":"市本级","5001010300":"万州区","5001140300":"黔江区","5001020300":"涪陵区","5001030300":"渝中区",
							"5001040300":"大渡口区","5001050300":"江北区","5001060300":"沙坪坝区","5001070300":"九龙坡区","5001080300":"南岸区",
							"5001090300":"北碚区","5001120300":"渝北区","5001130300":"巴南区","5001160300":"江津区","5001170300":"合川区",
							"5001180300":"永川区","5001150300":"长寿区","5002220300":"綦江区","5002230300":"潼南区","5002240300":"铜梁区",
							"5002250300":"大足区","5002260300":"荣昌区","5002270300":"璧山区","5002280300":"梁平县","5002290300":"城口县",
							"5001190300":"南川区","5002300300":"丰都县","5002310300":"垫江县","5002320300":"武隆县","5002330300":"忠县",
							"5002340300":"开州区","5002350300":"云阳县","5002360300":"奉节县","5002370300":"巫山县","5002380300":"巫溪县",
							"5002400300":"石柱县","5002410300":"秀山县","5002420300":"酉阳县","5002430300":"彭水县","5009030300":"两江新区",
							"5001430300":"万盛区","5009100300":"成铁重庆社保部"}
        scrapy.Request(url=self.start_urls[0],callback=self.parse)

    def parse(self, response):
        for code in self.area.keys():
            formdata = {
                'code': '033',
                'ajbjg': code,
                'bfwjgmc':'',
                'afwjglx': '药店',
                # 'ayydj':'',
                'ftbydbz':''
            }
            # yield scrapy.FormRequest(url='http://ggfw.cqhrss.gov.cn/ggfw/QueryBLH_querySmXz.do', formdata=formdata, callback=self.parse_yl,meta={'currentpage':1,'code':code})
            yield scrapy.FormRequest(url='http://ggfw.cqhrss.gov.cn/ggfw/QueryBLH_querySmXz.do', formdata=formdata,
                                     callback=self.parse_yd, meta={'currentpage': 1, 'code': code})

    def parse_yl(self,response: Response):
        try:
            datas = json.loads(response.body,encoding='utf-8') #type: dict
            if datas.get('message') == '操作成功!':
                results = datas.get('result')
                for result in results:
                    item = ShmedicalItem()
                    item['name'] = result.get('fwjgmc')
                    item['address'] = result.get('dz')
                    item['type'] = result.get('yljglb')
                    item['level'] = result.get('yydj')
                    item['ssq'] = result.get('jbjgmc')
                    item['telephone'] = result.get('lxdh','')
                    item['memo'] = result.get('fwjgbh')
                    yield item
                page = datas.get('page')
                tp = page['pageCount']
                if response.meta['currentpage'] < tp:
                    currentpage = response.meta['currentpage']+1
                    code = response.meta['code']
                    formdata = {
                        'code': '033',
                        'ajbjg': code,
                        'bfwjgmc': '',
                        'afwjglx': '医院',
                        'ayydj': '',
                        'currentPage': str(currentpage),
                        'goPage': ''
                    }
                    yield scrapy.FormRequest(url='http://ggfw.cqhrss.gov.cn/ggfw/QueryBLH_querySmXz.do',
                                             formdata=formdata,
                                             callback=self.parse_next,
                                             meta={'currentpage':currentpage,'code':code})

        except Exception as e:
            print(e)

    def parse_yd(self,response: Response):
        try:
            datas = json.loads(response.body,encoding='utf-8') #type: dict
            if datas.get('message') == '操作成功!':
                results = datas.get('result')
                for result in results:
                    item = ShmedicalItem()
                    item['name'] = result.get('fwjgmc')
                    item['address'] = result.get('dz')
                    item['type'] = result.get('yljglb')
                    # item['level'] = result.get('yydj')
                    item['ssq'] = result.get('jbjgmc')
                    item['telephone'] = result.get('lxdh','')
                    item['memo'] = result.get('fwjgbh')
                    yield item
                page = datas.get('page')
                tp = page['pageCount']
                if response.meta['currentpage'] < tp:
                    currentpage = response.meta['currentpage']+1
                    code = response.meta['code']
                    formdata = {
                        'code': '033',
                        'ajbjg': code,
                        'bfwjgmc': '',
                        'afwjglx': '药店',
                        'ayydj': '',
                        'currentPage': str(currentpage),
                        'goPage': ''
                    }
                    yield scrapy.FormRequest(url='http://ggfw.cqhrss.gov.cn/ggfw/QueryBLH_querySmXz.do',
                                             formdata=formdata,
                                             callback=self.parse_yd,
                                             meta={'currentpage':currentpage,'code':code})

        except Exception as e:
            print(e)