# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import University


class GermanRussianSpider(scrapy.Spider):
    """
    Scrape all profiles from
    http://www.mendoza.nd.edu

    """
    name = "germanandrussian"
    allowed_domains = ["germanandrussian.nd.edu"]
    start_urls = (
        'http://germanandrussian.nd.edu/german-faculty/',
    )

    def parse(self, response):
        """
        Parse profiles page

        """
        sel = Selector(response)
        people_sel = sel.xpath('//div[@class="alpha"]')

        for profile_sel in people_sel:
            item = University()

            name = profile_sel.xpath('//div[@class="alpha"]/h4/text()').extract()
            if name:
                item['name'] = name

            title = profile_sel.xpath('//div[@class="alpha"]/p/text()').extract()
            if title:
                item['title'] = title

            item['department'] = 'German Languages'

            item['institution'] = 'Notre Dame'

            email = profile_sel.xpath('//div[@class="alpha"]/p[4]/a[1]/@href').extract()
            if email:
                item['email'] = email

            phone = profile_sel.xpath('//div[@class="alpha"]/p[2]/text()').extract()
            if phone:
                item['phone'] = ' '.join(phone for phone in phone if phone.isdigit())

            # url = profile_sel.xpath('//div[@class="alpha"]/p[3]/text()').extract()
            # if url:
            #     item['url'] =
            return item