# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import University


class TheologySpider(scrapy.Spider):
    """
    Scrape all faculty members profiles from
    http://www.romance.nd.edu

    """
    name = "theology"
    allowed_domains = ["theology.nd.edu"]
    start_urls = (
        'http://theology.nd.edu/people/',
    )

    def parse(self, response):
        """
        Getting links from Notre Dame university's Theology department

        """
        selection = Selector(response)

        romance_links = selection.xpath('//div[@role="main"]//ul/li/a/@href').extract()


        for this_link in romance_links:
            p_link = 'http://www.theology.nd.edu%s' % this_link
            request = Request(p_link,
                              callback=self.parse_theology)
            yield request

    def parse_theology(self, response):
        """
        Parse profile page

        """

        theology = University()

        sel = Selector(response)

        name = sel.xpath('//h1[@class="page-title"]/text()').extract() + \
            sel.xpath('//div[@id="alpha"]/h1/text()').extract()
        if name:
            theology['name'] = ' '.join([x.strip() for x in name[0].split('\r\n') if x.strip()])

        title = sel.xpath('//div[@role="main"]/p/text()').extract()
        if title:
            theology['title'] = ' '.join([x.strip() for x in title[0].split('\r\n') if x.strip()])

        theology['division'] = 'Arts and Letters'
        theology['institution'] = 'Virginia Tech'

        phone = sel.xpath('//h2[contains(text(), "Contact")]/following-sibling::p/text()').extract()[1]
        if phone:
            theology['phone'] = ''.join(phone for phone in phone if phone.isdigit())

        email = sel.xpath('//h2[contains(text(), "Contact")]/following-sibling::p/a/text()').extract()
        if email:
            theology['email'] = email[0].strip()
        url = sel.xpath('//div[@role="main"]//ul/li/a/@href').extract()
        if url:
            theology['url'] = url
        return theology

"""
The department of theology in Notre Dame also has the following information for faculty members

Degrees and research profile

"""