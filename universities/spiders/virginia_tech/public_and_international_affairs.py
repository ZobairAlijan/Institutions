# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import University


class CulturalSpider(scrapy.Spider):
    """
    Scrape all faculty members profiles from
    http://www.alce.vt.edu

    """
    name = "public"
    allowed_domains = ["spia.vt.edu"]
    start_urls = (
        'http://www.spia.vt.edu/people',
    )

    def parse(self, response):
        """
        Parse profiles page from department of Agriculture, Leadership, and Community education

        """
        sel = Selector(response)
        people_sel = sel.xpath('//div[@class="field-items"]//div/a/@href')

        for agriculture_sel in people_sel:
            item = University()

            name = agriculture_sel.xpath('//div[@class="row"]/div/h60/text()').extract()
            if name:
                item['name'] = name

            title = agriculture_sel.xpath('//table[@width="100%"]//tr/td[2]/text()').extract()
            if title:
                item['title'] = title
            item['department'] = 'Agriculture, Leadership, and Community education'
            item['division'] = 'College of Agriculture and Life Sciences'
            item['institution'] = 'Virginia Tech'

            email = agriculture_sel.xpath('//table[@width="100%"]//tr/td[4]/text()').extract()
            if email:
                item['email'] = email.strip()[0]

            phone = agriculture_sel.xpath('//table[@width="100%"]//tr/td[5]/a/text()').extract()
            if phone:
                item['phone'] = phone.strip()[0]
            return item