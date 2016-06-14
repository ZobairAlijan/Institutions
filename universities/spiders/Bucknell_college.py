# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import University


 class BabsonEduSpider(scrapy.Spider):
    """
    Scrape all profiles from
    http://www.babson.edu

    """
    name = "bucknell"
    allowed_domains = ["bucknell.edu"]
    start_urls = (
        'http://www.bucknell.edu/script/communication/EverythingDirectory/',
    )

    def parse(self, response):
        """
        Get links from Bucknelll college

        """
        sel = Selector(response)

        links = sel.xpath\
            ('//div[@class="mobile-full tablet-full desktop-full listing everything_listing margin_top_small"]'
             '//div/h3/a/@href').extract()
        for link in links:
            p_link = 'http://www.bucknell.edu%s' % link
            request = Request(p_link,
                              callback=self.parse_bucknell_page)
            yield request

    def parse_bucknell_page(self, response):
        """
        Parse profile page

        """
        this_item = University()
        sel = Selector(response)

        name = sel.xpath('//table[@id="tblResults"]//tr/td[2]/span/text()').extract()
        if name:
            this_item['name'] = ' '.join([name.strip() for name in name])

        title = sel.xpath('//table[@id="tblResults"]//tr[12]/td[2]/text()').extract()
        if title:
            this_item['title'] = ' '.join([title.strip() for title in title])

        department = sel.xpath('//table[@id="tblResults"]//tr[11]/td[2]/text()').extract()
        if department:
            this_item['department'] = department

        this_item['institution'] = 'Bucknell College'

        email = sel.xpath('//table[@id="tblResults"]//tr[4]/td[2]/a/text()').extract() + \
            sel.xpath('//table[@id="tblResults"]//tr[5]/td[2]/a/text()').extract()
        if email:
            this_item['email'] = email

        phone = sel.xpath('//table[@id="tblResults"]//tr[6]/td[2]/text()').extract()
        if phone:
            this_item['phone'] = ' '.join([phone.strip() for phone in phone])
        return this_item

