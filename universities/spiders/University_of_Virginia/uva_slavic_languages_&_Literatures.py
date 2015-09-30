# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import University


class ReligionSpider(scrapy.Spider):
    """
    Scrape all profiles from
    http://www.religiousstudies.virginia.edu

    """
    name = "slavic"
    allowed_domains = ["http://cacsprd.web.virginia.edu/"]
    start_urls = (
        'http://artsandsciences.virginia.edu/slavic/people/index.html',
    )

    def parse(self, response):
        """
        Parsing faculty members profiles page from department of Slavic Languages & Literature

        """
        my_sel = Selector(response)
        global_sel = my_sel.xpath('//div[@class="yui-b"]')

        for psycho_sel in global_sel:
            the_religion = University()

            name = psycho_sel.xpath('//dl[@class="directory"]/dt/a/text()').extract()
            if name:
                the_religion['name'] = ' '.join([name.strip() for name in name])

            title = psycho_sel.xpath('//dl/dd/p[@class="title"]/text()').extract()
            if title:
                the_religion['title'] = title

            the_religion['department'] = 'Slavic Languages and Literature'
            the_religion['institution'] = 'University of Virginia'
            the_religion['division'] = 'Arts and Science'

            email = psycho_sel.xpath('//dl[@class="directory"]/dd/p[2]/a/text()').extract()
            if email:
                the_religion['email'] = email

            phone = psycho_sel.xpath('//dl[@class="directory"]/dd/p[2]/text()').extract()
            if phone:
                the_religion['phone'] = phone

            url = psycho_sel.xpath('//dl[@class="directory"]/dt/a/@href').extract()
            if url:
                the_religion['url'] = ' '.join([url.strip() for url in url])
            return the_religion
