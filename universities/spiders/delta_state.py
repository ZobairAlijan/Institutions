# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import Delta_State


class MendozaNdEduSpider(scrapy.Spider):
    """
    Scrape all profiles from
    http://www.mendoza.nd.edu

    """
    name = "delta"
    allowed_domains = ["deltastate.edu"]
    start_urls = (
        'http://www.deltastate.edu/contacts/',
        'http://www.deltastate.edu/contacts/page/2/',
        'http://www.deltastate.edu/contacts/page/3/',
        'http://www.deltastate.edu/contacts/page/4/',
        'http://www.deltastate.edu/contacts/page/5/',
        'http://www.deltastate.edu/contacts/page/6/',
        'http://www.deltastate.edu/contacts/page/7/',
        'http://www.deltastate.edu/contacts/page/8/',
        'http://www.deltastate.edu/contacts/page/9/',
        'http://www.deltastate.edu/contacts/page/10/',
        'http://www.deltastate.edu/contacts/page/11/',

    )

    def parse(self, response):
        """
        Parse profiles page

        """
        sel = Selector(response)
        people_sel = sel.xpath('//table[@class="ecc-contact-table responsive-table"]')

        for profile_sel in people_sel:
            bii = Delta_State()

            name = profile_sel.xpath('//tr/td[@data-title="Name"]/a/text()').extract()
            if name:
                bii['name'] = name

            department = profile_sel.xpath('//tr/td[@data-title="Department"]/a/text()').extract()
            if department:
                bii['department'] = department

            title = profile_sel.xpath('//tr/td[@class="ecc-contact-position"]/a/text()').extract()
            if title:
                bii['title'] = title

            bii['institution'] = 'Delta State University'

            email = profile_sel.xpath('//tr/td[@data-title="Email"]/a/text()').extract()
            if email:
                bii['email'] = email
            #
            phone = profile_sel.xpath('//tr/td[@data-title="Phone"]/a/text()').extract()
            if phone:
                bii['phone'] = phone

            url = profile_sel.xpath('//tr/td[@data-title="Name"]/a/@href').extract()
            if url:
                bii['url'] = url
            return bii


