# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import University


class NdArchitectureSpider(scrapy.Spider):
    """
    Scrape faculty members profile from Arch

    """
    name = "architecturess"
    allowed_domains = ["architecture.nd.edu"]
    start_urls = (
        'http://architecture.nd.edu/people/',
    )

    def start_requests(self):

        yield Request(self.start_urls[0], callback=self.parse_architecture)

    def parse_architecture(self, response):
        """
        Parse School of Architecture

        """
        sel = Selector(response)

        profiles_sel = sel.xpath('//h3[contains(text(), "Administration")]/following-sibling::ul/li') + \
            sel.xpath('//h3[contains(text(), "Staff")]/following-sibling::ul/li')

        for p in profiles_sel:
            link = p.xpath('p/a/@href').extract()
            if link:
                yield Request('http://architecture.nd.edu%s' %link[0], callback=self.parse_arc_profile)
            else:
                architecture = University
                architecture['name'] = p.xpath('descendant-or-self::h3/text()').extract()
                architecture['title'] = p.xpath('descendant-or-self::p[2]/text()').extract()
                architecture['institution'] = 'School of Architecture'
                yield architecture

    def parse_arc_profile(self, response):
        sel = Selector(response)

        architecture = University()
        architecture['name'] = sel.xpath('//h1/text()').extract()
        architecture['title'] = sel.xpath('//h2/text()').extract()
        architecture['institution'] = 'School of Architecture'
        phone = sel.xpath('//b[contains(text(), "Phone:")]/following-sibling::text()').extract()
        if phone:
            architecture['phone'] = phone

        email = sel.xpath('//b[contains(text(), "Email:")]/following-sibling::a/text()').extract()
        if email:
            architecture['email'] = email
        yield architecture

