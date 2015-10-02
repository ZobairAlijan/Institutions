# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import University


class SociologySpider(scrapy.Spider):
    """
    Scrape all profiles from
    http://www.sociology.virginia.edu

    """
    name = "gender"
    allowed_domains = ["sociology.virginia.edu"]
    start_urls = (
        'http://wgs.virginia.edu/people/director_staff',
    )
    other_urls = [
        'http://wgs.virginia.edu/people/director_staff',
    ]

    def start_requests(self):
        requests = list(super(SociologySpider, self).start_requests())
        requests += [scrapy.Request(x, self.parse_other) for x in self.other_urls]
        return requests

    def parse(self, response):
        """
        Parsing faculty members profiles page from department of Sociology

        """
        my_sel = Selector(response)
        global_sel = my_sel.xpath('//div[@class="view-content"]')

        for socio_sel in global_sel:
            item = University()

            name = socio_sel.xpath('//td[@class="views-field views-field-field-position"]/h1/a/text()').extract()
            if name:
                item['name'] = ' '.join([name.strip() for name in name])

            title = socio_sel.xpath('//td[@class="views-field views-field-field-position"]/h5/text()').extract()
            if title:
                item['title'] = ' '.join([title.strip() for title in title])

            item['department'] = 'Women Gender and Sexuality'
            item['institution'] = 'University of Virginia'
            item['division'] = 'Arts and Science'

            email = socio_sel.xpath('//td[@class="views-field views-field-field-phone"]/a/text()').extract()
            if email:
                item['email'] = email

            phone = socio_sel.xpath('//td[@class="views-field views-field-field-phone"]/text()').extract()
            if phone:
                item['phone'] = ' '.join([phone.strip() for phone in phone])

            url = socio_sel.xpath('//td[@class="views-field views-field-field-position"]/h1/a/@href').extract()
            if url:
                item['url'] = ' '.join([url.strip() for url in url])
            return item

    def parse_other(self, response):
        pass
