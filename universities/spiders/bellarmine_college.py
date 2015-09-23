# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import University


class BemidjiStateEduSpider(scrapy.Spider):
    """
    Scrape all profiles from
    http://www.mendoza.nd.edu

    """
    name = "bellarmine"
    allowed_domains = ["bellarmine.edu"]
    start_urls = (
        'https://catalog.bellarmine.edu/2014-2015/university-personnel#Faculty',
    )

    def parse(self, response):
        """
        Parse profiles page

        """
        sel = Selector(response)
        people_sel = sel.xpath('//div[@class="node"]')

        for profile_sel in people_sel:
            bii = University()

            name = profile_sel.xpath('//div/p[0]/text()').extract()
            if name:
                bii['name'] = ' '.join([x.strip() for x in name])

            title = profile_sel.xpath('//td[@class="title"]/text()').extract()
            if title:
                bii['title'] = ' '.join([x.strip() for x in title])

            department = profile_sel.xpath('//div/h3/text()').extract()
            if department:
                bii['department'] = ' '.join([x.strip() for x in department])

            division = profile_sel.xpath('//div/h2/text()').extract()
            if division:
                bii['division'] = ' '.join([x.strip() for x in department])

            bii['institution'] = 'Bellarmine University'

            return bii


