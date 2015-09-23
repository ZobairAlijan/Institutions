# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import uva_edu


class ArchitectureSpider(scrapy.Spider):
    """
    Scrape all profiles from
    http://www.mendoza.nd.edu

    """
    name = "arch"
    allowed_domains = ["arch.virginia.edu"]
    start_urls = (
        'http://www.arch.virginia.edu/people/directory/',
        'http://www.virginia.edu/art/faculty/',
    )

    def parse(self, response):
        """
        Parse profiles page

        """
        sel = Selector(response)

        people_sel = sel.xpath('//div[@class="search-results directory-search-results"]')

        for profile_sel in people_sel:
            bii = uva_edu()

            name = profile_sel.xpath('//a[@class="result clearfix"]/h4/text()').extract()
            if name:
                bii['name'] = name

            title = profile_sel.xpath('//span[@class="position"]/text()').extract()
            if title:
                bii['title'] = title

            bii['department'] = 'architecture'
            bii['institution'] = 'University of Virginia'
            bii['division'] = 'school of architecture'

            email = profile_sel.xpath('//span[@class="email"]/text()').extract()
            if email:
                bii['email'] = email

            phone = profile_sel.xpath('//span[@class="phone"]/text()').extract()
            if phone:
                bii['phone'] = phone
            yield bii



