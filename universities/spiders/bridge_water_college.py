# -*- coding: utf-8 -*-

import scrapy
import re
from string import digits
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import University


class BridgeSpider(scrapy.Spider):
    """
    Scrape all profiles from
    http://www.babson.edu

    """
    name = "water"
    allowed_domains = ["bridgewater.edu"]
    start_urls = (
        'https://www.bridgewater.edu/about-bc/faculty-students',
    )

    def parse(self, response):
        """
        Get links to profiles

        """
        sel = Selector(response)

        links = sel.xpath('//ul[@class="people-list nobullets"]//div/a/@href').extract()
        for link in links:
            p_link = 'http://www.bridgewater.edu%s' %link
            request = Request(p_link, callback=self.parse_profile_page)
            yield request

    def parse_profile_page(self, response):
        """
        Parse profile page

        """

        water_sel = University()

        sel = Selector(response)

        name = sel.xpath('//section[@class="user-markup content fullwidth no-overlap"]/h1/text()').extract()
        if name:
            water_sel['name'] = ' '.join([name for name in name if name])

        title = sel.xpath('//section[@class="user-markup content fullwidth no-overlap"]/h2/text()').extract()
        if title:
            water_sel['title'] = ' '.join([title for title in title if title])

        department = sel.xpath('//section[@class="user-markup content fullwidth no-overlap"]/h3/a/text()').extract()
        if department:
            water_sel['department'] = department

        water_sel['institution'] = 'Bridge Water College'

        email = sel.xpath('//strong[contains(text(), "Email")]/following-sibling::a/text()').extract() + \
            sel.xpath('//section[@class="user-markup content fullwidth no-overlap"]/p/a/text()').extract()
        if email:
            water_sel['email'] = email

        phone = sel.xpath('//strong[contains(text(), "Phone")]/following-sibling::text()').extract() + \
            sel.xpath('//section[@class="user-markup content fullwidth no-overlap"]/p/text()').extract()

        if phone:
            water_sel['phone'] = ''.join(phone for phone in phone if phone.isdigit())

        return water_sel
