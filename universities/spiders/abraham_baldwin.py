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
        abraham_sel = sel.xpath('//table[@class="listingInner"]')

        for faculty_sel in abraham_sel:
            ab = University()

            name = faculty_sel.xpath('//tr[@class="degree"]/td/a/text()').extract()
            if name:
                ab['name'] = name[0].strip()

            title = faculty_sel.xpath('//tr[@class="degree"]/td[4]/text()').extract()
            if title:
                ab['title'] = title[0].strip()

            department = faculty_sel.xpath('//tr[@class="degree"]/td[3]/text()').extract()
            if department:
                ab['department'] = department[0].strip()

            ab['institution'] = 'Abraham Baldwin College'

            email = faculty_sel.xpath('//tr[@class="degree"]/td/p/text()').extract()[0]
            if email:
                ab['email'] = email[0].strip()

            phone = faculty_sel.xpath('//tr[@class="degree"]/td/p/text()').extract()[1]
            if phone:
                ab['phone'] = phone[0].strip()

            url = faculty_sel.xpath('//tr[@class="degree"]/td/a/@href').extract()
            if url:
                ab['url'] = url[0].strip()
            return ab


