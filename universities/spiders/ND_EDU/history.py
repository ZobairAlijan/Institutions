# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import University


class HistorySpider(scrapy.Spider):
    """
    Scrape all faculty members profiles from
    http://www.history.nd.edu

    """
    name = "history"
    allowed_domains = ["history.nd.edu"]
    start_urls = (
        'http://history.nd.edu/faculty/',
    )

    def parse(self, response):
        """
        Getting links from Notre Dame university's History department

        """
        selection = Selector(response)

        histry_links = selection.xpath('//div[@id="page"]/ul/li/a/@href').extract()
        for this_link in histry_links:
            p_link = 'http://www.history.nd.edu%s' % this_link
            request = Request(p_link,
                              callback=self.parse_history)
            print request
            yield request

    def parse_history(self, response):
        """
        Parse profile page

        """

        history = University()

        sel = Selector(response)

        name = sel.xpath('//div[@id="page"]/h1/text()').extract()
        if name:
            history['name'] = ' '.join([x.strip() for x in name[0].split('\r\n') if x.strip()])

        title = sel.xpath('//h3[contains(text(), "Title")]/following-sibling::p/text()').extract()
        if title:
            history['title'] = ' '.join([x.strip() for x in title[0].split('\r\n') if x.strip()])

        history['department'] = 'History'
        history['division'] = 'Arts and Letters'
        history['institution'] = 'Virginia Tech'

        phone = sel.xpath('//h3[contains(text(), "Contact Information")]/following-sibling::p/text()').extract()[1]
        if phone:
            history['phone'] = ''.join(phone for phone in phone if phone.isdigit())

        email = sel.xpath('//h3[contains(text(), "Contact Information")]/following-sibling::p/a/text()').extract()
        if email:
            history['email'] = email[0].strip()
        return history

"""
The department of history in Notre Dame also has the following information for faculty memebers

Specialization, Education, Research and Teaching Interests, Profiles and CV

"""


