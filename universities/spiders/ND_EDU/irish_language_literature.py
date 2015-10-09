# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import University


class irish_litSpider(scrapy.Spider):
    """
    Scrape all faculty members profiles from
    http://www.irish_lit.nd.edu

    """
    name = "irish"
    allowed_domains = ["irishlanguage.nd.edu"]
    start_urls = (
        'http://irishlanguage.nd.edu/people/',
    )

    def parse(self, response):
        """
        Getting links from Notre Dame university's irish_lit department

        """
        selection = Selector(response)

        irish_links = selection.xpath('//div[@class="main"]/ul/li/a/@href').extract() + \
            selection.xpath('//div[@class="aside"]/p/a/@href').extract()

        for this_link in irish_links:
            p_link = 'http://www.irishlanguage.nd.edu%s' % this_link
            request = Request(p_link,
                              callback=self.parse_irish_lit)
            print request
            yield request

    def parse_irish_lit(self, response):
        """
        Parse profile page

        """

        irish_lit = University()

        sel = Selector(response)

        name = sel.xpath('//h1[@class="page-title"]/text()').extract()
        if name:
            irish_lit['name'] = ' '.join([x.strip() for x in name[0].split('\r\n') if x.strip()])

        title = sel.xpath('//div[@class="alpha"]/p[2]/strong/text()').extract()
        if title:
            irish_lit['title'] = ' '.join([x.strip() for x in title[0].split('\r\n') if x.strip()])

        irish_lit['department'] = 'Irish Language and Literature'
        irish_lit['division'] = 'Arts and Letters'
        irish_lit['institution'] = 'Virginia Tech'

        phone = sel.xpath('//strong[contains(text(), "Phone")]/text()').extract()
        if phone:
            irish_lit['phone'] = ''.join(phone for phone in phone if phone.isdigit())

        email = sel.xpath('//div[@class="alpha"]/p[5]/a/text()').extract()
        if email:
            irish_lit['email'] = email[0].strip()
        return irish_lit

