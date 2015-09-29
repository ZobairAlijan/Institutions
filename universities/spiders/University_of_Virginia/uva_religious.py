# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import University


class MathematicsSpider(scrapy.Spider):
    """
    Scrape all profiles from
    http://www.religiousstudies.virginia.edu

    """
    name = "psychology"
    allowed_domains = ["http://cacsprd.web.virginia.edu/"]
    start_urls = (
        'http://religiousstudies.virginia.edu/faculty',
    )

    def parse(self, response):
        """
        Parsing faculty members profiles page from department of Religious Studies

        """
        my_sel = Selector(response)
        global_sel = my_sel.xpath('//div[@class="view-content"]')

        for rel_sel in global_sel:
            the_religion = University()

            name = rel_sel.xpath('//tr/td[@class="views-field views-field-title"]/h3/a/text()').extract()
            if name:
                the_religion['name'] = ' '.join([name.strip() for name in name])

            title = rel_sel.xpath('//tr/td[@class="views-field views-field-title"]/h3/a/text()').extract()
            if title:
                the_religion['title'] = ' '.join([title.strip() for title in title])

            the_religion['department'] = 'Religious Studies'
            the_religion['institution'] = 'University of Virginia'
            the_religion['division'] = 'Arts and Science'

            email = rel_sel.xpath('//tr/td[@class="views-field views-field-field-email"]/a/text()').extract()
            if email:
                the_religion['email'] = email

            phone = rel_sel.xpath('//tr/td[@class="views-field views-field-field-email"]/text()').extract()
            if phone:
                the_religion['phone'] = ' '.join([phone.strip() for phone in phone])

            url = rel_sel.xpath('//tr/td[@class="views-field views-field-title"]/h3/a/@href').extract()
            if url:
                the_religion['url'] = url
            return the_religion
