# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import University

class ChemSpider(scrapy.Spider):
    name = "chm"
    allowed_domains = ["classics.virginia.edu"]
    start_urls = (
        'http://www.virginia.edu/cognitivescience/faculty.htm',
    )

    def parse(self, response):
        """
        Getting links to profiles

        """
        sel = Selector(response)

        for link in links:
            p_link = 'http://www.virginia.edu%s' %link
            request = Request(p_link, callback=self.parse_profile_page)
            yield request

    def parse_profile_page(self, response):
        """
        Parse profile page

        """

        item = University()

        sel = Selector(response)

        name = sel.xpath('//b[@style="color: rgb(53, 85, 154);"]/text()').extract()
        if name:
            item['name'] = name

        return item
