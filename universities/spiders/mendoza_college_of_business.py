# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import BabsonEduItem


class MendozaNdEduSpider(scrapy.Spider):
    """
    Scrape all profiles from
    http://www.mendoza.nd.edu

    """
    name = "mendoza"
    allowed_domains = ["mendoza.nd.edu"]
    start_urls = (
        'http://mendoza.nd.edu/research-and-faculty/directory/',
    )

    def parse(self, response):
        """
        Parse profiles page

        """
        sel = Selector(response)
        people_sel = sel.xpath('//ul[@id="people-list"]/li')

        for profile_sel in people_sel:
            bii = BabsonEduItem()

            name = profile_sel.xpath('div/div/b[@class="person-fullname"]/a/text()').extract()
            if name:
                bii['name'] = name

            title = profile_sel.xpath('div/div/span[@class="person-title"]/text()').extract()
            if title:
                bii['title'] = title

            department = profile_sel.xpath('div/div/span[@class="person-department"]/a/text()').extract()
            if department:
                bii['department'] = department

            bii['institution'] = 'Mendoza College of Business'

            email = profile_sel.xpath('div/div/div[@class="person-email"]/a/text()').extract()
            if email:
                bii['email'] = email

            phone = profile_sel.xpath('div/div/div[@class="person-phone"]/text()').extract()
            if phone:
                bii['phone'] = phone
            return bii


