# -*- coding: utf-8 -*-
import csv
import json
from time import time

import openpyxl
import re

import requests

class hospitol(object):

    def __init__(self,keywords):
        self.keywords = keywords


    @classmethod
    def isvalid(cls,name:str):
        pass

def loadClassify():
    keyword = {}
    with open('keyword.csv','r') as f:
        reader = csv.reader(f)
        for keys in reader:
            keyword[keys[0]]=keys[1]
    print('load {} column keywords.'.format(len(keyword)))
    return keyword

class Classify(object):

    def __init__(self,name,type):
        self.name = ''

def fmm(text:str,dicts):
    maxlen = len(text) if (len(text)<12) else 12
    keywords = list()

    while len(text)>0:
        s1 = text[0:maxlen]

        while(s1 not in dicts):
            if len(s1) == 1:
                break
            s1 = s1[0:-1]

        if len(s1) >1:
            keywords.append(s1)
        text = text[len(s1):]
    return keywords

def is_chain(text:str):
    pattern = '.*[店|部]$|.*[店|部]\(.*\)$'
    if re.match(pattern,text):
        return True

def get_classify(words,dicts,is_chain):
    classifylist = set()
    for word in words:
        c = dicts[word]
        classifylist.add(c)
    if len(classifylist) == 0:
        classify =  '其他'
    elif len(classifylist) == 1:
        classify = classifylist.pop()
    else:
        if '连锁' in classifylist:
            classify = '连锁'
        elif {'单体药店','基层医疗'}.issubset(classifylist):
            classify = '单体药店'
        elif {'单体药店','医院'}.issubset(classifylist):
            classify = '单体药店'
        elif '基层医疗' in classifylist:
            classify = '基层医疗'
        elif {'医院','商业'}.issubset(classifylist):
            classify = '医院'
        elif {'单体药店','商业'}.issubset(classifylist):
            classify = '连锁'
        else:
            classify = ','.join(classifylist)
    if classify in {'商业','医院'} and is_chain:
        classify =  '连锁'
    if classify == '单体药店' and is_chain:
        for w in words:
            if not w.endswith('店'):
                classify = '连锁'

    return classify

def findClassify(name):
    st = time()
    response = requests.get("http://localhost:8080/classify/findByName?name="+name)
    result = json.loads(response.content)
    print(time()-st)
    return result['name']


if __name__ == '__main__':
    # findClassify('昆山市万家春药房连锁有限公司二十二分店')
    # keys = loadClassify()
    result = []
    index =1
    st = time()
    with open('/Users/wangshaohu/Desktop/石家庄3.csv','r') as f:
        for line in f.readlines():
            fields = line.split(',')
            if len(fields)<8:
                print(line)
                continue

            result.append((fields[0],fields[1],fields[2],fields[3],fields[4],fields[5],fields[6],findClassify(fields[1])))
            index+=1

    wb = openpyxl.Workbook()
    sheet = wb.active
    for r in result:
        sheet.append(r)
    wb.save('/Users/wangshaohu/Desktop/石家庄.xlsx')
