# -*- coding: utf-8 -*-

import scrapy
import re
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import University


class BentleySpider(scrapy.Spider):
    """
    Scrape all profiles from
    http://www.bentley.edu

    """
    name = "bentley"
    allowed_domains = ["bentley.edu"]
    start_urls = (
        'http://www.bentley.edu/about/directory',
    )

    def parse(self, response):
        """
        Parse profiles page

        """
        sel = Selector(response)
        people_sel = sel.xpath('//div[@class="view-content"]/div')

        for profile_sel in people_sel:
            bii = University()

            name = profile_sel.xpath('//span/h2/text()').extract()
            if name:
                bii['name'] = ' '.join([x.strip() for x in name[0].split('\r\n') if x.strip()])

            title = profile_sel.xpath('//h3/span/text()').extract()
            if title:
                bii['title'] = ' '.join([x.strip() for x in name[0].split('\r\n') if x.strip()])

            department = profile_sel.xpath('//div[@class="views-field views-field-text-3"]/span/text()').extract()
            if department:
                bii['department'] = department[0].strip()

            bii['institution'] = 'Bentley University'
            return bii

def normalize_whitespace(str):
    import re
    str = str.strip()
    str = re.sub(r'\s+', ' ', str)
    return str
