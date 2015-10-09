# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import University


class RomancelitSpider(scrapy.Spider):
    """
    Scrape all faculty members profiles from
    http://www.romance.nd.edu

    """
    name = "nd_romance"
    allowed_domains = ["romancelanguages.nd.edu"]
    start_urls = (
        'http://romancelanguages.nd.edu/people/all-faculty-by-alpha/',
    )

    def parse(self, response):
        """
        Getting links from Notre Dame university's Romance Languages and Literature department

        """
        selection = Selector(response)

        romance_links = selection.xpath('//div[@role="main"]/ul/li/a/@href').extract()
        for this_link in romance_links:
            p_link = 'http://www.romancelanguages.nd.edu%s' % this_link
            request = Request(p_link,
                              callback=self.parse_romance_lit)
            print request
            yield request

    def parse_romance_lit(self, response):
        """
        Parse profile page

        """

        romance_lit = University()

        sel = Selector(response)

        name = sel.xpath('//h1[@class="page-title"]/text()').extract()
        if name:
            romance_lit['name'] = ' '.join([x.strip() for x in name[0].split('\r\n') if x.strip()])

        title = sel.xpath('//h1[@class="page-title"]/text()').extract()
        if title:
            romance_lit['title'] = ' '.join([x.strip() for x in title[0].split('\r\n') if x.strip()])

        romance_lit['department'] = 'Romance Language and Literature'
        romance_lit['division'] = 'Arts and Letters'
        romance_lit['institution'] = 'Virginia Tech'

        phone = sel.xpath('//h3[contains(text(), "Contact Information")]/following-sibling::p/text()').extract()[1]
        if phone:
            romance_lit['phone'] = ''.join(phone for phone in phone if phone.isdigit())

        email = sel.xpath('//h3[contains(text(), "Contact Information")]/following-sibling::p/a/text()').extract()
        if email:
            romance_lit['email'] = email[0].strip()
        return romance_lit

"""
The department of Romance in Notre Dame also has the following information for faculty members

Degrees and research profile

"""