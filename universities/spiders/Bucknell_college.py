# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import University


class BrynMawrSpider(scrapy.Spider):
    """
    Scrape all profiles from
    http://www.bucknell.edu

    """
    name = "buck"
    allowed_domains = ["bucknell.edu"]
    start_urls = (
        'http://www.bucknell.edu/script/communication/EverythingDirectory/',
    )

    def parse(self, response):
        """
        Parsing faculty members profiles page from Bucknell College

        """
        sel = Selector(response)
        link_sel = sel.xpath('//div[@class="row"]')

        for bism_sel in link_sel:
            item = University()

            name = bism_sel.xpath('//article[@class="row item personnel"]/div/h3/a/text()').extract()
            if name:
                item['name'] = name

            title = bism_sel.xpath('//article[@class="row item personnel"]/div[1]/p/text()').extract()
            if title:
                item['title'] = title

            item['institution'] = 'Bucknell University'

            email = bism_sel.xpath('//div[@class="mobile-full tablet-5 desktop-4 max-5 contact"]/p/a/text()').extract()
            if email:
                item['email'] = email

            phone = bism_sel.xpath('//article[@class="row item personnel"]/div/h3/a/@href').extract()
            if phone:
                item['phone'] = ' '.join([phone.strip() for phone in phone])

            return item

