# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import University


class BellarmineEduSpider(scrapy.Spider):
    """
    Scrape all sfaculty profiles from
    http://www.bellarmine.edu

    """
    name = "bellarmine"
    allowed_domains = ["bellarmine.edu"]
    start_urls = (
        'https://catalog.bellarmine.edu/2014-2015/university-personnel#Faculty',
    )

    def parse(self, response):
        """
        All faculty information is in one plains text i.e name, title, department, division, phone, therefore
        it is not pssoble to group them seperatly.

        """
        sel = Selector(response)
        people_sel = sel.xpath('//div[@class="node"]/div')

        for profile_sel in people_sel:
            bii = University()

            name = profile_sel.xpath('//div[@class="content"]/p/text()').extract()
            if name:
                bii['name'] = name

            department = profile_sel.xpath('//div[@class="content"]/h3/text()').extract()
            if department:
                bii['department'] = department

            bii ['institution'] = 'Bellarmine University'

            return bii
