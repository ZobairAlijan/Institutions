# -*- coding: utf-8 -*-

import scrapy
from scrapy.selector import Selector

from universities.items import University


class RealStateEduSpider(scrapy.Spider):
    """
    Scrape all profiles from
    http://www.realestate.vt.edu

    """
    name = "real"
    allowed_domains = [
        "realestate.vt.edu",
    ]
    start_urls = (
        'http://www.realestate.vt.edu/people/index.html',
    )

    def parse(self, response):
        """
        Parse faculty profile from department of real state

        """
        sel = Selector(response)
        people_sel = sel.xpath('//div[@id="vt_body_col"]')

        for profile_sel in people_sel:
            real_state = University()

            name = profile_sel.xpath('//div[@id="vt_body"]//tr/td[2]/a/text()').extract()
            if name:
                real_state['name'] = name

            title = profile_sel.xpath('//div[@id="vt_body"]//tr/td[3]/text()').extract()
            if title:
                real_state['title'] = title

            department = profile_sel.xpath('div/div/span[@class="person-department"]/a/text()').extract()
            if department:
                real_state['department'] = department
            real_state['department'] = 'Real State'
            real_state['institution'] = 'Virginia Tech'

            email = profile_sel.xpath('//div[@id="vt_body"]//tr/td[4]/a/text()').extract()
            if email:
                real_state['email'] = email

            phone = profile_sel.xpath('//div[@id="vt_body"]//tr/td[5]/text()').extract()
            if phone:
                real_state['phone'] = phone

            return real_state

