# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import University


class BabsonEduSpider(scrapy.Spider):
    """
    Scrape all profiles from
    http://www.americanstudies.nd.edu

    """
    name = "american"
    allowed_domains = ["americanstudies.nd.edu"]
    start_urls = (
        'http://americanstudies.nd.edu/faculty-and-staff/',
    )

    def parse(self, response):
        """
        Get links to profiles

        """
        sel = Selector(response)

        links = sel.xpath('//div[@id="alpha"]//p/strong/a/@href').extract()
        for link in links:
            p_link = 'http://www.americanstudies.nd.edu%s' %link
            request = Request(p_link,
                              callback=self.parse_profile_page)
            yield request

    def parse_profile_page(self, response):
        """
        Parse profile page

        """
        bii = University()

        sel = Selector(response)

        name = sel.xpath('//div[@id="alpha"]/h1/text()').extract() + \
            sel.xpath('//h1[@class="page-title"]/text()').extract()

        if name:
            bii['name'] = ' '.join([name.strip() for name in name])

        title = sel.xpath('//div[@id="alpha"]/p/strong/text()').extract()
        if title:
            bii['title'] = ' '.join([title.strip() for title in title])

        bii['department'] = 'American Study'
        bii['institution'] = 'Notre Dame'

        email = sel.xpath('//div[@id="alpha"]/p/a/text()').extract()
        if email:
            bii['email'] = email[0].strip()

        phone = sel.xpath('//div[@id="alpha"]/p[7]/text()').extract()
        assert isinstance(phone, object)
        if phone:
            bii['phone'] = ''.join(phone for phone in phone if phone.isdigit())
        return bii

"""
The department of American Studies has the following information too:
profile, Courses, Books Articls & chapters and awards

"""


