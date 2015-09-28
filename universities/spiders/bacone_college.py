# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import University


class BethanyLutheranSpider(scrapy.Spider):
    """
    Scrape all profiles from
    http://www.bacone.edu

    """
    name = "bacone"
    allowed_domains = ["bacone.edu"]
    start_urls = (
        'http://www.bacone.edu/directory/',
    )

    def parse(self, response):
        """
        Parse profiles page

        """
        sel = Selector(response)
        people_sel = sel.xpath('//table[@class="directory table table-bordered"]')

        for profile_sel in people_sel:
            bii = University()

            name = profile_sel.xpath('//td/a[1]/b/text()').extract()
            if name:
                bii['name'] = name

            title = profile_sel.xpath('//tr/td[2]/text()').extract()
            if title:
                bii['title'] = ' '.join([title.strip() for title in title])

            bii['institution'] = 'Bacone College'
            email = profile_sel.xpath('//tr/td[4]/a/text()').extract()
            if email:
                bii['email'] = email

            phone = profile_sel.xpath('//tr/td[4]/a[1]/text()').extract()
            if phone:
                bii['phone'] = phone

            url = profile_sel.xpath('//tr/td[1]/a/@href').extract()
            if url:
                bii['url'] = url
            return bii


