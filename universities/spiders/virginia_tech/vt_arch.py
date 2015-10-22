# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import University


class ArchEduSpider(scrapy.Spider):
    """
    Scrape all profiles from
    http://www.arch.edu

    """
    name = "vt_arch"
    allowed_domains = ["archdesign.vt.edu"]
    start_urls = (
        'http://www.archdesign.vt.edu/faculty/',
    )

    def parse(self, response):
        sel = Selector(response)
        links = sel.xpath('//ul[@class="faculty-list"]/li/a/@href').extract()
        for link in links:
            p_link = 'http://www.archdesign.vt.edu%s' % link
            request = Request(p_link,
                              callback=self.parse_profile_page)
            yield request

    def parse_profile_page(self, response):
        """
        Parse profile page

        """
        this_arch = University()
        sel = Selector(response)

        name = sel.xpath('//div[@class="faculty-page"]/h2/text()').extract()
        if name:
            this_arch['name'] = name
        return this_arch

