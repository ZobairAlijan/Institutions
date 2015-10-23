# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import University


class ConstructionSpider(scrapy.Spider):
    """
    Scrape all profiles from
    http://www.mlsoc.vt.edu

    """
    name = "vt_construction"
    allowed_domains = ["mlsoc.vt.edu"]
    start_urls = (
        'http://www.mlsoc.vt.edu/directory/faculty-staff',
    )

    def parse(self, response):
        """
        Parse links and faculty members profile from Virginia Tech Construction department

        """
        sel = Selector(response)
        people_sel = sel.xpath('//div[@class="view-content"]//div')

        for profile_sel in people_sel:
            item = University()

            name = profile_sel.xpath('//h3[@class="field-content"]/a/text()').extract()
            if name:
                item['name'] = name

            title = profile_sel.xpath\
                ('//div[@class="inside panels-flexible-region-inside panels-flexible-region-profile-center-inside '
                 'panels-flexible-region-inside-first panels-flexible-region-inside-last"]/em/text()').extract()
            if title:
                item['title'] = title

            department = profile_sel.xpath('//div[@class="field-items"]/div/text()').extract()
            if department:
                item['department'] = department

            item['institution'] = 'Virginia Tech'

            email = profile_sel.xpath('//div[@class="inside panels-flexible-region-inside '
                                      'panels-flexible-region-profile-center-inside '
                                      'panels-flexible-region-inside-first panels-flexible-region-inside-last"]'
                                      '/div[1]/text()').extract()
            if email:
                item['email'] = email

            phone = profile_sel.xpath('//div[@class="inside panels-flexible-region-inside '
                                      'panels-flexible-region-profile-center-inside '
                                      'panels-flexible-region-inside-first panels-flexible-region-inside-last"]'
                                      '/div[2]/text()').extract()
            if phone:
                item['phone'] = phone
            return item
