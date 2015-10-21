# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import University


class BiochemistrySpider(scrapy.Spider):
    """
    Scrape all profiles from
    http://www.biochem.vt.edu

    """
    name = "biochem"
    allowed_domains = ["biochem.vt.edu"]
    start_urls = (
        'http://www.biochem.vt.edu/people/faculty/index.html',
    )

    def parse(self, response):
        """
        Get links from department of Biochemistry

        """
        sel = Selector(response)

        links = sel.xpath('//div[@class="col-lg-9"]//tr/td/a[1]/@href').extract()
        for link in links:
            p_link = 'http://www.biochem.vt.edu%s' % link
            request = Request(p_link,
                              callback=self.parse_biochem_page)
            yield request

    def parse_biochem_page(self, response):
        """
        Parse faculty members profile from biochemistry department

        """

        item = University()
        sel = Selector(response)

        name = sel.xpath('//div[@id="vt_bio_top"]/h2/text()').extract()
        if name:
            item['name'] = ' '.join([x.strip() for x in name[0].split('\r\n') if x.strip()])

        title = sel.xpath('//div[@id="vt_bio_top"]/h3/text()').extract()
        if title:
            item['title'] = ' '.join([x.strip() for x in title[0].split('\r\n') if x.strip()])

        department = sel.xpath('//li[@class="vt_cl_address"]/text()').extract()
        if department:
            item['department'] = department[0]

        item['institution'] = 'Virginia Tech'
        item['division'] = 'College of Agriculture and Life Sciences'

        email = sel.xpath('//li[@class="vt_cl_email"]/a/text()').extract()
        if email:
            item['email'] = ' '.join([x.strip() for x in email[0].split('\r\n') if x.strip()])

        phone = sel.xpath('//li[@class="vt_cl_phone"]/text()').extract() + \
            sel.xpath('//li[2][@class="vt_cl_phone"]/text()').extract()
        if phone:
            item['phone'] = ' '.join([x.strip() for x in phone[0].split('\r\n') if x.strip()])
        return item
