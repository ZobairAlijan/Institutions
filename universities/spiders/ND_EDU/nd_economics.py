# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import University


class EconomicsSpider(scrapy.Spider):
    """
    Scrape all faculty members profiles from
    http://www.economics.nd.edu

    """
    name = "nd_economics"
    allowed_domains = ["economics.nd.edu"]
    start_urls = (
        'http://economics.nd.edu/the-faculty/',
    )

    def parse(self, response):
        """
        Getting links from Notre Dame university's Economics department

        """
        selection = Selector(response)

        design_links = selection.xpath('//div[@id="content_main"]//tr/td/p/strong/a[1]/@href').extract()
        for this_link in design_links:
            p_link = 'http://www.economics.nd.edu%s' % this_link
            request = Request(p_link,
                              callback=self.parse_art_history)
            print request
            yield request

    def parse_art_history(self, response):
        """
        Parse profile page

        """

        economics = University()

        sel = Selector(response)

        name = sel.xpath('//div[@id="content_main"]//h1/text()').extract() + \
            sel.xpath('//div[@id="content_main"]/h1/text()').extract()

        if name:
            economics['name'] = ' '.join([x.strip() for x in name[0].split('\r\n') if x.strip()])

        title = sel.xpath('//div[@id="content_main"]//h2/text()').extract()
        if title:
            economics['title'] = ' '.join([x.strip() for x in title[0].split('\r\n') if x.strip()])

        economics['department'] = 'Economics'
        economics['division'] = 'College of Arts and Letters'
        economics['institution'] = 'Notre Dame'

        phone = sel.xpath('//em[contains(text(), "Phone")]/following-sibling::text()').extract()
        if phone:
            economics['phone'] = ''.join(phone for phone in phone if phone.isdigit())

        email = sel.xpath('//em[contains(text(), "Email")]/following-sibling::a/text()').extract()
        if email:
            economics['email'] = email[0].strip()
        return economics

"""
The department of Economics in Notre Dame also has the following information for faculty members

Areas of interests, Other affiliations, personal website, Education and Bio

"""