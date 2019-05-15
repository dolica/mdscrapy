# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AhybItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    institution_code = scrapy.Field()
    manage_type = scrapy.Field()
    registry_time = scrapy.Field()
    tc_area = scrapy.Field()
    classify = scrapy.Field()
    hospital_level = scrapy.Field()
    hospital_type = scrapy.Field()
    address = scrapy.Field()
    post = scrapy.Field()
    telephone = scrapy.Field()
    fax = scrapy.Field()
    email = scrapy.Field()
    employee_num = scrapy.Field()
    director_num = scrapy.Field()
    deputy_director_num = scrapy.Field()
    bed_num = scrapy.Field()
    open_bed_num = scrapy.Field()

