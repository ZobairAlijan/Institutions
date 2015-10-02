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
    name = "alce"
    allowed_domains = ["alce.vt.edu"]
    start_urls = (
        'http://www.alce.vt.edu/people/faculty-staff/index.html',
    )

    def parse(self, response):
        """
        Parse profiles page from department of Agriculture, Leadership, and Community education

        """
        sel = Selector(response)
        people_sel = sel.xpath('//div[@class="col-lg-9"]')

        for agriculture_sel in people_sel:
            item = University()

            name = agriculture_sel.xpath('//table[@width="100%"]//tr/td/a/text()').extract()
            if name:
                item['name'] = name

            title = agriculture_sel.xpath('//table[@width="100%"]//tr/td[2]/text()').extract()
            if title:
                item['title'] = title
            item['department'] = 'Agriculture, Leadership, and Community education'
            item['division'] = 'School of Agriculture and Life'
            item['institution'] = 'Virginia Tech'

            email = agriculture_sel.xpath('//table[@width="100%"]//tr/td[4]/text()').extract()
            if email:
                item['email'] = email

            phone = agriculture_sel.xpath('//table[@width="100%"]//tr/td[5]/a/text()').extract()
            if phone:
                item['phone'] = phone

            yield item
