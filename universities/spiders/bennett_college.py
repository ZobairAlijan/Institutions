# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import University


class Bennett_CollegeSpider(scrapy.Spider):
    """
    Scrape all profiles from
    http://www.bennett.edu

    """
    name = "bennett"
    allowed_domains = ["bennett.edu"]
    start_urls = (
        'http://www.bennett.edu/empldir',
    )

    def parse(self, response):
        """
        Parse profiles page

        """
        sel = Selector(response)
        people_sel = sel.xpath('//table[@class="grid"]')

        for profile_sel in people_sel:
            bennett = University()

            name = profile_sel.xpath('//tr[@class="alt"]/td[1]/text()').extract()
            if name:
                bennett['name'] = name

            title = profile_sel.xpath('//tr[@class="alt"]/td[2]/text()').extract()
            if title:
                bennett['title'] = title

            department = profile_sel.xpath('//tr[@class="alt"]/td[5]/text()').extract()
            if department:
                bennett['department'] = department

            bennett['institution'] = 'Bennete College'

            email = profile_sel.xpath('//tr[@class="alt"]/td/a/text()').extract()
            if email:
                bennett['email'] = email

            phone = profile_sel.xpath('//tr[@class="alt"]/td[3]/text()').extract()
            if phone:
                bennett['phone'] = phone
            return bennett


