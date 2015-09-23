# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import BabsonEduItem


class NotreArchSpider(scrapy.Spider):
    """
    Scrape all profiles from
    http://www.architecture.nd.edu

    """
    name = "nd_arch"
    allowed_domains = ["architecture.nd.edu"]
    start_urls = (
        'http://architecture.nd.edu/people/faculty-directory/',
    )

    def parse(self, response):
        """
        Parse profiles page

        """
        sel = Selector(response)
        people_sel = sel.xpath('//ul[@class="faclist"]/li/a')

        for profile_sel in people_sel:
            bii = BabsonEduItem()

            name = profile_sel.xpath('/text()').extract()
            if name:
                bii['name'] = name[0].strip()

            title = profile_sel.xpath('/text()').extract()
            if title:
                bii['title'] = title[0].strip()

            yield bii
