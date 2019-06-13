# -*- coding: utf-8 -*-
# Description: 抓取陕西榆林医保定点数据

import csv

import requests
from collections import namedtuple
from lxml import etree


url = 'http://ylhrss.yl.gov.cn/wsfw/sbk/ylfwwd/'

subPage = {
          'sq.htm':'市区',
          'yy.htm':'榆阳',
          'sm.htm':'神木',
          'fg.htm':'府谷',
          'hs.htm':'横山',
          'jb.htm':'靖边',
          'db.htm':'定边',
          'sd.htm':'绥德',
          'mz.htm':'米脂',
          'jx.htm':'佳县',
          'wb.htm':'吴堡',
          'gj.htm':'清涧',
          'zz.htm':'子洲'
}

YLInfo = namedtuple('YLInfo',['name','address','ssq'])

def download():
    result = []
    for suburl,ssq in subPage.items():
        download_url = url+suburl
        response = requests.get(download_url)
        if response.status_code == 200:
            page = etree.HTML(response.content)
            fr = page.xpath('//tr[@class="firstRow"]')[0]
            content_table = fr.getparent()
            trs = content_table.xpath('./tr[position()>1]')
            for tr in trs:
                fields = tr.xpath('.//td/p/text()')
                if len(fields)==0:
                    fields=tr.xpath('.//td/p/span/text()')
                print(fields)
                ylInfo = YLInfo(fields[1],fields[2],ssq)
                result.append(ylInfo)

    with open('../datas/陕西/yl.csv','w') as f:
        writer = csv.writer(f)
        writer.writerows(result)

download()