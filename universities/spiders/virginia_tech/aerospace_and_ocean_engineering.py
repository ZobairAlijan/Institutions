# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import University


class AeroSpaceSpider(scrapy.Spider):
    """
    Scrape all faculty members profiles from
    http://www.aoe.vt.edu website

    """
    name = "aerospace"
    allowed_domains = ["aoe.vt.edu"]
    start_urls = (
        'http://www.aoe.vt.edu/people/faculty/index.html',
        'http://www.aoe.vt.edu/people/faculty-research/index.html',
        'http://www.aoe.vt.edu/people/faculty/adjunct/index.html',
        'http://www.aoe.vt.edu/people/faculty/affiliates/index.html',
        'http://www.aoe.vt.edu/people/faculty/emeritus/index.html',
    )

    def parse(self, response):
        """
        Getting links from department of Aerospace and Ocean Engineering

        """
        sel = Selector(response)

        links = sel.xpath('//div[@id="vt_body_col"]/div/ul/li/div/div[1]/ul/li[2]/a/@href').extract()
        for link in links:
            p_link = 'http://www.aoe.vt.edu%s' %link
            request = Request(p_link,
                              callback=self.parse_aerospace_and_ocean_engineering)
            assert isinstance(request, object)
            yield request

    def parse_aerospace_and_ocean_engineering(self, response):
        """
        Parse faculty members profile from department of Aerospace and Ocean Engineering

        """

        item = University()

        sel = Selector(response)

        name = sel.xpath('//div[@id="vt_bio_top"]/h2/text()').extract()
        if name:
            item['name'] = ' '.join([x.strip() for x in name[0].split('\r\n') if x.strip()])

        title = sel.xpath('//div[@id="vt_bio_top"]/h3/text()').extract()
        if title:
            item['title'] = ' '.join([x.strip() for x in title[0].split('\r\n') if x.strip()])

        item['institution'] = 'Aerospace and Ocean Engineering'
        item['institution'] = 'Virginia Tech'
        item['division'] = 'College of Engineering'

        email = sel.xpath('//li[@class="vt_cl_email"]/a/text()').extract()
        if email:
            item['email'] = email[0].strip()

        phone = sel.xpath('//li[@class="vt_cl_phone"]/text()').extract()
        if phone:
            item['phone'] = phone[0].strip()
        url = sel.xpath('//div[@id="vt_bio_top"]/h2/@href').extract()
        if url:
            item['url'] = phone[0].strip()

        return item



