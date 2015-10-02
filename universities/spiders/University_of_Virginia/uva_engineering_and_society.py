# -*- coding: utf-8 -*-

import scrapy
from scrapy.selector import Selector
from scrapy.http import Request
from universities.items import University

class ComputerScienceSpider(scrapy.Spider):
    """
    Scrape all profiles of faculty members from
    http://www.sts.virginia.edu

    """
    name = "society"
    allowed_domains = ["sts.virginia.edu"]
    start_urls = (
        'http://www.sts.virginia.edu/projects/faculty/',
    )
    other_urls = [
        'http://www.sts.virginia.edu',
    ]

    def start_requests(self):
        requests = list(super(ComputerScienceSpider, self).start_requests())
        requests += [scrapy.Request(x, self.parse_other) for x in self.other_urls]
        return requests

    def parse(self, response):
        """
        Parsing faculty members profiles page from department of Engineering and Society

        """
        sel = Selector(response)
        computer_sel = sel.xpath('//div[@class="project clearfix"]')

        for computer_sel in computer_sel:
            item = University()

            name = computer_sel.xpath('//p/strong/text()').extract() + \
                computer_sel.xpath('//p/a/strong/text()').extract()

            if name:
                item['name'] = ' '.join([name.strip() for name in name])

            title = computer_sel.xpath('//p/strong/text()').extract()
            if title:
                item['title'] = ' '.join([title.strip() for title in title])

            item['department'] = 'Engineering and Society'
            item['institution'] = 'University of Virginia'
            item['division'] = 'School of Engineering'

            return item

    def parse_other(self, response):
        pass
