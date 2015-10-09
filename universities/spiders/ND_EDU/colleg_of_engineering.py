# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import BabsonEduItem


class BabsonEduSpider(scrapy.Spider):
    """
    Scrape all profiles from
    http://www.babson.edu

    """
    name = "b"
    allowed_domains = ["nd.edu"]
    start_urls = (
        'http://ame.nd.edu/people/faculty',
    )

    def parse(self, response):
        """
        Get links to profiles

        """
        sel = Selector(response)

        links = sel.xpath('//div[@id="parent-fieldname-text"]//tr/td[2]/p/strong/a/@href').extract()
        for link in links:
            p_link = 'http://www.nd.edu%s' %link
            request = Request(p_link,
                callback=self.parse_profile_page)
            yield request

    def parse_profile_page(self, response):
        """
        Parse profile page

        """

        item = BabsonEduItem()

        sel = Selector(response)

        name = sel.xpath('//div[@id="content-core"]/h1/text()').extract()
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
            item['email'] = email[0].strip()

        phone = sel.xpath('//span[contains(text(), "Contact")]/following-sibling::div/text()').extract()
        if phone:
            item['phone'] = phone[0].strip()

        return item


