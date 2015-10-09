# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import BabsonEduItem


class ArchEduSpider(scrapy.Spider):
    """
    Scrape all profiles from
    http://www.arch.edu

    """
    name = "ba"
    allowed_domains = ["archdesign.vt.edu"]
    start_urls = (
        'http://www.archdesign.vt.edu/faculty/',
    )

    def parse(self, response):
        """
        Get links to profiles

        """
        sel = Selector(response)

        links = sel.xpath('//ul[@class="faculty-list"]/li/a/@href').extract()
        for link in links:
            p_link = 'http://www.archdesign.vt.edu%s' %link
            request = Request(p_link,
                              callback=self.parse_profile_page)
            yield request

    def parse_profile_page(self, response):
        """
        Parse profile page

        """

        this_arch = BabsonEduItem()

        sel = Selector(response)

        name = sel.xpath('//div[@class="faculty-page"]/h2/text()').extract()
        if name:
            this_arch['name'] = ' '.join([x.strip() for x in name[0].split('\r\n') if x.strip()])

        title = sel.xpath('//div[@class="faculty-page"]/h3/text()').extract()
        if title:
            this_arch['title'] = ' '.join([x.strip() for x in title[0].split('\r\n') if x.strip()])

        this_arch['department'] = 'Architecture and design'
        this_arch['disvision'] = 'School of Architecture and design'
        this_arch['institution'] = 'Virginia Teh'

        email = sel.xpath('//div[@class="faculty-page"]/p[5]/text()').extract()
        if email:
            this_arch['email'] = email[0].strip()

        return this_arch


