# -*- coding: utf-8 -*-
# Description: 抓取陕西铜川医保定点数据

import csv

import requests
from lxml import etree
from collections import namedtuple

hospital_level = {
    '02':'三级医院',
    '05':'二级医院',
    '08':'一级医院',
    '14':'乡镇卫生院',
    '15':'社区医疗机构'
}

YLObject = namedtuple('YLObject',['name','level','ssq','address','tel','scope'])
StoreObject = namedtuple('StoreObject',['name','address','tel','ssq'])

def download_yl():
    url = 'http://wx.tongchuanhrss.gov.cn/hospitalQuery.action'
    datas = {
        'p2':1,
        'p1':'02',
        'submit':'查询'
    }
    ylobjs = []

    def __download_by_level(url, datas):
        response = requests.post(url, datas)
        dom = etree.HTML(response.content)
        hospitals = dom.xpath('//li[@class="p1 lyb"]')
        for h in hospitals:
            name = h.text.strip()
            fields = h.xpath('.//ul/li/text()')
            level = fields[0].split('\xa0')[1]
            ssq = fields[1].split('\xa0')[1]
            address = fields[2].split('\xa0')[1]
            tel = fields[3].split('\xa0')[1]
            scope = ','.join(fields[4].split('\xa0')[1:])
            ylobj = YLObject(name, level, ssq, address, tel, scope)
            ylobjs.append(ylobj)

    ylobjs.append(YLObject._fields)
    for level,ln in hospital_level.items():
        datas['p1'] = level
        __download_by_level(url,datas)

    write_to_csv('../datas/陕西/铜仁医疗.csv',ylobjs)

def download_store():
    url = 'http://wx.tongchuanhrss.gov.cn/pharmacyQuery.action'
    response = requests.get(url)
    dom = etree.HTML(response.content)
    ssqs = dom.xpath('//li[@class="pm lm"]')
    storeObjs = []
    for sq in ssqs:
        ssq = sq.text.strip()
        stores = sq.xpath('.//li[@class="p1 lyb"]')
        for store in stores:
            name = store.text.strip()
            fields = store.xpath('.//ul/li/text()')
            tel = fields[0].split('\xa0')[1]
            address = fields[1].split('\xa0')[1]
            storeObj = StoreObject(name,address,tel,ssq)
            storeObjs.append(storeObj)
    write_to_csv('../datas/陕西/铜仁药店.csv',storeObjs)


def write_to_csv(filepath,datas):
    with open(filepath,'w') as f:
        writer = csv.writer(f)
        writer.writerows(datas)



download_store()