# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import University


class NdBiologicySpider(scrapy.Spider):
    """
    Scrape all faculty members profiles from
    http://www.romance.nd.edu

    """
    name = "nd_biology"
    allowed_domains = ["biology.nd.edu"]
    start_urls = (
        'http://biology.nd.edu/people/faculty/',
    )

    def parse(self, response):
        """
        Getting links from department of Biological Science

        """
        selection = Selector(response)

        design_links = selection.xpath('//div[@id="page-content"]//tr/td/strong/a/@href').extract() + \
            selection.xpath('//div[@id="page-content"]//tr/td/a/@href').extract()

        for this_link in design_links:
            p_link = 'http://www.biology.nd.edu%s' % this_link
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

        name = sel.xpath('//div[@class="faculty"]/h1/text()').extract()
        if name:
            history_design['name'] = ' '.join([x.strip() for x in name[0].split('\r\n') if x.strip()])

        title = sel.xpath('//div[@class="faculty"]/p/strong/text()').extract()
        if title:
            history_design['title'] = ' '.join([x.strip() for x in title[0].split('\r\n') if x.strip()])

        department = sel.xpath('//div[@class="faculty"]/h3/text()').extract()
        if department:
            history_design['department'] = ' '.join([x.strip() for x in department[1].split('\r\n') if x.strip()])

        history_design['division'] = 'Science'
        history_design['institution'] = 'Notre Dame'

        email = sel.xpath('//div[@class="faculty"]/p/a/@href').extract()
        if email:
            history_design['email'] = email[0].strip()
        return history_design

"""
The department of Art Design in Notre Dame also has the following information for faculty members

Degree and Bio

"""