# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import BelmontAbbeyEdu


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
        people_sel = sel.xpath('//table[@id="tablepress-15"]/tbody/tr')

        for belmont_sel in people_sel:
            item = BelmontAbbeyEdu()

            last_name = belmont_sel.xpath('//tbody[@class="row-hover"]/tr/td[1]/text()').extract()
            if last_name:
                item['last_name'] = last_name

            first_name = belmont_sel.xpath('//tbody[@class="row-hover"]/tr/td[2]/text()').extract()
            if first_name:
                item['first_name'] = first_name

            title = belmont_sel.xpath('//tbody[@class="row-hover"]/tr/td[3]/text()').extract()
            if title:
                item['title'] = title

            institution = belmont_sel.xpath('//tbody[@class="row-hover"]/tr/td[4]/text()').extract()
            if institution:
                item['institution'] = institution
            return item
