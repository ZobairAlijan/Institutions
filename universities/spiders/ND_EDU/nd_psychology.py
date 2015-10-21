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
    name = "nd_psychology"
    allowed_domains = ["psychology.nd.edu"]
    start_urls = (
        'http://psychology.nd.edu/faculty/',
    )

    def parse(self, response):
        """
        Getting links from Notre Dame university's psychology department

        """
        selection = Selector(response)

        design_links = selection.xpath('//div[@id="page-content"]//tr/td[1]/a/@href').extract()
        for this_link in design_links:
            p_link = 'http://www.psychology.nd.edu%s' % this_link
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

        name = sel.xpath('//div[@id="page-header"]/h1/text()').extract()
        if name:
            history_design['name'] = ' '.join([name.strip() for name in name])

        title = sel.xpath('//div[@id="page-content"]/h3[1]/text()').extract() + \
            sel.xpath('//div[@id="page-content"]/h2/strong/text()').extract()

        if title:
            history_design['title'] = ' '.join([title.strip() for title in title])

        history_design['department'] = 'Psychology'
        history_design['division'] = 'College of Arts and Letters'
        history_design['institution'] = 'Notre Dame'

        phone = sel.xpath('//strong[contains(text(), "Phone:")]/following-sibling::text()').extract()
        if phone:
            history_design['phone'] = ' '.join([phone.strip() for phone in phone])

        email = sel.xpath('//strong[contains(text(), "Email:")]/following-sibling::a/text()').extract()
        if email:
            history_design['email'] = ' '.join([email.strip() for email in email])
        return history_design

"""
The department of Psychology in Notre Dame also has the following information for faculty members

Profile and resent papers

"""