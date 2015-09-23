# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import uva_edu


class AmericanStudySpider(scrapy.Spider):
    """
    Scrape all profiles from
    http://www.mendoza.nd.edu

    """
    name = "american"
    allowed_domains = ["americanstudies.virginia.edu",]
    start_urls = (
        "http://americanstudies.virginia.edu/faculty",
    )

    def parse(self, response):
        """
        Parse profiles page

        """
        sel = Selector(response)

        people_sel = sel.xpath('//div[@class="content clearfix"]/div')

        for profile_sel in people_sel:
            item = uva_edu()

            name = profile_sel.xpath('//div[@class="view-content"]//td/h3/a/text()').extract()
            if name:
                item['name'] = name

            title = profile_sel.xpath('//td[@class="views-field views-field-title"]/h5/text()').extract()
            if title:
                item['title'] = title

            url = profile_sel.xpath('//div[@class="view-content"]//td/h3/a/@href').extract()
            if url:
                item['url'] = url

            item['division'] = 'School of Arts and Sceince'
            item['institution'] = 'University of Virginia'
            item['department'] = 'American Study'

            phone = profile_sel.xpath('//div[@class="view-content"]//td/span/text()').extract()
            if phone:
                item['phone'] = phone
            email = profile_sel.xpath('//div[@class="view-content"]//td/a/text()').extract()
            if email:
                item['email'] = email
            return item



