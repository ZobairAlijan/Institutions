# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import University


class BabsonEduSpider(scrapy.Spider):

    """
    Scrape all profiles from
    http://www.sociology.nd.edu

    """
    name = "nd_sociology"
    allowed_domains = ["sociology.nd.edu"]
    start_urls = (
        'http://sociology.nd.edu/people/faculty-by-alpha/',
    )

    def parse(self, response):
        """
        Getting links from department of sociology

        """
        sel = Selector(response)

        links = sel.xpath('//div[@class="column in"]//div/h2/a/@href').extract()
        for link in links:
            p_link = 'http://www.sociology.nd.edu%s' %link
            request = Request(p_link,
                callback=self.parse_profile_page)
            yield request

    def parse_profile_page(self, response):
        """
        Parse faculty member profile

        """

        socio = University()

        sel = Selector(response)

        name = sel.xpath('//h1[@class="page-title"]/text()').extract()
        if name:
            socio['name'] = ' '.join([x.strip() for x in name[0].split('\r\n') if x.strip()])

        title = sel.xpath('//div[@class="column in"]//p/text()').extract()
        if title:
            socio['title'] = ' '.join([x.strip() for x in title[0].split('\r\n') if x.strip()])

        socio['institution'] = 'Notre Dame'
        socio['department'] = 'Sociology'

        email = sel.xpath('//div[@class="column in"]//p/a/text()').extract()
        if email:
            socio['email'] = email[0].strip()

        phone = sel.xpath('//div[@class="column in"]//p/text()').extract()
        if phone:
            socio['title'] = ' '.join([phone.strip() for phone in phone.isdigit()])
        return socio


