# -*- coding: utf-8 -*-
import scrapy
import re
from universities.items import University


class MusicSpider(scrapy.Spider):
    name = "music"
    allowed_domains = ["music.nd.edu"]
    start_urls = (
        'http://music.nd.edu/people/faculty-by-alpha/',
    )

    def parse(self, response):

        for i in xrange(2,5):
            for e_url in response.xpath('//main/ul[%d]/li/a/@href' % i).extract():
                yield scrapy.Request(response.urljoin(e_url), meta={}, callback=self.parse_member)

    def parse_member(self, response):

        params = dict(name=response.xpath('//h1[@class="page-title"]/text()').extract_first())
        params['email'] = response.xpath('//main//a[contains(@href,"mailto:")]/text()').extract_first()

        try:
            params['phone'] = self.get_phone_number(response.xpath
                                                    ('//main//a[contains(@href,"mailto:")]/../text()').extract())
        except:
            params['phone'] = ''
        if response.xpath('//main/p[@class="image-left"]').extract() or \
                response.xpath('//main/p[@class="image-right"]').extract():
            params['title'] = response.xpath('//main/p[2]/text()').extract_first()
        else:
            params['title'] = response.xpath('//main/p[1]/text()').extract_first()

        yield University(**params)

    def get_phone_number(self, lst):
        for e in lst:
            if re.match(r'\s+?(\(\d{3}-?\)\s?\d{3}\s?-\s?\d{3})', e) is not None \
                    or re.match(r'\s+?\d{3}-\d{2}-\d{3}-\d{3}-\d{4}', e) is not None \
                    or re.match(r'\s+?(\d{3}-?\s?\d{3}\s?-\s?\d{3})', e) is not None:
                return e.replace('\r', '').replace('\n', '')
