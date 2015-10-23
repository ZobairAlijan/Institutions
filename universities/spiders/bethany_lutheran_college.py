# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import University


class LutheranSpider(scrapy.Spider):
    """
    Scrape all profiles from
    http://www.blc.edu.edu

    """
    name = "lutheran"
    allowed_domains = ["bismarckstate.edu"]
    start_urls = (
        'https://www.blc.edu/directory/faculty',

    )

    def parse(self, response):
        """
        Parse faculty members profile

        """
        sel = Selector(response)
        link_sel = sel.xpath('//table[@class="layoutTable"]//tr')

        for bism_sel in link_sel:
            item = University()

            name = bism_sel.xpath('//td[@class="views-field views-field-title"]/a/text()').extract()
            if name:
                item['name'] = name

            title = bism_sel.xpath('//td[@class="views-field views-field-field-job-title"]/text()').extract()
            if title:
                item['title'] = ' '.join([title.strip() for title in title])

            item['institution'] = 'Bethany Lutheran College'

            email = sel.xpath('//td[@class="views-field views-field-nid"]/a/@href').extract()
            if email:
                item['email'] = email
            phone = sel.xpath('//td[@class="views-field views-field-nid"]/text()').extract()
            if phone:
                item['phone'] = phone
            yield item

