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
        Get links to profiles

        """
        sel = Selector(response)

        links = sel.xpath('//ul[@class="directory-list"]/li/a/@href').extract()
        for link in links:
            p_link = 'http://www.law.nd.edu%s' %link
            request = Request(p_link,
                callback=self.parse_profile_page)
            yield request

    def parse_profile_page(self, response):
        """
        Parse profile page

        """

        bii = University()

        sel = Selector(response)

        name = sel.xpath('//h1[@class="page-title"]/text()').extract()
        if name:
            bii['name'] = ' '.join([x.strip() for x in name[0].split('\r\n') if x.strip()])

        title = sel.xpath('//p[@class="directory-title"]/text()').extract()
        if title:
            bii['title'] = ' '.join([x.strip() for x in title[0].split('\r\n') if x.strip()])

        bii['institution'] = 'Notre Dame'

        email = sel.xpath('//p[contains(text(), "Email:")]/following-sibling::a/text()').extract()
        if email:
            bii['email'] = email[0].strip()

        phone = sel.xpath('//p[contains(text(), "Phone:")]/following-sibling::text()').extract()
        if phone:
            bii['phone'] = phone[0].strip()

        return bii


