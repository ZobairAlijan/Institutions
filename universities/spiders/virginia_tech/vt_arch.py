# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import BabsonEduItem


class BabsonEduSpider(scrapy.Spider):
    """
    Scrape all profiles from
    http://www.babson.edu

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

        bii = BabsonEduItem()

        sel = Selector(response)

        name = sel.xpath('//div[@class="faculty-page"]/h2/text()').extract()
        if name:
            bii['name'] = ' '.join([x.strip() for x in name[0].split('\r\n') if x.strip()])

        title = sel.xpath('//div[@class="faculty-page"]/h3/text()').extract()
        if title:
            bii['title'] = ' '.join([x.strip() for x in title[0].split('\r\n') if x.strip()])

        bii['department'] = 'Architecture and design'
        bii['disvision'] = 'School of Architecture and design'
        bii['institution'] = 'Virginia Teh'

        email = sel.xpath('//div[@class="faculty-page"]/p[5]/text()').extract()
        if email:
            bii['email'] = email[0].strip()

        return bii


