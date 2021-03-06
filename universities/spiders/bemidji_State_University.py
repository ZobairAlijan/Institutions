# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import University


class BemidjiStateEduSpider(scrapy.Spider):
    """
    Scrape all profiles from
    http://www.bemidji.edu

    """
    name = "bemidji"
    allowed_domains = ["bemidjistate.edu"]
    start_urls = (
        'http://www.bemidjistate.edu/directory/facstaff/',
    )

    def parse(self, response):
        sel = Selector(response)
        people_sel = sel.xpath('//table[@class="result-listing"]')

        for profile_sel in people_sel:
            bii = University()

            name = profile_sel.xpath('//td[@class="name"]/a/text()').extract()
            if name:
                bii['name'] = ' '.join([x.strip() for x in name])

            title = profile_sel.xpath('//td[@class="title"]/text()').extract()
            if title:
                bii['title'] = ' '.join([x.strip() for x in title])

            department = profile_sel.xpath('//td[@class="dept_code"]/text()').extract()
            if department:
                bii['department'] = ' '.join([x.strip() for x in department])

            bii['institution'] = 'Bemidji State University'

            email = sel.xpath('//div[@class="small-12 columns"]/p[1]').extract()
            if email:
                bii['email'] = ' '.join([x.strip() for x in email])

            phone = profile_sel.xpath('//td[@class="phone"]/text()').extract()
            if phone:
                bii['phone'] = ' '.join([x.strip() for x in phone])
            return bii


