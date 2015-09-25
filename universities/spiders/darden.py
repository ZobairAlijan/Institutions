# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import uva_edu


class MendozaNdEduSpider(scrapy.Spider):
    """
    Scrape all profiles from
    http://www.mendoza.nd.edu

    """
    name = "m"
    allowed_domains = ["engl.virginia.edu"]
    start_urls = (
        'http://www.engl.virginia.edu/faculty',
    )

    def parse(self, response):
        """
        Parse profiles page

        """
        sel = Selector(response)
        people_sel = sel.xpath('//div[@class="view-content"]')

        for profile_sel in people_sel:
            bii = uva_edu()

            name = profile_sel.xpath('//tr/td[@class="views-field views-field-title"]/h4/a/text()').extract()
            if name:
                bii['name'] = name

            title = profile_sel.xpath('//tr/td[@class="views-field views-field-title"]/h5/a/text()').extract()
            if title:
                bii['title'] = title

            bii['department'] = 'Creative Writing'
            bii['institution'] = 'University of virginia'
            bii['division'] = 'Arts and Sceince'

            email = profile_sel.xpath('//tr/td[4][@class="views-field views-field-field-email"]/a/text()').extract()
            if email:
                bii['email'] = email

            phone = profile_sel.xpath('//tr/td[4][@class="views-field views-field-field-email"]/span/text()').extract()
            if phone:
                bii['phone'] = phone

            url = profile_sel.xpath('//tr/td[@class="views-field views-field-title"]/h4/a/@href').extract()
            if url:
                bii['url'] = url

            discipline = profile_sel.xpath('//tr/td[2][@class="views-field views-field-title"]/h5/a/text()').extract()
            if discipline:
                bii['discipline'] = discipline
            return bii


