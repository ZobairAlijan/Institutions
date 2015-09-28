# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import University

class BabsonSpider(scrapy.Spider):
    name = "think"
    allowed_domains = ["babson.edu"]
    start_urls = (
        'http://www.babson.edu/Academics/faculty/profiles/Pages/default.aspx',
    )

    def parse(self, response):
        """
        Getting links to profiles

        """
        sel = Selector(response)

        links = sel.xpath('//ul[@id="facultyList"]/li/a/@href').extract()
        for link in links:
            p_link = 'http://www.babson.edu %s' % link
            request = Request(p_link, callback=self.parse_profile_page)
            yield request

    def parse_profile_page(self, response):
        """
        Parse profile page

        """
        item = University()

        sel = Selector(response)

        name = sel.xpath('//div[@class="responsive-profile__bio responsive-profile__main-col"]/h1/text()').extract()
        if name:
            item['name'] = ' '.join([x.strip() for x in name[0].split('\r\n') if x.strip()])

        title = sel.xpath('//div[@class="responsive-profile__bio responsive-profile__main-col"]/h2/text()').extract()
        if title:
            item['title'] = ' '.join([x.strip() for x in title[0].split('\r\n') if x.strip()])

        department = sel.xpath('//span[contains(text(), "Academic Division")]/following-sibling::div/a/text()').extract()
        if department:
            item['department'] = department[0]

        item['institution'] = 'Babson College'

        email = sel.xpath('//span[contains(text(), "Contact")]/following-sibling::div/a/text()').extract()
        if email:
            item ['email'] = email[0].strip()

        phone = sel.xpath('//span[contains(text(), "Contact")]/following-sibling::div/text()').extract()
        if phone:
            item['phone'] = phone[0].strip()

        url = sel.xpath('//ul[@id="facultyList"]/li/a/@href').extract()
        if url:
            item['url'] = url[0].strip()
        return item
