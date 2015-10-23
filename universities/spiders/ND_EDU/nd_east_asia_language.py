# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import University


class NdClassicsSpider(scrapy.Spider):
    """
    Scrape all profiles from
    http://www.classics.nd.edu

    """
    name = "nd_east_asian"
    allowed_domains = ["eastasian.nd.edu"]
    start_urls = (
        'http://eastasian.nd.edu/faculty-and-staff/',
        'http://eastasian.nd.edu/faculty-and-staff/faculty-by-alpha/',
    )

    def parse(self, response):
        """
        Get links to profiles

        """
        sel = Selector(response)

        links = sel.xpath('//div[@id="alpha"]//tr/td/a/@href').extract()
        for link in links:
            p_link = 'http://www.eastasian.nd.edu%s' % link
            request = Request(p_link,
                              callback=self.parse_east_asian_language_page)
            yield request

    def parse_east_asian_language_page(self, response):
        """
        Parse faculty members profile from the department of East Asian Languages and Culture

        """
        east_asian_sel = University()

        sel = Selector(response)

        name = sel.xpath('//h1[@class="page-title"]/text()').extract()
        if name:
            east_asian_sel['name'] = name

        title = sel.xpath('//div[@id="alpha"]/text()').extract()
        if title:
            east_asian_sel['title'] = ' '.join([x.strip() for x in title[4].split('\r\n') if x.strip()])

        east_asian_sel['department'] = 'East Asian Languages and Culture'
        east_asian_sel['division'] = 'College of Arts and Letters'
        east_asian_sel['institution'] = 'Notre Dame'

        phone = sel.xpath('//div[@id="alpha"]/text()').extract()
        if phone:
            east_asian_sel['phone'] = ' '.join([x.strip() for x in phone[6].split('\r\n') if x.strip()])

        email = sel.xpath('//div[@id="alpha"]/a/text()').extract()
        if email:
            east_asian_sel['email'] = email

        return east_asian_sel

"""
Department of East Asian Languages and Culture also has the following information

Education Background and profile

"""

