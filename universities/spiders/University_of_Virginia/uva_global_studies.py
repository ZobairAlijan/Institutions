# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import University


class GloablSpider(scrapy.Spider):
    """
    Scrape all profiles from
    http://globalstudies.virginia.edu

    """
    name = "global"
    allowed_domains = ["http://globalstudies.virginia.edu"]
    start_urls = (
        'http://globalstudies.virginia.edu/gds-faculty',

    )

    def parse(self, response):
        """
        Parsing faculty members profiles page from department of global studies

        """
        my_sel = Selector(response)
        global_sel = my_sel.xpath('//div[@class="view-content"]')

        for bia_sel in global_sel:
            the_global = University()

            name = bia_sel.xpath('//tr/td[@class="views-field views-field-title"]/h3/a/text()').extract()
            if name:
                the_global['name'] = name

            title = bia_sel.xpath('//tr/td[@class="views-field views-field-title"]/text()').extract()
            if title:
                the_global['title'] = ' '.join([title.strip() for title in title])

            the_global['department'] = 'gGlobal Studies'
            the_global['institution'] = 'University of Virginia'
            the_global['division'] = 'Arts and Science'

            email = bia_sel.xpath('//tr/td[@class="views-field views-field-field-email"]/a/text()').extract()
            if email:
                the_global['email'] = email

            phone = bia_sel.xpath('//tr/td[@class="views-field views-field-field-email"]/span/text()').extract()
            if phone:
                the_global['phone'] = phone

            url = bia_sel.xpath('//tr/td[@class="views-field views-field-title"]/h3/a/@href').extract()
            if url:
                the_global['url'] = url
            return the_global


