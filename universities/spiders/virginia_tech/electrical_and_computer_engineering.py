# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import University


class ElectricalEngineeringSpider(scrapy.Spider):
    """
    Scrape all profiles from
    http://www.enge.vt.edu

    """
    name = "ece"
    allowed_domains = ["enge.vt.edu"]
    start_urls = (
        'http://www.enge.vt.edu/people/teaching-research-faculty.html',
    )

    def parse(self, response):
        """
        Get links from department of  electrical and Computer Engineering

        """
        sel = Selector(response)

        links = sel.xpath('//form[@id="adminForm"]/div/p/a/@href').extract()
        for link in links:
            pc_link = 'http://www.enge.vt.edu%s' % link
            request = Request(pc_link,
                              callback=self.parse_computer_engineering)
            yield request

    def parse_computer_engineering(self, response):
        """
        Parse faculty members profile from the department of electrical and Computer Engineering

        :rtype : object
        """

        item = University()

        sel = Selector(response)

        name = sel.xpath('//div[@class="contact directory"]/h2/span[1]/text()').extract()
        if name:
            item['name'] = ' '.join([x.strip() for x in name[0].split('\r\n') if x.strip()])

        title = sel.xpath('//div[@id="my_contact_details"]/p/text()').extract()
        if title:
            item['title'] = ' '.join([x.strip() for x in title[0].split('\r\n') if x.strip()])

        item['department'] = 'Engineering Education'
        item['division'] = 'College of Engineering'
        item['institution'] = 'Virginia Tech'

        phone = sel.xpath('//span[@class="contact-telephone"]/text()').extract()
        if phone:
            item['phone'] = phone[0].strip()

        email = sel.xpath('//span[@class="contact-emailto"]/a/text()').extract()
        if email:
            item['email'] = email[0].strip()

        url = sel.xpath('//form[@id="adminForm"]/div/p/a/@href').extract()
        if url:
            item['url'] = url

        return item


