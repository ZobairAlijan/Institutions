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
    name = "darden"
    allowed_domains = ["ece.virginia.edu"]
    start_urls = (
        'http://www.darden.virginia.edu/faculty-research/directory/',
    )

    def parse(self, response):
        """
        Get links to profiles

        """
        sel = Selector(response)

        links = sel.xpath('//p[@class="faculty-name"]/a/@href').extract()

        for link in links:
            p_link = 'http://www.virginia.edu.edu%s' %link
            request = Request(p_link, callback=self.parse_profile_page)
            yield request

    def parse_profile_page(self, response):
        """
        Parse profile page

        """

        bii = University()

        sel = Selector(response)

        name = sel.xpath('//div[@id="upper"]/h3/text()').extract()
        if name:
            bii['name'] = ' '.join([x.strip() for x in name[0].split('\r\n') if x.strip()])

        # title = sel.xpath('//div[@class="responsive-profile__bio responsive-profile__main-col"]/h2/text()').extract()
        # if title:
        #     bii['title'] = 'scrapy shell  '.join([x.strip() for x in title[0].split('\r\n') if x.strip()])
        #
        # department = sel.xpath('//span[contains(text(), "Academic Division")]/following-sibling::div/a/text()').extract()
        # if department:
        #     bii['department'] = department[0]
        #
        # bii['institution'] = 'Babson College'
        #
        # email = sel.xpath('//span[contains(text(), "Contact")]/following-sibling::div/a/text()').extract()
        # if email:
        #     bii['email'] = email[0].strip()
        #
        # phone = sel.xpath('//span[contains(text(), "Contact")]/following-sibling::div/text()').extract()
        # if phone:
        #     bii['phone'] = phone[0].strip()

        return bii
