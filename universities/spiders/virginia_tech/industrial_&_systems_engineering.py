# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import University


class BabsonEduSpider(scrapy.Spider):
    """
    Scrape all profiles from
    http://www.babson.edu

    """
    name = "ise"
    allowed_domains = ["ise.vt.edu"]
    start_urls = (
        'http://www.ise.vt.edu/People/Faculty/Faculty_index.html',
    )

    def parse(self, response):
        """
        Get links to profiles

        """
        sel = Selector(response)

        links = sel.xpath('//div[@class="col-lg-6"]//li/a/@href').extract()
        for link in links:
            p_link = 'http://www.ise.vt.edu%s' %link
            request = Request(p_link,
                              callback=self.parse_profile_page)
            yield request

    def parse_profile_page(self, response):
        """
        Parse profile page

        """

        bii = University()

        sel = Selector(response)

        name = sel.xpath('//div[@id="vt_bio_top"]/h2/text()').extract()
        if name:
            bii['name'] = ' '.join([x.strip() for x in name[0].split('\r\n') if x.strip()])

        title = sel.xpath('//div[@id="vt_bio_top"]/h3/text()').extract()
        if title:
            bii['title'] = ' '.join([x.strip() for x in title[0].split('\r\n') if x.strip()])

        bii['department'] = 'Industrial and Systems Engineering'
        bii['division'] = 'College of Engineering'
        bii['institution'] = 'Virginia Tech'

        email = sel.xpath('//li[@class="vt_cl_email"]/a/text()').extract()
        if email:
            bii['email'] = email[0].strip()

        phone = sel.xpath('//li[@class="vt_cl_phone"]/h3/text()').extract()
        if phone:
            bii['phone'] = phone[0].strip()

        url = sel.xpath('//div[@class="col-lg-6"]//li/a/@href').extract()
        if url:
            bii['url'] = url[0].strip()
        return bii


