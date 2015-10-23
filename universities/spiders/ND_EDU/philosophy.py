# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from universities.items import University
import re


class PhilosophySpider(scrapy.Spider):
    name = "philosophy"
    allowed_domains = ["philosophy.nd.edu"]
    start_urls = (
        'http://philosophy.nd.edu/people/faculty-by-alpha/',
    )

    def parse(self, response):

        for e_url in response.xpath('//tr/td[1]//a/@href').extract():
            if 'http' not in e_url.lower():
                yield scrapy.Request(response.urljoin(e_url), callback=self.parse_member)

    def parse_member(self, response):
        params = dict(name=response.xpath('//h1[@class="page-title"]/text()').extract_first())

        params['phone'] = self.get_phone_number(self.clear_p(Selector(response).xpath('//div[@id="alpha"]').extract_first()).splitlines())
        params['email'] = self.get_email(self.clear_p(Selector(response).xpath('//div[@id="alpha"]').extract_first()).splitlines())

        if response.xpath('//div[@id="alpha"]/p[@class="image-default"]').extract():
            params['title'] = response.xpath('//div[@id="alpha"]/p[2]/text()').extract_first()
        else:
            params['title'] = response.xpath('//div[@id="alpha"]/p[1]/text()').extract_first()

        yield University(**params)

    def get_phone_number(self, lst):
        for e in lst:
            if re.match(r'(?:\s+)?phone:.+?(.+)', e.lower()) is not None:
                return re.match(r'(?:\s+)?phone:.+?(.+)', e.lower()).group(1)

    def get_email(self, lst):
        for e in lst:
            if re.match(r'(?:\s+)?e-?mail:.+?(.+)', e.lower()) is not None:
                return re.match(r'(?:\s+)?e-?mail:.+?(.+)', e.lower()).group(1).replace(' ', '')

    def clear_p(self, html_text):
        html_text = re.sub(r'(</?br/?>|</li>|</ul>)', r'\n', html_text)
        html_text = re.sub(r'(<.+?>)', r' ', html_text)
        return html_text

