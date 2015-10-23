# -*- coding: utf-8 -*-

import scrapy
from scrapy.selector import Selector

from universities.items import Bethany


class BelmontAbbeyEduSpider(scrapy.Spider):
    """
    Scrape all faculty members from
    http://belmontabbeycollege.edu

    """
    name = "belmont"
    allowed_domains = ["belmontabbeycollege.edu"]
    start_urls = (
        'http://belmontabbeycollege.edu/academics/office-of-academic-affairs/alphabetical/',

    )

    def parse(self, response):
        """
        Parse profiles page

        """
        sel = Selector(response)
        people_sel = sel.xpath('//tbody[@class="row-hover"]')

        for belmont_sel in people_sel:
            item = Bethany()

            last_name = belmont_sel.xpath('//tr/td[1]/text()').extract()
            if last_name:
                item['last_name'] = last_name

            first_name = belmont_sel.xpath('//tr/td[2]/text()').extract()
            if first_name:
                item['first_name'] = first_name

            title = belmont_sel.xpath('//tr/td[3]/text()').extract()
            if title:
                item['title'] = title

            item['institution'] = 'Belmont Abbey'
            return item
