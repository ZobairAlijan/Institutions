# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import University


class ComputerScienceSpider(scrapy.Spider):
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
        Getting links from department of Computer Science

        """
        sel = Selector(response)

        links = sel.xpath('//table[@class="people"]//tr/td/h3/a/@href').extract()
        for link in links:
            p_link = 'http://www.cs.vt.edu%s' %link
            request = Request(p_link,
                              callback=self.parse_profile_page)
            yield request

    def parse_profile_page(self, response):
        """
        Parse profile page

        """

        computer = University()

        sel = Selector(response)

        name = sel.xpath('//div[@id="main-content"]//tr/td[2]/h3/text()').extract()
        if name:
            computer['name'] = ' '.join([x.strip() for x in name[0].split('\r\n') if x.strip()])

        title = sel.xpath('//div[@id="main-content"]//tr/td[2]/p/b/text()').extract()
        if title:
            computer['title'] = ' '.join([x.strip() for x in title[0].split('\r\n') if x.strip()])

        computer['institution'] = 'Virginia Tech'
        computer['department'] = 'Computer Science'
        computer['division'] = 'College of Engineering'

        email = sel.xpath('//th[contains(text(), "Email")]/following-sibling::td/a/text()').extract()
        if email:
            computer['email'] = email[0].strip()

        phone = sel.xpath('//th[contains(text(), "Phone")]/following-sibling::td/text()').extract()
        if phone:
            computer['phone'] = phone[0].strip()
        url = sel.xpath('//table[@class="people"]//tr/td[2]/h3/a/@href').extract()
        if url:
            computer['url'] = url
        return computer
