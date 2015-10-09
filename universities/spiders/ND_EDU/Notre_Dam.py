# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import University


class NotreDameUniversitySpider(scrapy.Spider):
    """
    Scrape all profiles from these faculties:

    School of Architecture
    Arts and Letters
    The Humanities
    The Social Sciences
    College of Engineering
    Keough School of Global Affairs


    http://nd.edu

    """
    name = "nd"
    allowed_domains = ["nd.edu"]
    start_urls = (
        'http://architecture.nd.edu/people/',
        'http://al.nd.edu/about/the-faculty/'
    )

    def start_requests(self):
        """
        Generate start requests to faculties
        """

        yield Request(self.start_urls[0], callback=self.parse_architecture)

    def parse_architecture(self, response):
        """
        Parse School of Architecture

        """
        sel = Selector(response)

        profiles_sel = sel.xpath('//h3[contains(text(), "Administration")]/following-sibling::ul/li') + \
            sel.xpath('//h3[contains(text(), "Staff")]/following-sibling::ul/li')

        for p in profiles_sel:
            link = p.xpath('p/a/@href').extract()
            if link:
                yield Request('http://architecture.nd.edu%s' %link[0], callback=self.parse_arc_profile)
            else:
                item = University()
                item['name'] = p.xpath('descendant-or-self::h3/text()').extract()[0]
                item['title'] = p.xpath('descendant-or-self::p[2]/text()').extract()[0]
                item['institution'] = 'School of Architecture'
                yield item

    def parse_arc_profile(self, response):
        sel = Selector(response)

        item = University()
        item['name'] = sel.xpath('//h1/text()').extract()[0]
        item['title'] = sel.xpath('//h2/text()').extract()[0]
        item['institution'] = 'School of Architecture'
        phone = sel.xpath('//b[contains(text(), "Phone:")]/following-sibling::text()').extract()
        if phone:
            item['phone'] = phone[0].strip()

        email = sel.xpath('//b[contains(text(), "Email:")]/following-sibling::a/text()').extract()
        if email:
            item['email'] = email[0].strip()
        yield item

    def parse_arts_and_letters(self, response):
        """
        Parse profiles page

        """
        sel = Selector(response)
        people_sel = sel.xpath('//ul[@id="people-list"]/li')

        for profile_sel in people_sel:
            item = University()

            name = profile_sel.xpath('div/div/b[@class="person-fullname"]/a/text()').extract()
            if name:
                item['name'] = name[0].strip()

            title = profile_sel.xpath('div/div/span[@class="person-title"]/text()').extract()
            if title:
                item['title'] = title[0].strip()

            department = profile_sel.xpath('div/div/span[@class="person-department"]/a/text()').extract()
            if department:
                item['department'] = department[0]

            item['institution'] = 'Mendoza College of Business'

            email = profile_sel.xpath('div/div/div[@class="person-email"]/a/text()').extract()
            if email:
                item['email'] = email[0].strip()

            phone = profile_sel.xpath('div/div/div[@class="person-phone"]/text()').extract()
            if phone:
                item['phone'] = phone[0].strip()

            yield item


