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
    name = "bioetich"
    allowed_domains = ["bioethics.virginia.edu"]
    start_urls = (
        'http://bioethics.virginia.edu/people',
    )

    def parse(self, response):
        """
        Parse profiles page

        """
        sel = Selector(response)
        people_sel = sel.xpath('//table[@class="views-table cols-0"]')

        for profile_sel in people_sel:
            bii = University()

            name = profile_sel.xpath('//tr/td/h1/a/text()').extract()
            if name:
                bii['name'] = name

            title = profile_sel.xpath('//tr/td/h5/text()').extract()
            if title:
                bii['title'] = title

            url = profile_sel.xpath('//tr/td/h1/a/@href').extract()
            if url:
                bii['url'] = url

            phone = profile_sel.xpath('//tr/td[2]/a/text()').extract()
            if phone:
                bii['phone'] = phone

            email = profile_sel.xpath('//tr/td[2]/text()').extract()
            if email:
                bii['email'] = email

            bii['department'] = "Bioethics"
            bii['institution'] = "University of Virginia"
            bii['division'] = "Arts and Science"

            return bii


