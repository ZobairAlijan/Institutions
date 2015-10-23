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

    name = "nd_classics"
    allowed_domains = ["classics.nd.edu"]
    start_urls = (
        'http://classics.nd.edu/faculty/',
    )

    def parse(self, response):
        """
        Get links to profiles

        """
        sel = Selector(response)

        links = sel.xpath('//div[@id="primary"]/p/a/@href').extract()
        for link in links:
            p_link = 'http://www.classics.nd.edu%s' % link
            request = Request(p_link,
                              callback=self.parse_classics_page)
            yield request

    def parse_classics_page(self, response):
        """
        Parse faculty members profile from the department of classics

        """
        classics_sel = University()

        sel = Selector(response)

        name = sel.xpath('//div[@id="primary"]/h1/text()').extract()
        if name:
            classics_sel['name'] = name

        title = sel.xpath('//div[@id="primary"]/p[1]/text()').extract() + \
            sel.xpath('//div[@id="primary"]/p[2]/text()').extract() + \
            sel.xpath('//div[@id="primary"]/p[1]/span/text()').extract()

        if title:
            classics_sel['title'] = ' '.join([x.strip() for x in title[0].split('\r\n') if x.strip()])

        classics_sel['department'] = 'Classics'
        classics_sel['division'] = 'College of Arts and Letters'
        classics_sel['institution'] = 'Notre Dame'

        email = sel.xpath('//h3[contains(text(), "Contact Information")]/following-sibling::p/a/text()').extract()
        if email:
            classics_sel['email'] = email[0].strip()

        phone = sel.xpath('//h3[contains(text(), "Contact Information")]/following-sibling::p/text()').extract()
        if phone:
            classics_sel['phone'] = phone[1].strip()

        return classics_sel

"""
Department of Classics also has the following information

Research Profile

"""

