# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import University


class my_computerScienceSpider(scrapy.Spider):
    """
    Scrape all faculty members profiles from
    http://www.cs.vt.edu

    """
    name = "cs"
    allowed_domains = ["cs.vt.edu"]
    start_urls = (
        'http://www.cs.vt.edu/people',
    )

    def parse(self, response):
        """
        Getting links from department of my_computer Science

        """
        sel = Selector(response)

        links = sel.xpath('//table[@class="people"]//tr/td/h3/a/@href').extract()
        for link in links:
            p_link = 'http://www.cs.vt.edu%s' % link
            request = Request(p_link,
                              callback=self.parse_my_computer_science_page)
            yield request

    def parse_my_computer_science_page(self, response):
        """
        Parse faculty members profile from department of my_computer Science

        """
        my_computer = University()

        sel = Selector(response)

        name = sel.xpath('//div[@id="main-content"]//tr/td[2]/h3/text()').extract()
        if name:
            my_computer['name'] = ' '.join([x.strip() for x in name[0].split('\r\n') if x.strip()])

        title = sel.xpath('//div[@id="main-content"]//tr/td[2]/p/b/text()').extract()
        if title:
            my_computer['title'] = ' '.join([x.strip() for x in title[0].split('\r\n') if x.strip()])

        my_computer['institution'] = 'Virginia Tech'
        my_computer['department'] = 'my_computer Science'
        my_computer['division'] = 'College of Engineering'

        email = sel.xpath('//th[contains(text(), "Email")]/following-sibling::td/a/text()').extract()
        if email:
            my_computer['email'] = email[0].strip()

        phone = sel.xpath('//th[contains(text(), "Phone")]/following-sibling::td/text()').extract()
        if phone:
            my_computer['phone'] = phone[0].strip()
        url = sel.xpath('//table[@class="people"]//tr/td[2]/h3/a/@href').extract()
        if url:
            my_computer['url'] = url
        return my_computer
