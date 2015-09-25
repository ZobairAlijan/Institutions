# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import uva_edu


class AmericanSignLangSpider(scrapy.Spider):
    """
    Scrape all profiles from
    http://www.asl.virginia.edu

    """
    name = "asl"
    allowed_domains = ["asl.virginia.edu"]
    start_urls = (
        "http://asl.virginia.edu/node/11",
    )

    def parse(self, response):
        """
        Parse profiles page

        """
        sel = Selector(response)

        people_sel = sel.xpath('//div[@class="field-item even"]')

        for profile_sel in people_sel:
            bii = uva_edu()

            name = profile_sel.xpath('//p/strong/text()').extract()
            if name:
                bii['name'] = name

            title = profile_sel.xpath('//p/text()').extract()
            if title:
                bii['title'] = title

            bii['division'] = 'School of Arts and Sceince'
            bii['institution'] = 'University of Virginia'
            bii['department'] = 'American Sign Language'

            email = profile_sel.xpath('///p/a/text()').extract()
            if email:
                bii['email'] = email
            phone = profile_sel.xpath('//p/text()').extract()
            if phone:
                bii['phone'] = phone
            return bii



