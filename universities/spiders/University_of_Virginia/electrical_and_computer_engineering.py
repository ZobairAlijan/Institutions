# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import University


class ElectricalEngineeringSpider(scrapy.Spider):
    """
    Scrape all profiles from
    http://www.sociology.virginia.edu

    """
    name = "electrical"
    allowed_domains = ["sociology.virginia.edu"]
    start_urls = (
        'http://www.ece.virginia.edu/faculty/',
    )
    other_urls = [
        'http://www.ece.virginia.edu/faculty/',
    ]

    def start_requests(self):
        requests = list(super(ElectricalEngineeringSpider, self).start_requests())
        requests += [scrapy.Request(x, self.parse_other) for x in self.other_urls]
        return requests

    def parse(self, response):
        """
        Parsing faculty members profiles page from department of Engineering and computer science

        """
        my_sel = Selector(response)
        engineering_sel = my_sel.xpath('//div[@id="page-content"]')

        for engin_sel in engineering_sel:
            item = University()

            name = engin_sel.xpath('//tr/td/b/a[2]/text()').extract()
            if name:
                item['name'] = ' '.join([name.strip() for name in name])

            title = engin_sel.xpath('//tr/td/text()').extract()
            if title:
                item['title'] = ' '.join([title.strip() for title in title])

            item['department'] = 'Electrical Engineering and Computer Science'
            item['institution'] = 'University of Virginia'
            item['division'] = 'School of Engineering'

            email = engin_sel.xpath('//tr/td[2]/a/text()').extract()
            if email:
                item['email'] = email

            phone = engin_sel.xpath('//tr/td[2]/text()').extract()
            if phone:
                item['phone'] = ' '.join([phone.strip() for phone in phone])

            url = engin_sel.xpath('//td[@class="views-field views-field-edit-node"]/h4/a/@href').extract()
            if url:
                item['url'] = ' '.join([url.strip() for url in url])
            return item

    def parse_other(self, response):
        pass
