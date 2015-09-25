# -*- coding: utf-8 -*-

import scrapy
from scrapy.selector import Selector

from universities.items import University


class BioethicsSpider(scrapy.Spider):
    """
    Scrape all profiles from
    http://www.bioethics.virginia.edu

    """
    name = "bioetich"
    allowed_domains = ["bioethics.virginia.edu"]
    start_urls = (
        'http://bioethics.virginia.edu/people',
    )

    def parse(self, response):
        """
        Parse profiles page

        """
        sel = Selector(response)
        people_sel = sel.xpath('//table[@class="views-table cols-0"]')

        for profile_sel in people_sel:
            bioetich = University()

            name = profile_sel.xpath('//tr/td/h1/a/text()').extract()
            if name:
                bioetich['name'] = name

            title = profile_sel.xpath('//tr/td/h5/text()').extract()
            if title:
                bioetich['title'] = title

            url = profile_sel.xpath('//tr/td/h1/a/@href').extract()
            if url:
                bioetich['url'] = url

            phone = profile_sel.xpath('//tr/td[2]/a/text()').extract()
            if phone:
                bioetich['phone'] = phone

            email = profile_sel.xpath('//tr/td[2]/text()').extract()
            if email:
                bioetich['email'] = email

            bioetich['department'] = "Bioethics"
            bioetich['institution'] = "University of Virginia"
            bioetich['division'] = "Arts and Science"

            return bioetich


