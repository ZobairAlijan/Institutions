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
    name = "ece"
    allowed_domains = ["enge.vt.edu"]
    start_urls = (
        'http://www.enge.vt.edu/people/teaching-research-faculty.html',
    )

    def parse(self, response):
        """
        Get links to profiles

        """
        
        sel = Selector(response)

        links = sel.xpath('//form[@id="adminForm"]/div/p/a/@href').extract()
        for link in links:
            p_link = 'http://www.enge.vt.edu%s' %link
            request = Request(p_link,
                              callback=self.parse_max_the_best)
            yield request

    def parse_max_the_best(self, response):
        """
        Parse profile page

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

        url = sel.xpath('//div[@class="adminForm"]/div[1]/p/a/@href').extract()
        if url:
            item['url'] = url

        return item


