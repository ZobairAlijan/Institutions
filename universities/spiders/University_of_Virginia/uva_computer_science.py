# -*- coding: utf-8 -*-

import scrapy
from scrapy.selector import Selector
from scrapy.http import Request
from universities.items import University

class ComputerScienceSpider(scrapy.Spider):
    """
    Scrape all profiles of faculty members from
    http://www.cs.virginia.edu

    """
    name = "computer"
    allowed_domains = ["sociology.virginia.edu"]
    start_urls = (
        'http://www.cs.virginia.edu/people/faculty/',
    )
    other_urls = [
        'http://www.cs.virginia.edu',
    ]

    def start_requests(self):
        requests = list(super(ComputerScienceSpider, self).start_requests())
        requests += [scrapy.Request(x, self.parse_other) for x in self.other_urls]
        return requests

    def parse(self, response):
        """
        Parsing faculty members profiles page from department of computer science

        """
        sel = Selector(response)
        computer_sel = sel.xpath('//table[@width="100%"]')

        for computer_sel in computer_sel:
            item = University()

            name = computer_sel.xpath('//tr/td/h3/text()').extract()
            if name:
                item['name'] = ' '.join([name.strip() for name in name])

            title = computer_sel.xpath('//tr/td/p/i/text()').extract()
            if title:
                item['title'] = ' '.join([title.strip() for title in title])

            item['department'] = 'Computer Science'
            item['institution'] = 'University of Virginia'
            item['division'] = 'School of Engineering'

            email = computer_sel.xpath('//tr/td/p[2]/a[1]/text()').extract()
            if email:
                item['email'] = email

            phone = computer_sel.xpath('string(//tr/td/p[2])').re(r"Phone: (\d+-\d+-\d+)")
            if phone:
                item['phone'] = ' '.join([phone.strip() for phone in phone])

            url = computer_sel.xpath('//tr/td/p[2]/a[2]/@href').extract()
            if url:
                item['url'] = ' '.join([url.strip() for url in url])

            return item

    def parse_other(self, response):
        pass
