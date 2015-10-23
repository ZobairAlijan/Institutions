# -*- coding: utf-8 -*-

import scrapy
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

            name = faculty_sel.xpath('//tr[@class="degree"]/td[2]/a/text()').extract()
            if name:
                ab['name'] = ' '.join([name.strip() for name in name])

            title = faculty_sel.xpath('//tr[@class="degree"]/td[4]/text()').extract()
            if title:
                ab['title'] = ' '.join([title.strip() for title in title])

            department = faculty_sel.xpath('//tr[@class="degree"]/td[3]/text()').extract()
            if department:
                ab['department'] = ' '.join([department.strip() for department
                                             in department])

            ab['institution'] = 'Abraham Baldwin College'

            email = faculty_sel.xpath('//table[@class="directory table table-bordered"]'
                                      '//tr/td[4]/a/text()').extract_first()[0]
            if email:
                ab['email'] = email

            phone = faculty_sel.xpath('//tr[@class="degree"]/td/p/text()').extract()
            if phone:
                ab['phone'] = phone

            url = faculty_sel.xpath('//tr[@class="degree"]/td/a/@href').extract()
            if url:
                ab['url'] = url
            return ab
