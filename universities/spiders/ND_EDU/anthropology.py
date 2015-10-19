# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import University


class MendozaNdEduSpider(scrapy.Spider):
    """
    Scrape all profiles from
    http://www.anthropology.nd.edu

    """
    name = "anthropology"
    allowed_domains = ["mendoza.nd.edu"]
    start_urls = (
        'http://anthropology.nd.edu/faculty-and-staff/#regular-faculty',
    )

    def parse(self, response):
        """
        Parse faculty profiles from Notre Dame University

        """
        sel = Selector(response)
        people_sel = sel.xpath('//div[@role="main"]/ul')

        for profile_sel in people_sel:
            item = University()

            name = profile_sel.xpath('//div[@class="faculty-about"]/h4/a/text()').extract()
            if name:
                item['name'] = ' '.join([name.strip() for name in name])

            title = profile_sel.xpath('//div[@class="faculty-about"]/h5/text()').extract()
            if title:
                item['title'] = ' '.join([title.strip() for title in title])

            item['department'] = 'Anthropology'
            item['division'] = 'Social Science'
            item['institution'] = 'Notre Dame'

            email = profile_sel.xpath('//div[@class="faculty-about"]/p[2]/a/text()').extract()
            if email:
                item['email'] = ' '.join([email.strip() for email in email])

            phone = profile_sel.xpath('//div[@class="faculty-about"]/p[2]/a/text()').extract()
            if phone:
                item['phone'] = ''.join(phone for phone in phone if phone.isdigit())

            yield item

"""
The department of Anthropology has the following information as well:

faculty educational background and research interests
"""



