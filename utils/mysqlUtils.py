# -*- coding: utf-8 -*-
import csv

import pymysql

db_params = {
    'host':'localhost',
    'port':3306,
    'user':'root',
    'password':'123456',
    'db':'cdp',
    'charset':'utf8'
}

class MysqlClient(object):

    def __init__(self, params=db_params):
        self._connect = pymysql.Connect(**params)


    def execute(self,sql,data):
        connect = self._connect
        cursor = connect.cursor()
        try:
            cursor.execute(sql,data)
            connect.commit()
        except pymysql.MySQLError as e:
            print(e)
            connect.rollback()


    def close(self):
        self._connect.close()


if __name__ == '__main__':
    sql = 'select id,name,address,province,city from t_medical_terminal'
    client = MysqlClient()
    client.execute(sql)
    client.close()

