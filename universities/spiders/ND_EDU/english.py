# -*- coding: utf-8 -*-
import scrapy
from universities.items import University
import re


class EnglishSpider(scrapy.Spider):
    name = "english"
    allowed_domains = ["english.nd.edu"]
    start_urls = (
        'http://english.nd.edu/people/faculty/faculty-by-alpha/',
    )

    def parse(self, response):
        yield scrapy.Request('http://english.nd.edu/people/faculty/newman/', meta={}, callback=self.parse_member)

        for e_url in response.xpath('//tbody/tr/td[1]/a/@href').extract():
            yield scrapy.Request(response.urljoin(e_url), meta={}, callback=self.parse_member)

    def parse_member(self, response):
        params = dict(
            name=response.xpath('//h1[@class="page-title"]/text()').extract_first())
        params['email'] = response.xpath('//main//a[contains(@href,"mailto:")]/text()').extract_first()

        try:
            params['phone'] = self.get_phone_number(response.xpath
                                                    ('//main//a[contains(@href,"mailto:")]/../text()').extract())
        except:
            params['phone'] = ''

        if response.xpath('//main/p[@class="image-left"]').extract() or response.xpath\
                    ('//main/p[@class="image-right"]').extract():
            params['title'] = response.xpath('//main/p[2]/strong/text()').extract_first()
        else:
            params['title'] = response.xpath('//main/p[1]/strong/text()').extract_first()

        yield University(**params)

    def get_phone_number(self, lst):
        for e in lst:
            if re.match(r'\s+?(\(\d{3}-?\)\s?\d{3}\s?-\s?\d{3})', e) is not None \
                    or re.match(r'\s+?\d{3}-\d{2}-\d{3}-\d{3}-\d{4}', e) is not None:
                return e.replace('\r', '').replace('\n', '')


