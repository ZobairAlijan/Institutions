# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import University


class NdSchoolOfLawSpider(scrapy.Spider):
    """
    Scrape all profiles from
    http://www.law.nd.edu

    """
    name = "nd_law"
    allowed_domains = ["law.nd.edu"]
    start_urls = (
        'http://law.nd.edu/faculty/',
    )

    def parse(self, response):
        """
        Getting links from Law School

        """
        sel = Selector(response)

        links = sel.xpath('//ul[@class="directory-list"]/li/a/@href').extract()
        for link in links:
            law_link = 'http://www.law.nd.edu%s' % link
            request = Request(law_link, callback=self.parse_law_school_page)
            yield request

    def parse_law_school_page(self, response):
        """
        Parse profile page

        """

        law = University()

        sel = Selector(response)

        name = sel.xpath('//h1[@class="page-title"]/text()').extract()
        if name:
            law['name'] = ' '.join([x.strip() for x in name[0].split('\r\n') if x.strip()])

        title = sel.xpath('//p[@class="directory-title"]/text()').extract()
        if title:
            law['title'] = ' '.join([x.strip() for x in title[0].split('\r\n') if x.strip()])

        law['institution'] = 'Notre Dame'

        email = sel.xpath('//b[contains(text(), "Email:")]/following-sibling::a/text()').extract()
        if email:
            law['email'] = email[0].strip()

        phone = sel.xpath('//b[contains(text(), "Phone:")]/following-sibling::text()').extract()
        if phone:
            law['phone'] = phone[0].strip()

        return law
