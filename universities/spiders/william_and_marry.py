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
    name = "m"
    allowed_domains = ["directory.wm.edu/"]
    start_urls = (
        'http://directory.wm.edu/people/namelisting.cfm',
    )

    def parse(self, response):
        """
        Parse profiles page

        """
        sel = Selector(response)
        people_sel = sel.xpath('//div[@class="user_content"]/tr')

        for profile_sel in people_sel:
            bii = BabsonEduItem()

            name = profile_sel.xpath('//tr/td/text()').extract()
            if name:
                bii['name'] = name

            # title = profile_sel.xpath('div/div/span[@class="person-title"]/text()').extract()
            # if title:
            #     bii['title'] = title
            #
            # department = profile_sel.xpath('div/div/span[@class="person-department"]/a/text()').extract()
            # if department:
            #     bii['department'] = department
            #
            # bii['institution'] = 'Mendoza College of Business'
            #
            # email = profile_sel.xpath('div/div/div[@class="person-email"]/a/text()').extract()
            # if email:
            #     bii['email'] = email
            #
            # phone = profile_sel.xpath('div/div/div[@class="person-phone"]/text()').extract()
            # if phone:
            #     bii['phone'] = phone
            return bii


