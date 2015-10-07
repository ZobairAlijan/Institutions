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
    name = "real"
    allowed_domains = ["realestate.vt.edu"]
    start_urls = (
        'http://www.realestate.vt.edu/people/index.html',
    )

    def parse(self, response):
        """
        Parse profiles page

        """
        sel = Selector(response)
        people_sel = sel.xpath('//div[@id="vt_body_col"]')

        for profile_sel in people_sel:
            bii = BabsonEduItem()

            name = profile_sel.xpath('//div[@id="vt_body"]//tr/td[2]/a/text()').extract()
            if name:
                bii['name'] = name

            title = profile_sel.xpath('//div[@id="vt_body"]//tr/td[3]/text()').extract()
            if title:
                bii['title'] = title

            department = profile_sel.xpath('div/div/span[@class="person-department"]/a/text()').extract()
            if department:
                bii['department'] = department
            bii['department'] = 'Real State'
            bii['institution'] = 'Virginia Tech'

            email = profile_sel.xpath('//div[@id="vt_body"]//tr/td[4]/a/text()').extract()
            if email:
                bii['email'] = email

            phone = profile_sel.xpath('//div[@id="vt_body"]//tr/td[5]/text()').extract()
            if phone:
                bii['phone'] = phone

            return bii


