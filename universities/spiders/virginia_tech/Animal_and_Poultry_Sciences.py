# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import University


class AnimalSpider(scrapy.Spider):
    """
    Scrape all faculty members profiles from
    http://www.apsc.vt.edu

    """
    name = "animal"
    allowed_domains = ["apsc.vt.edu"]
    start_urls = (
        'http://www.apsc.vt.edu/people/faculty/faculty.html',
    )

    def parse(self, response):
        """
        Parse profiles page from department of Animal and Poultry Science

        """
        sel = Selector(response)
        people_sel = sel.xpath('//div[@class="col-lg-9"]')

        for agriculture_sel in people_sel:
            animal_item = University()

            name = agriculture_sel.xpath('//tr/td[1]/a[1]/text()').extract()
            if name:
                animal_item['name'] = name

            title = agriculture_sel.xpath('//tr/td[5]/text()').extract()
            if title:
                animal_item['title'] = title
            animal_item['department'] = 'Animal and Poultry'
            animal_item['division'] = 'College of Agriculture and Life Sciences'
            animal_item['institution'] = 'Virginia Tech'

            email = agriculture_sel.xpath('//tr/td[2]/a/text()').extract()
            if email:
                animal_item['email'] = email

            phone = agriculture_sel.xpath('//tr/td[3]/text()').extract()
            if phone:
                animal_item['phone'] = phone

            yield animal_item
