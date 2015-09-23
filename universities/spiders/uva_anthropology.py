# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import uva_edu


class anthopologySpider(scrapy.Spider):
    """
    Scrape all profiles from
    http://www.anthropology.virginia.edu

    """
    name = "anthopology"
    allowed_domains = ["anthropology.virginia.edu"]
    start_urls = (
        "http://anthropology.virginia.edu/faculty",
    )

    def parse(self, response):
        """
        Parse profiles page

        """
        sel = Selector(response)

        people_sel = sel.xpath('//div[@class="clearfix"]//div')

        for profile_sel in people_sel:
            item = uva_edu()

            name = profile_sel.xpath('//td[@class="views-field views-field-title"]/h4/a/text()').extract()
            if name:
                item['name'] = name

            title = profile_sel.xpath('//td[@class="views-field views-field-title"]/h5/text()').extract()
            if title:
                item['title'] = title

            url = profile_sel.xpath('//td[@class="views-field views-field-title"]/h4/a/@href').extract()
            if url:
                item['url'] = url

            item['division'] = 'School of Arts and Sceince'
            item['institution'] = 'University of Virginia'
            item['department'] = 'Anthopology'

            phone = profile_sel.xpath('//td[@class="views-field views-field-field-email"]/span/text()').extract()
            if phone:
                item['phone'] = phone
            email = profile_sel.xpath('//td[@class="views-field views-field-field-email"]/a/@href').extract()
            if email:
                item['email'] = email
            return item



