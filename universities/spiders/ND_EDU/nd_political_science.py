# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import University


class PoliticalScienceSpider(scrapy.Spider):
    """
    Scrape all faculty members profiles from
    http://www.politicalscience.nd.edu

    """
    name = "politicalscience"
    allowed_domains = ["politicalscience.nd.edu"]
    start_urls = (
        'http://politicalscience.nd.edu/faculty/faculty-list/',
    )

    def parse(self, response):
        """
        Getting links from Notre Dame university's politicalscience.nd.edu department

        """
        selection = Selector(response)

        design_links = selection.xpath('//ul[@id="faculty-by-alpha"]/li/a/@href').extract()
        for this_link in design_links:
            p_link = 'http://www.politicalscience.nd.edu%s' % this_link
            request = Request(p_link,
                              callback=self.parse_art_history)
            print request
            yield request

    def parse_art_history(self, response):
        """
        Parse profile page

        """

        history_design = University()

        sel = Selector(response)

        name = sel.xpath('//div[@id="content"]/h1/text()').extract()
        if name:
            history_design['name'] = ' '.join([x.strip() for x in name[0].split('\r\n') if x.strip()])

        title = sel.xpath('//div[@id="content"]/text()').extract()
        if title:
            history_design['title'] = ' '.join([title.strip() for title in title])

        history_design['department'] = 'Political Science'
        history_design['division'] = 'College of Arts and Letters'
        history_design['institution'] = 'Notre Dame'

        phone = sel.xpath('//p[contains(text(), "Phone:")]/following-sibling::strong/text()').extract()
        if phone:
            history_design['phone'] = ''.join(phone for phone in phone if phone.isdigit())

        email = sel.xpath('//p[contains(text(), "Email:")]/following-sibling::strong/a/text()').extract()
        if email:
            history_design['email'] = email[0].strip()
        return history_design

"""
The department of Art Design in Notre Dame also has the following information for faculty members

Degree and Bio

"""