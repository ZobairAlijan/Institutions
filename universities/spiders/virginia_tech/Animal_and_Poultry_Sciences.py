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
        Getting links from department of Animal Poultry Sciences

        """
        sel = Selector(response)

        links = sel.xpath('//div[@class="col-lg-9"]//tr/td[1]/a/@href').extract()
        for link in links:
            p_link = 'http://www.apsc.vt.edu%s' %link
            request = Request(p_link,
                              callback=self.parse_animal_poultry_science)
            assert isinstance(request, object)
            print request
            yield request

    def parse_animal_poultry_science(self, response):
        """
        Parse faculty members profile from department of Animal and Poultry Sciences

        """
        animal_sel = Selector(response)

        animal_item = University()

        name = animal_sel.xpath('//div[@id="vt_bio_top"]/h2/text()').extract()
        if name:
            animal_item['name'] = ' '.join([x.strip() for x in name[0].split('\r\n') if x.strip()])

        title = animal_sel.xpath('//div[@id="vt_bio_top"]/h3/text()').extract()
        if title:
            animal_item['title'] = ' '.join([x.strip() for x in title[0].split('\r\n') if x.strip()])

        animal_item['department'] = 'Animal and Poultry'
        animal_item['division'] = 'College of Agriculture and Life Sciences'
        animal_item['institution'] = 'Virginia Tech'

        email = animal_sel.xpath('//li[@class="vt_cl_email"]/text()').extract()
        if email:
            animal_item['email'] = ' '.join([x.strip() for x in email[0].split('\r\n') if x.strip()])

        phone = animal_sel.xpath('//li[@class="vt_cl_phone"]/text()').extract()
        if phone:
            animal_item['phone'] = ' '.join([x.strip() for x in phone[0].split('\r\n') if x.strip()])

        return animal_item