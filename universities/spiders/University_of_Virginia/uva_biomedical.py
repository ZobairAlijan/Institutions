# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import University


class BridgeSpider(scrapy.Spider):
    """
    Scrape all profiles from
    http://www.babson.edu

    """
    name = "bme"
    allowed_domains = ["bme.virginia.edu"]
    start_urls = (
        'http://bme.virginia.edu/people/index.html',
    )

    def parse(self, response):
        """
        Get links to profiles

        """
        sel = Selector(response)

        links = sel.xpath('//td[@width="700"]//tr/td/a/@href').extract()
        for link in links:
            p_link = 'http://www.virginia.edu%s' %link
            request = Request(p_link, callback=self.parse_profile_page)
            yield request


    def parse_profile_page(self, response):
        """
        Parse profile page

        """

        bii = University()

        sel = Selector(response)

        name = sel.xpath('//tr/td[@valign="top"]/span/text()').extract()
        if name:
            bii['name'] = ' '.join([x.strip() for x in name[0].split('\r\n') if x.strip()])

        # title = sel.xpath('//section[@class="user-markup content fullwidth no-overlap"]/h2/text()').extract()
        # if title:
        #     bii['title'] = ' '.join([x.strip() for x in title[0].split('\r\n') if x.strip()])
        #
        # department = sel.xpath('//section[@class="user-markup content fullwidth no-overlap"]/h3/a/text()').extract()
        # if department:
        #     bii['department'] = department[0]
        #
        # bii['institution'] = 'Bridge Water College'
        #
        # email = sel.xpath('//section[strong(text(), "Email")]/following-sibling::text()').extract()
        # if email:
        #     bii['email'] = email[0].strip()
        #
        # phone = sel.xpath('//section[strong(text(), "Phone")]/following-sibling::text()').extract()
        # if phone:
        #     bii['phone'] = phone[0].strip()

        return bii


