# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ShmedicalItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass
    ssq = scrapy.Field()
    name = scrapy.Field()
    address = scrapy.Field()
    level = scrapy.Field()
    memo = scrapy.Field()
    type = scrapy.Field()
