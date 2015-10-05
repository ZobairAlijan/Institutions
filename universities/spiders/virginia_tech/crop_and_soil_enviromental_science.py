# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import University


class CulturalSpider(scrapy.Spider):
    """
    Scrape all faculty members profiles from
    http://www.cses.vt.edu

    """
    name = "soil"
    allowed_domains = ["cses.vt.edu"]
    start_urls = (
        'http://www.cses.vt.edu/people/tenure/index.html',
    )

    def parse(self, response):
        """
        Parse profiles page from department of Crop, Soil, and Environmental Science

        """
        sel = Selector(response)
        people_sel = sel.xpath('//div[@class="col-lg-9"]')

        for agriculture_sel in people_sel:
            item = University()

            name = agriculture_sel.xpath('//td[@style=" width: 195px;"]/a/text()').extract()
            if name:
                item['name'] = name

            title = agriculture_sel.xpath('//td[@style=" width: 138px;"]/text()').extract()
            if title:
                item['title'] = title
            item['department'] = 'Crop, Soil, and Environmental Science'
            item['division'] = 'College of Agriculture and Life Sciences'
            item['institution'] = 'Virginia Tech'

            email = agriculture_sel.xpath('//td[@style =" width: 163px;"]/a/text()').extract()
            if email:
                item['email'] = email

            phone = agriculture_sel.xpath('//td[@style =" width: 117px;"]/text()').extract()
            if phone:
                item['phone'] = phone

            yield item
