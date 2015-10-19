# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import University


class NdBiologicalScienceSpider(scrapy.Spider):
    """
    Scrape all profiles from
    http://www.biology.nd.edu

    """
    name = "nd_biology"
    allowed_domains = ["biology.nd.edu"]
    start_urls = (
        'http://biology.nd.edu/people/faculty/',
    )

    def parse(self, response):
        """
        Parse profiles page

        """
        sel = Selector(response)
        people_sel = sel.xpath('//div[@id="page-content"]')

        for profile_sel in people_sel:
            bii = University()

            name = profile_sel.xpath('//div[@id="page-content"]//tr/td[2]/strong/a/text()').extract() + \
                profile_sel.xpath('//div[@id="page-content"]//tr/td[2]/p/a/strong/text()').extract()

            if name:
                bii['name'] = name

            title = profile_sel.xpath('//div[@id="page-content"]//tr/td[2]/text()').extract()
            if title:
                bii['title'] = ' '.join([title.strip() for title in title])

            bii['department'] = 'Biological Science'
            bii['division'] = 'College of Science'
            bii['institution'] = 'Notre Dame'

            email = profile_sel.xpath('//div[@id="page-content"]//tr/td[2]/strong/a/@href').extract() + \
                profile_sel.xpath('//div[@id="page-content"]//tr/td[2]/p/a/strong/@href').extract()
            if email:
                bii['email'] = email

            yield bii


