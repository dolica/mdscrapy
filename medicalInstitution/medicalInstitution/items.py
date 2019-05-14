# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MedicalinstitutionItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    detail_link = scrapy.Field()
    name = scrapy.Field()
    type = scrapy.Field()
    address = scrapy.Field()
    postcode = scrapy.Field()
    registry_authority = scrapy.Field()
    start_date = scrapy.Field()
    end_date = scrapy.Field()
    pass

