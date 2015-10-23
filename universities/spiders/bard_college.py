# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import University

class BardSpider(scrapy.Spider):
    name = "bard"
    allowed_domains = ["bard.edu"]
    start_urls = (
        'http://www.bard.edu/academics/faculty/',
    )

    def parse(self, response):
        """
        Getting links to profiles

        """
        sel = Selector(response)

        links = sel.xpath('//select[@class="acad"]/option').extract()
        for link in links:
            p_link = 'http://www.bard.edu%s' % link
            request = Request(p_link, callback=self.parse_profile_page)
            yield request

    def parse_profile_page(self, response):
        """
        Parse profile page

        """
        item = University()

        sel = Selector(response)

        name = sel.xpath('//div[@id="text"]//text()').extract()
        if name:
            item['name'] = name
        return item
