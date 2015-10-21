# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import University


class CulturalSpider(scrapy.Spider):
    """
    Scrape all faculty members profiles from
    http://www.alce.vt.edu

    """
    name = "alce"
    allowed_domains = ["alce.vt.edu"]
    start_urls = (
        'http://www.alce.vt.edu/people/faculty-staff/index.html',
    )

    def parse(self, response):
        """
        Getting links from department of Aerospace and Ocean Engineering

        """
        sel = Selector(response)

        links = sel.xpath('//div[@class="col-lg-9"]//tr/td[1]/a/@href').extract()
        for link in links:
            p_link = 'http://www.alce.vt.edu%s' %link
            request = Request(p_link,
                              callback=self.parse_aerospace_and_ocean_engineering)
            assert isinstance(request, object)
            print request
            yield request

    def parse_aerospace_and_ocean_engineering(self, response):
        """
        Parse profiles page from department of Agriculture, Leadership, and Community education
        :param response:
        :return:
        """
        item = University()

        agriculture_sel = Selector(response)

        name = agriculture_sel.xpath('//div[@id="vt_bio_top"]/h2/text()').extract()
        if name:
            item['name'] = ' '.join([x.strip() for x in name[0].split('\r\n') if x.strip()])

        title = agriculture_sel.xpath('//div[@id="vt_bio_top"]/h3/text()').extract()
        if title:
            item['title'] = ' '.join([x.strip() for x in title[0].split('\r\n') if x.strip()])

        item['department'] = 'Agriculture, Leadership, and Community education'
        item['division'] = 'College of Agriculture and Life Sciences'
        item['institution'] = 'Virginia Tech'

        email = agriculture_sel.xpath('//li[@class="vt_cl_email"]/a/text()').extract()
        if email:
            item['email'] = ' '.join([x.strip() for x in email[0].split('\r\n') if x.strip()])

        phone = agriculture_sel.xpath('//li[@class="vt_cl_phone"]/text()').extract()
        if phone:
            item['phone'] = ' '.join([x.strip() for x in phone[0].split('\r\n') if x.strip()])
        return item
