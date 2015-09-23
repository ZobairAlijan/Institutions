# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import University


class AbrahamBaldwinEduSpider(scrapy.Spider):
    """
    Scrape all faculty members from Abraham Baldwin Agriculture college
    http://www.abac.edu

    """
    name = "abac"
    allowed_domains = ["abac.edu"]
    start_urls = (
        'http://www.abac.edu/more/employees/full-employee-directory',
    )

    def parse(self, response):
        """
        Parse profiles page

        """
        sel = Selector(response)
        people_sel = sel.xpath('//table[@class="listingInner"]')

        for profile_sel in people_sel:
            ab = University()

            name = profile_sel.xpath('//tr[@class="degree"]/td/a/text()').extract()
            if name:
                ab['name'] = name

            title = profile_sel.xpath('//tr[@class="degree"]/td[4]/text()').extract()
            if title:
                ab['title'] = title

            department = profile_sel.xpath('//tr[@class="degree"]/td[3]/text()').extract()
            if department:
                ab['department'] = department

            ab['institution'] = 'Abraham Baldwin College'

            email = profile_sel.xpath('//tr[@class="degree"]/td/p/text()').extract()[0]
            if email:
                ab['email'] = email

            phone = profile_sel.xpath('//tr[@class="degree"]/td/p/text()').extract()[1]
            if phone:
                ab['phone'] = phone

            url = profile_sel.xpath('//tr[@class="degree"]/td/a/@href').extract()
            if url:
                ab['url'] = url
            return ab


