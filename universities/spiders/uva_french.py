# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import uva_edu


class FrenchSpider(scrapy.Spider):
    """
    Scrape all profiles from
    http://www.french.virginia.edu

    """
    name = "french"
    allowed_domains = ["french.virginia.edu"]
    start_urls = (
        'http://french.virginia.edu/faculty',
        'http://french.virginia.edu/faculty?page=1'
    )

    def parse(self, response):
        """
        Parsing faculty members profiles page from department of French Studies

        """
        my_sel = Selector(response)
        french_sel = my_sel.xpath('//div[@class="content"]//div')

        for profile_sel in french_sel:
            french_genisys = uva_edu()

            name = profile_sel.xpath('//tr/td[@class="views-field views-field-title"]/h4/a/text()').extract()
            if name:
                french_genisys['name'] = name

            title = profile_sel.xpath('//tr/td[@class="views-field views-field-field-position-1"]/text()').extract()
            if title:
                french_genisys['title'] = ' '.join([title.strip() for title in title])

            french_genisys['department'] = 'FRENCH'
            french_genisys['institution'] = 'University of Virginia'
            french_genisys['division'] = 'Arts and Science'

            email = profile_sel.xpath('//tr/td[@class="views-field views-field-title"]/a/text()').extract()
            if email:
                french_genisys['email'] = email

            phone = profile_sel.xpath('//tr/td[@class="views-field views-field-title"]/span/text()').extract()
            if phone:
                french_genisys['phone'] = phone

            url = profile_sel.xpath('//tr/td[@class="views-field views-field-title"]/h4/a/@href').extract()
            if url:
                french_genisys['url'] = url
            return french_genisys


