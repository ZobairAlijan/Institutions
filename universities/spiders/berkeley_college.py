# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import University


class BerkeleySpider(scrapy.Spider):
    """
    Scrape all profiles from
    http://www.berkeleycollege.edu

    """
    name = "berkeley"
    allowed_domains = ["berkeleycollege.edu"]
    start_urls = (
        'http://berkeleycollege.edu/academics_bc/faculty.htm',
    )

    def parse(self, response):
        """
        Parse profiles page

        """
        sel = Selector(response)
        people_sel = sel.xpath('//div[@class="row"]//div')

        for profile_sel in people_sel:
            berk = University()

            name = profile_sel.xpath('//p[@style="widows: 1;"]/strong/text()').extract()
            if name:
                berk['name'] = name

            title = profile_sel.xpath('//p[@style="widows: 1;"]/text()').extract()
            if title:
                berk['title'] = ' '.join([x.strip() for x in title[0].split('\r\n') if x.strip()])

            department = profile_sel.xpath('//a[@class="arrow"]/text()').extract()
            if department:
                berk['department'] = department[0]

            berk['institution'] = 'Berkeley College'

            return berk


