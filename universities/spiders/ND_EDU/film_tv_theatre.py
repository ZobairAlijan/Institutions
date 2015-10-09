# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import University


class FilmTvTheatreSpider(scrapy.Spider):
    """
    Scrape all faculty members profiles from
    http://www.romance.nd.edu

    """
    name = "film"
    allowed_domains = ["ftt.nd.edu"]
    start_urls = (
        'http://ftt.nd.edu/faculty-staff/',
    )

    def parse(self, response):
        """
        Getting links from department of Film, Television and Theatre

        """
        selection = Selector(response)

        design_links = selection.xpath('//ul[@class="col-grid"]//ul/li/a/@href').extract()
        for this_link in design_links:
            p_link = 'http://www.ftt.nd.edu%s' % this_link
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

        name = sel.xpath('//h1[@class="page-title"]/text()').extract()
        if name:
            history_design['name'] = ' '.join([x.strip() for x in name[0].split('\r\n') if x.strip()])

        title = sel.xpath('//main[@role="main"]/p[2]/strong/text()').extract()
        if title:
            history_design['title'] = ' '.join([x.strip() for x in title[0].split('\r\n') if x.strip()])

        department = sel.xpath('//main[@role="main"]/p[2]/strong/text()').extract()
        if department:
            history_design['department'] = ' '.join([x.strip() for x in department[1].split('\r\n') if x.strip()])

        history_design['division'] = 'College of Arts and Letters'
        history_design['institution'] = 'Virginia Tech'

        phone = sel.xpath('//main[@role="main"]/p[3]/text()').extract()
        if phone:
            history_design['phone'] = ' '.join(phone for phone in phone if phone.isdigit())

        email = sel.xpath('//main[@role="main"]/p[3]/a/text()').extract()
        if email:
            history_design['email'] = email[0].strip()
        return history_design

"""
The department of Art Design in Notre Dame also has the following information for faculty members

Degree and Bio

"""