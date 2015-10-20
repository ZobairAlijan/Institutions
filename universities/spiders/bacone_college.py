# -*- coding: utf-8 -*-

import scrapy
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
            bacone = University()

            name = profile_sel.xpath('//table[@class="directory table table-bordered"]//tr/td/a/b/text()').extract()
            if name:
                bacone['name'] = ' '.join([name.strip() for name in name])

            title = profile_sel.xpath('//table[@class="directory table table-bordered"]//tr//td[2]/text()').extract()
            if title:
                bacone['title'] = ' '.join([title.strip() for title in title])

            bacone['institution'] = 'Bacone College'
            email = profile_sel.xpath('//table[@class="directory table table-bordered"]//tr/td[2]/a[2]/text()').extract()
            if email:
                bacone['email'] = email

            phone = profile_sel.xpath('//table[@class="directory table table-bordered"]//tr/td/a/text()').extract()
            if phone:
                bacone['phone'] = ' '.join([phone.strip() for phone in phone])

            url = profile_sel.xpath('//table[@class="directory table table-bordered"]//tr/td[1]/a[1]/@href').extract()
            if url:
                bacone['url'] = url
            return bacone


