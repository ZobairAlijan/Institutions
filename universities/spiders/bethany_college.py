# -*- coding: utf-8 -*-

import scrapy
from scrapy.selector import Selector

from universities.items import BethanyEdu


class BethanyEduSpider(scrapy.Spider):
    """
    Scrape all faculty members from Bethany college
    http://www.bethanylb.edu

    """
    name = "bethany"
    allowed_domains = ["bethanylb.edu"]
    start_urls = (
        'http://www.bethanylb.edu/directory/',
        'http://www.bethanylb.edu/directory/pg/2/',
        'http://www.bethanylb.edu/directory/pg/3/',
        'http://www.bethanylb.edu/directory/pg/4/',
        'http://www.bethanylb.edu/directory/pg/5/',
        'http://www.bethanylb.edu/directory/pg/6/',
        'http://www.bethanylb.edu/directory/pg/7/',
        'http://www.bethanylb.edu/directory/pg/8/',
        'http://www.bethanylb.edu/directory/pg/9/',
        'http://www.bethanylb.edu/directory/pg/10/',
        'http://www.bethanylb.edu/directory/pg/11/',

    )

    def parse(self, response):
        """
        Parse profiles page

        """
        sel = Selector(response)
        bethany_people_sel = sel.xpath('//div[@id="cn-list-body"]')

        for profile_sel in bethany_people_sel:
            bethany = BethanyEdu()

            first_name = profile_sel.xpath('//span[@class="given-name"]/text()').extract()
            if first_name:
                bethany ['first_name'] = first_name

            last_name = profile_sel.xpath('//span[@class="family-name"]/text()').extract()
            if last_name:
                bethany['last_name'] = last_name

            title = profile_sel.xpath('//span[@class="title notranslate"]/text()').extract()
            if title:
                bethany['title'] = title

            department = profile_sel.xpath('//span[@class="street-address notranslate"]/text()').extract()
            if department:
                bethany['department'] = department

            bethany['institution'] = 'Bethany College'

            phone = profile_sel.xpath('//span[@class="phone-number-block"]/span/a//text()').extract()
            if phone:
                bethany['phone'] = phone

            email = profile_sel.xpath('//span[@class="email-address-block"]/span/span/a/text()').extract()
            if email:
                bethany['email'] = email

            url = profile_sel.xpath('//div[@class="cn-right"]/div/h3/a/@href').extract()
            if url:
                bethany['url'] = url
            return bethany


