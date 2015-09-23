# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
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
        The faculty members also have previous educations listed on facult directory
        if needed, it can be added later

        """
        sel = Selector(response)
        people_sel = sel.xpath('//div[@id="global-contentcontainer"]')

        for bellin_sel in people_sel:
            item = University()

            name = bellin_sel.xpath('//td[@align="left"]/strong/text()').extract()
            if name:
                item['name'] = name

            title = bellin_sel.xpath('//td[@align="left"]/text()[3]').extract()
            if title:
                item['title'] = title

            item['institution'] = 'Bellin college'

            email = bellin_sel.xpath('//td[contains(text(), "Email")]/following-sibling::a/text()').extract()
            if email:
                item['email'] = email

            phone = bellin_sel.xpath('//td[@align="left"]/text()[5]').extract()
            if phone:
                item['phone'] = phone
            return item
