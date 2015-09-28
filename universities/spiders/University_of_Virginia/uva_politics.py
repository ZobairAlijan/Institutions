# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import University


class MathematicsSpider(scrapy.Spider):
    """
    Scrape all profiles from
    http://www.politics.virginia.edu

    """
    name = "politics"
    allowed_domains = ["politics.virginia.edu"]
    start_urls = (
        'http://politics.virginia.edu/faculty',
    )

    def parse(self, response):
        """
        Parsing faculty members profiles page from department of Politics

        """
        my_sel = Selector(response)
        global_sel = my_sel.xpath('//div[@class="view-content"]')

        for polit_sel in global_sel:
            the_global = University()

            name = polit_sel.xpath('//tr/td[@class="views-field views-field-field-position"]//h4/a/text()').extract()
            if name:
                the_global['name'] = ' '.join([name.strip() for name in name])

            title = polit_sel.xpath('//tr/td[@class="views-field views-field-field-position"]/text()').extract()
            if title:
                the_global['title'] = ' '.join([title.strip() for title in title])

            the_global['department'] = 'Politics'
            the_global['institution'] = 'University of Virginia'
            the_global['division'] = 'Arts and Science'

            email = polit_sel.xpath('//tr/td[@class="views-field views-field-field-phone"]/a/text()').extract()
            if email:
                the_global['email'] = ' '.join([email.strip() for email in email])

            phone = polit_sel.xpath('//tr/td[@class="views-field views-field-field-phone"]/span/text()').extract()
            if phone:
                the_global['phone'] = ' '.join([phone.strip() for phone in phone])

            url = polit_sel.xpath('//tr/td[@class="views-field views-field-field-position"]//h4/a/@href').extract()
            if url:
                the_global['url'] = url
            return the_global
