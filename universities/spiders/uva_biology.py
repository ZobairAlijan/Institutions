# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import University


class MendozaNdEduSpider(scrapy.Spider):
    """
    Scrape all profiles from
    http://www.mendoza.nd.edu

    """
    name = "bio"
    allowed_domains = ["virginia.edu"]
    start_urls = (
        'http://bio.virginia.edu/faculty-directory',
    )

    def parse(self, response):
        """
        Parse profiles page

        """
        sel = Selector(response)
        people_sel = sel.xpath('//table[@class="views-table cols-5"]')

        for profile_sel in people_sel:
            bii = University()

            name = profile_sel.xpath('//tr/td/text()').extract()
            if name:
                bii['name'] = name[0].strip()

            title = profile_sel.xpath('//tr/td[2]/text()').extract()
            if title:
                bii['title'] = title[0].strip()

            phone = profile_sel.xpath('//tr/td[5]/text()').extract()
            if phone:
                bii['phone'] = phone[0].strip()

            email = profile_sel.xpath('//tr/td[3]/a/@href').extract()
            if email:
                bii['email'] = email[0].strip()

            id = profile_sel.xpath('//tr/td[3]/a/text()').extract()
            if id:
                bii['id'] = id

            bii['department'] = "Biology"
            # bii['institution'] = "University of Virginia"
            # bii['division'] = "Arts and Science"

            return bii


