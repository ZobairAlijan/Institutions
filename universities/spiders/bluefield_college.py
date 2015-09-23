# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import University

class BabsonSpider(scrapy.Spider):
    name = "bluefield"
    allowed_domains = ["bluefield.edu"]
    start_urls = (
        'http://www.bluefield.edu/employee-directory/',
    )

    def parse(self, response):
        """
        Getting links to profiles

        """
        sel = Selector(response)

        links = sel.xpath('//table[@class="staff-list"]/tr/td/a/@href').extract()
        for link in links:
            p_link = 'http://www.bluefield.edu%s' %link
            request = Request(p_link, callback=self.parse_profile_page)
            yield request

    def parse_profile_page(self, response):
        """
        Parse profile page

        """

        item = University()

        sel = Selector(response)

        name = sel.xpath('//div[@class="m-right"]/div/h2/text()').extract()
        if name:
            item['name'] = ' '.join([x.strip() for x in name[0].split('\r\n') if x.strip()])

        title = sel.xpath('//div[@class="m-right"]/div/h3/text()').extract()
        if title:
            item['title'] = ' '.join([x.strip() for x in title[0].split('\r\n') if x.strip()])
        #
        department = sel.xpath('//div[@class="m-left"]/div/p/text()').extract()
        if department:
            item['department'] = department
        #
        item['institution'] = 'BlueField College'
        #
        email = sel.xpath('//div[@class="m-right"]/div/div/span/a/text()').extract()
        if email:
            item ['email'] = email[0].strip()

        phone = sel.xpath('//div[@class="m-right"]/div/div/span/text()').extract()
        if phone:
            item['phone'] = phone[0].strip()
        return item
