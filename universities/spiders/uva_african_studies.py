# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import uva_edu


class AfricanStudiesSpider(scrapy.Spider):
    """
    Scrape all profiles from
    http://www.mendoza.nd.edu

    """
    name = "african"
    allowed_domains = ["woodson.virginia.edu"]
    start_urls = (
        "http://www.woodson.virginia.edu/faculty",
    )

    def parse(self, response):
        """
        Parse profiles page

        """
        sel = Selector(response)

        people_sel = sel.xpath('//div[@class="view-content"]/div')

        for profile_sel in people_sel:
            bii = uva_edu()

            name = profile_sel.xpath('//div[@class="views-field views-field-title"]/span/h3/text()').extract()

            if name:
                bii['name'] = name

            # title = profile_sel.xpath('//div[@class="views-field views-field-title"]/span/text()').extract()
            # if title:
            #     bii['title'] = title
            #
            # bii['division'] = 'Arts and Science'
            # bii['institution'] = 'University of Virginia'
            # bii['department'] = 'African American and African Studies'
            #
            # email = profile_sel.xpath('//div[@class="views-field views-field-field-email"]/a/text()').extract()
            # if email:
            #     bii['email'] = email
            #
            # phone = profile_sel.xpath('//div[@class="views-field views-field-field-email"]/span/text()').extract()
            # if phone:
            #     bii['phone'] = phone
            return bii