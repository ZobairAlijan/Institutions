# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BabsonEduItem(scrapy.Item):
    name = scrapy.Field()
    title = scrapy.Field()
    department = scrapy.Field()
    institution = scrapy.Field()
    email = scrapy.Field()
    phone = scrapy.Field()
    url = scrapy.Field()


class Mendoza_college_of_bussiness(scrapy.Item):
    name = scrapy.Field()
    title = scrapy.Field()
    department = scrapy.Field()
    institution = scrapy.Field()
    email = scrapy.Field()
    phone = scrapy.Field()

class Notre_Dame_college(scrapy.Item):
    name = scrapy.Field()
    title = scrapy.Field()
    department = scrapy.Field()
    division = scrapy.Field()
    institution = scrapy.Field()
    email = scrapy.Field()
    phone = scrapy.Field()

class uva_edu(scrapy.Item):
    name = scrapy.Field()
    title = scrapy.Field()
    department = scrapy.Field()
    institution = scrapy.Field()
    division = scrapy.Field()
    email = scrapy.Field()
    phone = scrapy.Field()
    url = scrapy.Field()


class Delta_State(scrapy.Item):
    name = scrapy.Field()
    title = scrapy.Field()
    department = scrapy.Field()
    institution = scrapy.Field()
    email = scrapy.Field()
    phone = scrapy.Field()
    url = scrapy.Field()


class University(scrapy.Item):
    name = scrapy.Field()
    title = scrapy.Field()
    department = scrapy.Field()
    institution = scrapy.Field()
    email = scrapy.Field()
    phone = scrapy.Field()
    url = scrapy.Field()
    id = scrapy.Field()


class BethanyEdu(scrapy.Item):
    last_name = scrapy.Field()
    first_name = scrapy.Field()
    title = scrapy.Field()
    department = scrapy.Field()
    institution = scrapy.Field()
    email = scrapy.Field()
    phone = scrapy.Field()
    url = scrapy.Field()


