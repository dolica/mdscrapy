# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pprint

from pymysql import OperationalError
from pymysql.constants.CR import CR_SERVER_GONE_ERROR, CR_SERVER_LOST, CR_CONNECTION_ERROR
from pymysql.cursors import DictCursor
from twisted.enterprise import adbapi
import logging

from twisted.internet import defer

logger = logging.getLogger(__name__)
logger.setLevel('DEBUG')


class MedicalinstitutionPipeline(object):
    """
    Defaults:
    MYSQL_HOST = 'localhost'
    MYSQL_PORT = 3306
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'root'
    MYSQL_DB = 'medical'
    MYSQL_TABLE = 't_medical_institution'
    MYSQL_RETRIES = 3
    MYSQL_CHARSET = "utf8"
    """

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def __init__(self, crawler):
        self.settings = crawler.settings
        db_args = {
            'host': self.settings.get('MYSQL_HOST','localhost'),
            'port': self.settings.get('MYSQL_PORT',3306),
            'db': self.settings.get('MYSQL_DB',None),
            'user': self.settings.get('MYSQL_USER',None),
            'password': self.settings.get('MYSQL_PASSWORD',''),
            'charset': self.settings.get('MYSQL_CHARSET','utf8'),
            'cursorclass': DictCursor,
        }
        self.retries = self.settings.get('MYSQL_RETRIES',3)
        self.table = self.settings.get('MYSQL_TABLE', None)
        self.db = adbapi.ConnectionPool('pymysql', **db_args)

    def close_spider(self, spider):
        self.db.close()

    @defer.inlineCallbacks
    def process_item(self, item, spider):
        retries = self.retries
        status = False
        while retries:
            try:
                yield self.db.runInteraction(self._process_item, item)
            except OperationalError as e:
                if e.args[0] in (
                    CR_SERVER_GONE_ERROR,
                    CR_SERVER_LOST,
                    CR_CONNECTION_ERROR
                ):
                    retries -= 1
                    logger.info('%s %s attempts to reconnect left',e, retries)
                    continue
                logging.error(e)
                logging.exception('%s', pprint.pformat(item))
            except Exception as e1:
                logging.exception('%s', pprint.pformat(item))
            else:
                status = True
            break
        yield item

    def _generate_sql(self, data):
        columns = lambda d: ','.join(['`{}`'.format(k) for k in d])
        values = lambda d: [v for v in d.values()]
        placeholders = lambda d: ','.join(['%s']*len(d))

        sql_template = 'INSERT INTO `{}` ( {} ) VALUES ( {} )'
        return (
            sql_template.format(self.table, columns(data), placeholders(data)),
            values(data)
        )

    def _process_item(self, tx ,row):
        sql, data = self._generate_sql(row)
        try:
            tx.execute(sql,data)
        except Exception:
            logger.error('SQL: %s', sql)
            raise
