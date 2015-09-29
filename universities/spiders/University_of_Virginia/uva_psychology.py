# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import University


class MathematicsSpider(scrapy.Spider):
    """
    Scrape all profiles from
    http://www.cacsprd.web.virginia.edu

    """
    name = "psychology"
    allowed_domains = ["http://cacsprd.web.virginia.edu/"]
    start_urls = (
        'http://cacsprd.web.virginia.edu/Psych/Faculty/Profiles',
    )

    def parse(self, response):
        """
        Parsing faculty members profiles page from department of Psychology

        """
        my_sel = Selector(response)
        global_sel = my_sel.xpath('//div[@class="grid_10"]')

        for psycho_sel in global_sel:
            the_psychology = University()

            name = psycho_sel.xpath('//div[@class="grid_5 alpha profile-list"]/h4/a/text()').extract()
            if name:
                the_psychology['name'] = ' '.join([name.strip() for name in name])

            title = psycho_sel.xpath('//div[@class="grid_5 alpha profile-list"]/p/text()').extract()
            if title:
                the_psychology['title'] = ' '.join([title.strip() for title in title])

            the_psychology['department'] = 'Psychology'
            the_psychology['institution'] = 'University of Virginia'
            the_psychology['division'] = 'Arts and Science'

            email = psycho_sel.xpath('//div[@class="grid_5 alpha profile-list"]/a/text()').extract()
            if email:
                the_psychology['email'] = email

            phone = psycho_sel.xpath('//div[@class="grid_2"]/p/text()').extract()
            if phone:
                the_psychology['phone'] = ' '.join([phone.strip() for phone in phone])

            url = psycho_sel.xpath('//div[@class="grid_5 alpha profile-list"]/h4/a/@href').extract()
            if url:
                the_psychology['url'] = url
            return the_psychology
