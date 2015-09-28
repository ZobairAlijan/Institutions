# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import University


class ChristenDomSpider(scrapy.Spider):
    """
    Scrape all profiles from
    http://www.christendom.edu

    """
    name = "chris"
    allowed_domains = ["christendom.edu"]
    start_urls = (
        'http://www.christendom.edu/academics/graduate-faculty.php',
    )

    def parse(self, response):
        """
        Parse profiles page

        """
        sel = Selector(response)
        people_sel = sel.xpath('//div[@id="content"]//tr')

        for profile_sel in people_sel:
            chdom = University()

            name = profile_sel.xpath('//td/strong/text()').extract()
            if name:
                chdom['name'] = ' '.join([name.strip() for name in name])

            title = profile_sel.xpath('//td/em/text()').extract()
            if title:
                chdom['title'] = ' '.join([title.strip() for title in title])

            chdom['institution'] = 'Christendom College'

            return chdom


