# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class University(scrapy.Item):
    name = scrapy.Field()
    title = scrapy.Field()
    department = scrapy.Field()
    division = scrapy.Field()
    institution = scrapy.Field()
    email = scrapy.Field()
    phone = scrapy.Field()
    url = scrapy.Field()
    id = scrapy.Field()

class Bethany(scrapy.Item):
    first_name = scrapy.Field()
    last_name = scrapy.Field()
    title = scrapy.Field()
    department = scrapy.Field()
    institution = scrapy.Field()
    email = scrapy.Field()
    phone = scrapy.Field()
    url = scrapy.Field()

class uva_edu(scrapy.Item):
    name = scrapy.Field()
    title = scrapy.Field()
    department = scrapy.Field()
    division = scrapy.Field()
    institution = scrapy.Field()
    email = scrapy.Field()
    phone = scrapy.Field()
    url = scrapy.Field()
    id = scrapy.Field()