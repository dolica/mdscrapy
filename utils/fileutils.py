# -*- coding: utf-8 -*-
import csv


def txt_to_csv(file:str,to_file:str,delimit='\t') ->None:
    with open(file,'r') as f:
        with open(to_file,'w',encoding='utf-8') as wf:
            writer = csv.writer(wf)
            for line in f.readlines():
                fields = line.split(delimit)
                writer.writerow(fields)


if __name__ == '__main__':
    txt_to_csv('/Users/wangshaohu/OneDrive/md/卫健委数据库/wsjd_20180716.txt','/Users/wangshaohu/OneDrive/md/卫健委数据库/wsjd_20180716.csv')