# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import University


class BiologicalSystemsSpider(scrapy.Spider):
    """
    Scrape all faculty members profiles from
    http://www.bse.vt.edu website

    """
    name = "biological"
    allowed_domains = ["bse.vt.edu"]
    start_urls = (
        'http://www.bse.vt.edu/people/tenure-track/index.html',
    )

    def parse(self, response):
        """
        Get links to profiles

        """
        sel = Selector(response)

        links = sel.xpath('//div[@id="vt_body_col"]//tr/td[2]/a[1]/@href').extract()
        for link in links:
            p_link = 'http://www.bse.vt.edu%s' %link
            request = Request(p_link, callback=self.max_parse)
            yield request

    def max_parse(self, response):
        """
        Parse profile page from Virginia Tech

        """

        item = University()

        sel = Selector(response)

        name = sel.xpath('//div[@id="vt_bio_top"]/h2/text()').extract()
        if name:
            item['name'] = ' '.join([x.strip() for x in name[0].split('\r\n') if x.strip()])

        title = sel.xpath('//div[@id="vt_bio_top"]/h3/text()').extract()
        if title:
            item['title'] = ' '.join([x.strip() for x in title[0].split('\r\n') if x.strip()])

        item['institution'] = 'Virginia Tech'
        item['department'] = 'Biological Systems Engineering'
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
