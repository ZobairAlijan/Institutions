# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import University


class SpanishItalianSpider(scrapy.Spider):
    """
    Scrape all profiles from
    http://www.spanitalport.virginia.edu

    """
    name = "spanish"
    allowed_domains = ["spanitalport.virginia.edu"]
    start_urls = (
        'http://spanitalport.virginia.edu/faculty',
        'http://spanitalport.virginia.edu/faculty?page=1'
    )

    def parse(self, response):
        """
        Parse profiles page

        """
        sel = Selector(response)
        people_sel = sel.xpath('//div[@class="view-content"]/table')

        for profile_sel in people_sel:
            item = University()

            name = profile_sel.xpath('//td[@class="views-field views-field-field-position-title"]/h4/a/text()').extract()
            if name:
                item['name'] = name

            title = profile_sel.xpath('//td[@class="views-field views-field-field-position-title"]/h5/text()').extract()
            if title:
                item['title'] = title


            item['department'] = 'Spanish Italian'
            item['institution'] = 'University of Virginia'
            item['division'] = 'Arts and Science'

            email = profile_sel.xpath('//td[@class="views-field views-field-field-email"]/a/text()').extract()
            if email:
                item['email'] = email

            phone = profile_sel.xpath('//td[@class="views-field views-field-field-email"]/span/text()').extract()
            if phone:
                item['phone'] = phone
            return item


