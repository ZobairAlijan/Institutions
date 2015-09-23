# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import University


class BarclayEduSpider(scrapy.Spider):
    """
    Scrape faculty member profiles from
    http://www.barclaycollege.edu

    """
    name = "barclay"
    allowed_domains = ["barclaycollege.edu"]
    start_urls = (
        'http://www.barclaycollege.edu/about/faculty/',
        'http://www.barclaycollege.edu/about/staff/',
        'http://www.barclaycollege.edu/about/administration/',
    )

    def parse(self, response):
        """
        Parse profiles page

        """
        sel = Selector(response)
        people_sel = sel.xpath('//div[@class="row"]')

        for barclay_sel in people_sel:
            item = University()

            name = barclay_sel.xpath('//div[@class="well"]/h4/strong/text()').extract()
            if name:
                item['name'] = ' '.join([x.strip() for x in name])

            title = barclay_sel.xpath('//div[@class="well"]/div/strong/text()').extract()
            if title:
                item['title'] = ' '.join([x.strip() for x in title])

            department = barclay_sel.xpath('//div[@class="well"]/div[1]/text()').extract()
            if department:
                item['department'] = ' '.join([x.strip() for x in department])

            item['institution'] = 'Barclay College',

            email = barclay_sel.xpath('//div[@class="well"]/a/@href').extract()
            if email:
                item['email'] = ' '.join([x.strip() for x in email])

            return item


