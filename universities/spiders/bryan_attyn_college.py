# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import University


class MendozaNdEduSpider(scrapy.Spider):
    """
    Scrape all profiles from
    http://www.brynathyn.edu

    """
    name = "bryan"
    allowed_domains = ["brynathyn.edu"]
    start_urls = (
        'http://www.brynathyn.edu/about/directory/faculty/',
    )

    def parse(self, response):
        """
        Parse profiles page

        """
        sel = Selector(response)
        people_sel = sel.xpath('//div[@class="staff-member-listing faculty"]')

        for profile_sel in people_sel:
            item = University()

            name = profile_sel.xpath('//a[@class="accordion-toggle"]/strong/text()').extract()

            if name:
                item['name'] = name

            title = profile_sel.xpath('//a[@class="accordion-toggle"]/text()').extract()
            if title:
                item['title'] = title

            item['institution'] = 'Bryn Athyn'

            email = profile_sel.xpath('//a[@class="staff-member-email"]/text()').extract()
            if email:
                item['email'] = email

            phone = profile_sel.xpath('//div[@class="accordion-body"]/div/text()').extract()
            if phone:
                item['phone'] = phone
            return item


