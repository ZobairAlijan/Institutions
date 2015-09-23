# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import University

class BabsonSpider(scrapy.Spider):
    name = "chm"
    allowed_domains = ["classics.virginia.edu"]
    start_urls = (
        'http://www.virginia.edu/cognitivescience/faculty.htm',
    )

    def parse(self, response):
        """
        Getting links to profiles

        """
        sel = Selector(response)

        links = sel.xpath('//td[@style="vertical-align: top; text-align: center; font-family: Calibri;"]')
        for link in links:
            p_link = 'http://www.virginia.edu%s' %link
            request = Request(p_link, callback=self.parse_profile_page)
            yield request

    def parse_profile_page(self, response):
        """
        Parse profile page

        """

        item = University()

        sel = Selector(response)

        name = sel.xpath('//b[@style="color: rgb(53, 85, 154);"]/text()').extract()
        if name:
            item['name'] = name

        # title = sel.xpath('//div[@class="responsive-profile__bio responsive-profile__main-col"]/h2/text()').extract()
        # if title:
        #     item['title'] = ' '.join([x.strip() for x in title[0].split('\r\n') if x.strip()])
        #
        # department = sel.xpath('//span[contains(text(), "Academic Division")]/following-sibling::div/a/text()').extract()
        # if department:
        #     item['department'] = department[0]
        #
        # item['institution'] = 'Babson College'
        #
        # email = sel.xpath('//span[contains(text(), "Contact")]/following-sibling::div/a/text()').extract()
        # if email:
        #     item ['email'] = email[0].strip()
        #
        # phone = sel.xpath('//span[contains(text(), "Contact")]/following-sibling::div/text()').extract()
        # if phone:
        #     item['phone'] = phone[0].strip()
        #
        # url = sel.xpath('//ul[@id="facultyList"]/li/a/@href').extract()
        # if url:
        #     item['url'] = url[0].strip()
        return item
