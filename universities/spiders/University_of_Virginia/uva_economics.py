# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import uva_edu


class EconomicsSpider(scrapy.Spider):
    """
    Scrape all profiles from
    http://www.economics.virginia.edu

    """
    name = "uva_economics"
    allowed_domains = ["/economics.virginia.edu"]
    start_urls = (
        'http://economics.virginia.edu/faculty',
    )

    def parse(self, response):
        """
        Parsing faculty members profiles page from department of economics

        """
        my_sel = Selector(response)
        economics_sel = my_sel.xpath('//div[@class="view-content"]')

        for profile_sel in economics_sel:
            economics_genisys = uva_edu()

            name = profile_sel.xpath('//div[@class="views-field views-field-title"]/span/h3/a/text()').extract()
            if name:
                economics_genisys['name'] = name

            title = profile_sel.xpath('//div[@class="views-field views-field-title"]/span/em/text()').extract()
            if title:
                economics_genisys['title'] = title

            economics_genisys['department'] = 'Economics'
            economics_genisys['institution'] = 'University of Virginia'
            economics_genisys['division'] = 'Arts and Science'

            email = profile_sel.xpath('//div[@class="views-field views-field-field-email"]/a/text()').extract()
            if email:
                economics_genisys['email'] = email

            phone = profile_sel.xpath('//tr/td[@class="views-field views-field-field-email"]/span/text()').extract()
            if phone:
                economics_genisys['phone'] = phone

            url = profile_sel.xpath('//div[@class="views-field views-field-title"]/span/h3/a/@href').extract()
            if url:
                economics_genisys['url'] = url
            return economics_genisys


