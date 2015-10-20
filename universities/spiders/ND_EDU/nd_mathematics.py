# -*- coding: utf-8 -*-
import scrapy
from universities.items import University
import re


class EnglishSpider(scrapy.Spider):
    name = "nd_math"
    allowed_domains = ["math.nd.edu"]
    start_urls = (
        'http://math.nd.edu/people/faculty-directory/teaching-and-research-faculty/',
    )

    def parse(self, response):
        yield scrapy.Request('http://math.nd.edu/people/faculty/katrina-d-barron/', meta={}, callback=self.parse_member)

        for e_url in response.xpath('//tbody/tr/td[1]/a/@href').extract():
            yield scrapy.Request(response.urljoin(e_url), meta={}, callback=self.parse_member)

    def parse_member(self, response):
        params = dict(
            name=response.xpath('//div[@class="faculty"]/h1/text()').extract_first())
        params['email'] = response.xpath('//page-content//a[contains(@href,"mailto:")]/text()').extract_first()

        try:
            params['phone'] = self.get_phone_number(response.xpath
                                                    ('//page-content//a[contains(@href,"mailto:")]/../text()').extract())
        except:
            params['phone'] = ''

            params['title'] = response.xpath('//page-content/h4/strong/text()').extract_first()
        yield University(**params)

    def get_phone_number(self, lst):
        for e in lst:
            if re.match(r'\s+?(\(\d{3}-?\)\s?\d{3}\s?-\s?\d{3})', e) is not None \
                    or re.match(r'\s+?\d{3}-\d{2}-\d{3}-\d{3}-\d{4}', e) is not None:
                return e.replace('\r', '').replace('\n', '')


