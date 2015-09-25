# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import uva_edu


class AstronomyEduSpider(scrapy.Spider):
    """
    Scrape all profiles from
    http://www.astro.virginia.edu

    """
    name = "astro"
    allowed_domains = ["astro.virginia.edu"]
    start_urls = (
        'http://www.astro.virginia.edu/people',
    )

    def parse(self, response):
        """
        Parse profiles page

        """
        sel = Selector(response)
        people_sel = sel.xpath('//table[@class="views-table cols-0"]')

        for profile_sel in people_sel:
            astro = uva_edu()

            name = profile_sel.xpath('//tr/td/h4/a/text()').extract()
            if name:
                astro['name'] = name

            title = profile_sel.xpath('//tr/td/em/text()').extract()
            if title:
               astro['title'] = title

            astro['department'] = 'Astronomy'
            astro['institution'] = 'University of Virginia'
            astro['division'] = 'Arts and Science'

            email = profile_sel.xpath('//tr/td[3]/a/text()').extract().strip()
            if email:
                astro['email'] = email

            phone = profile_sel.xpath('//tr/td[3]/text()').extract()
            if phone:
                astro['phone'] = phone

            url = profile_sel.xpath('//tr/td/h4/a/@href').extract()
            if url:
                astro['url'] = url
            return astro


