# -*- coding: utf-8 -*-
import csv
import json

class Area(object):

    def __init__(self,code:int,name:str,level:int,pcode:int,fullname:str):
        self.code = code
        self.name = name
        self.level = level
        self.pcode = pcode
        self.fullname = fullname


class AreaService(object):

    areas = {}
    maxlen = 0

    def load_from_json(self,fp:str):
        with open(fp, 'r', encoding='utf8') as f:
            jdatas = json.load(f)
            for data in jdatas:
                self.__load_data(data)
        return self.areas

    def __load_data(self,data:dict,fullname=''):
        if fullname=='':
            fn = data['name']
        else:
            fn = fullname+','+data['name']
        area = Area(data['code'], data['name'], data['level'], data['pcode'],fn)
        if self.maxlen < len(data['name']):
            self.maxlen = len(data['name'])
        self.areas[data['name']] = area
        if 'children' in data.keys():
            for child in data['children']:
                self.__load_data(child,area.fullname)

    @classmethod
    def isInSameArea(cls,area1:Area,area2:Area):
        pass

    def searchByAddress(self,text:str):
        sublen = self.maxlen
        searched = []
        if len(text) < self.maxlen:
            sublen = len(text)

        while len(text)>1:
            searchtext = text[0:sublen]

            while searchtext not in self.areas.keys():
                if len(searchtext)==1:
                    break
                searchtext = searchtext[0:-1]

            if len(searchtext)>1:
                searched.append(self.areas[searchtext])

            text = text[len(searchtext):]
        result = None
        if len(searched) >=1:
            result = searched[0]
            for s in searched:
                if (s.level > result.level) and (s.fullname.startswith(result.fullname)):
                    result = s
        return result



areaService = AreaService()
areas = areaService.load_from_json('/Users/wangshaohu/OneDrive/md/china_area-master/area_code_2019.json')


def findarea(searchKeys:list):
    for key in searchKeys:
        r = areaService.searchByAddress(key)
        if r is None:
            continue
        else:
            pcc = r.fullname.split(',')
            print(pcc)
            if len(pcc) <3:
                continue
            else:
                return pcc
    return None


unmatch = []
match = []
with open('/Users/wangshaohu/Desktop/sjz终端明细.csv', 'r') as f:
    reader = csv.reader(f)
    for line in reader:
        area = findarea([line[3]])
        if area is None:
            unmatch.append(line)
            continue
        match.append(line+area)


with open('/Users/wangshaohu/Desktop/sjz终端明细1.csv','w') as fw:
    writer = csv.writer(fw)
    writer.writerows(match)

with open('/Users/wangshaohu/Desktop/sjz终端明细2.csv','w') as fw:
    writer = csv.writer(fw)
    writer.writerows(unmatch)



