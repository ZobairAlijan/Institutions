# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import University


class GloablSpider(scrapy.Spider):
    """
    Scrape all profiles from
    http://www.math.virginia.edu

    """
    name = "math"
    allowed_domains = ["math.virginia.edu"]
    start_urls = (
        'http://www.math.virginia.edu/directory',
        'http://www.math.virginia.edu/directory?page=1',
        'http://www.math.virginia.edu/directory?page=2',
        'http://www.math.virginia.edu/directory?page=3',
        'http://www.math.virginia.edu/directory?page=4',
        'http://www.math.virginia.edu/directory?page=5',
        'http://www.math.virginia.edu/directory?page=6',
        'http://www.math.virginia.edu/directory?page=7',
        'http://www.math.virginia.edu/directory?page=8',
        'http://www.math.virginia.edu/directory?page=9',
        'http://www.math.virginia.edu/directory?page=10',
        'http://www.math.virginia.edu/directory?page=11',

    )

    def parse(self, response):
        """
        Parsing faculty members profiles page from department of Mathematics

        """
        my_sel = Selector(response)
        global_sel = my_sel.xpath('//div[@id="page-content"]//div')

        for bia_sel in global_sel:
            the_global = University()

            name = bia_sel.xpath('//tr/td[@class="views-field views-field-title"]/h4/a/text()').extract()
            if name:
                the_global['name'] = ' '.join([name.strip() for name in name])

            title = bia_sel.xpath('//tr/td[@class="views-field views-field-title"]/h5/text()').extract()
            if title:
                the_global['title'] = ' '.join([title.strip() for title in title])

            the_global['department'] = 'Mathematics'
            the_global['institution'] = 'University of Virginia'
            the_global['division'] = 'Arts and Science'

            email = bia_sel.xpath('//tr/td[@class="views-field views-field-field-email"]/a/text()').extract()
            if email:
                the_global['email'] = ' '.join([email.strip() for email in email])

            phone = bia_sel.xpath('//tr/td[@class="views-field views-field-field-email"]/span/text()').extract()
            if phone:
                the_global['phone'] = ' '.join([phone.strip() for phone in phone])

            url = bia_sel.xpath('//tr/td[@class="views-field views-field-title"]/h4/a/@href').extract()
            if url:
                the_global['url'] = url
            return the_global
