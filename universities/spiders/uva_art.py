# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import University


class MendozaNdEduSpider(scrapy.Spider):
    """
    Scrape all profiles from
    http://www.mendoza.nd.edu

    """
    name = "art"
    allowed_domains = ["virginia.edu"]
    start_urls = (
        'http://www.virginia.edu/art/faculty/',
    )

    def parse(self, response):
        """
        Parse profiles page

        """
        sel = Selector(response)
        people_sel = sel.xpath('//div[@id="content"]')

        for profile_sel in people_sel:
            bii = University()

            name = profile_sel.xpath('//div/p/b/a/text()').extract()
            if name:
                bii['name'] = name

            title = profile_sel.xpath('//div/p/i/text()').extract()
            if title:
                bii['title'] = title

            bii ['department'] = 'Art and Science'
            bii ['institution'] = 'University of Virginia'
            #
            # bii['institution'] = 'Mendoza College of Business'
            #
            email = profile_sel.xpath('//div/p/a/@href').extract()
            if email:
                bii['email'] = email
            #
            # phone = profile_sel.xpath('div/div/div[@class="person-phone"]/text()').extract()
            # if phone:
            #     bii['phone'] = phone

            url = profile_sel.xpath('//div/p/b/a/@href').extract()
            if url:
                bii['url'] = url
            yield bii


