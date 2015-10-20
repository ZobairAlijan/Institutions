# -*- coding: utf-8 -*-

import scrapy
from scrapy.selector import Selector

from universities.items import University


class BellinEduSpider(scrapy.Spider):
    """
    Scrape all profiles from
    http://www.bellincollege.edu

    """
    name = "bellin"
    allowed_domains = ["bellincollege.edu"]
    start_urls = (
        'http://www.bellincollege.edu/bellin-college-faculty.php',
    )

    def parse(self, response):
        """
        Parse profiles page
        The faculty members also have previous educations listed on faculty directory
        if needed, it can be added later

        """
        sel = Selector(response)
        college_sel = sel.xpath('//div[@id="global-contentcontainer"]')

        for bellin_sel in college_sel:
            item = University()

            name = bellin_sel.xpath('//td[@align="left"]/strong/text()').extract()
            if name:
                item['name'] = ' '.join([x.strip() for x in name])

            title = bellin_sel.xpath('//td[@align="left"]/text()[3]').extract()
            if title:
                item['title'] = ' '.join([x.strip() for x in title])

            item['institution'] = 'Bellin college'

            email = bellin_sel.xpath('//td[@align="left"]/a/text()').extract()
            if email:
                item['email'] = ' '.join([x.strip() for x in email])

            phone = bellin_sel.xpath('//td[@align="left"]/text()[5]').extract()
            if phone:
                item['phone'] = ' '.join([x.strip() for x in phone])
            yield item
