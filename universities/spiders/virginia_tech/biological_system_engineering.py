# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import University


class BiologicalSpider(scrapy.Spider):
    """
    Scrape all profiles from
    http://www.bse.vt.edu

    """
    name = "biological"
    allowed_domains = ["bse.vt.edu"]
    start_urls = (
        'http://www.bse.vt.edu/people/tenure-track/index.html',
        'http://www.bse.vt.edu/people/other-faculty/index.html',
    )

    def parse(self, response):
        """
        Get links from department of biological System Engineering

        """
        sel = Selector(response)

        links =  sel.xpath('//div[@class="col-lg-9"]//tr/td/a[1]/@href').extract()
        for link in links:
            p_link = 'http://www.bse.vt.edu%s' % link
            request = Request(p_link,
                              callback=self.parse_biological_page)
            yield request

    def parse_biological_page(self, response):
        """
        Parse faculty members profile from department of biological System Engineering

        """

        item = University()
        sel = Selector(response)

        name = sel.xpath('//div[@id="vt_bio_top"]/h2/text()').extract()
        if name:
            item['name'] = name

        title = sel.xpath('//div[@id="vt_bio_top"]/h3/text()').extract()
        if title:
            item['title'] = title

        department = sel.xpath('//li[@class="vt_cl_address"]/text()').extract()
        if department:
            item['department'] = department

        item['institution'] = 'Virginia Tech'
        item['division'] = 'College of Agriculture and Life Sciences'

        email = sel.xpath('//li[@class="vt_cl_email"]/a/text()').extract()
        if email:
            item['title'] = email

        phone = sel.xpath('//li[@class="vt_cl_phone"]/text()').extract() + \
            sel.xpath('//li[2][@class="vt_cl_phone"]/text()').extract()

        if phone:
            item['title'] = phone
        return item
