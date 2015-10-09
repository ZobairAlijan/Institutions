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
    name = "test"
    allowed_domains = ["mlsoc.vt.edu"]
    start_urls = (
        'http://www.mlsoc.vt.edu/directory/faculty-staff',
    )

    def parse(self, response):
        """
        Get links to profiles

        """
        sel = Selector(response)

        links = sel.xpath('//div[@class="view-content"]//div/h3/a/@href').extract()
        for link in links:
            p_link = 'http://www.mlsoc.vt.edu%s' %link
            request = Request(p_link,
                              callback=self.parse_profile_page)
            yield request

    def parse_profile_page(self, response):
        """
        Parse profile page

        """

        bii = University()

        sel = Selector(response)

        name = sel.xpath('//div[@class="field-item even"]/text()').extract()
        if name:
            bii['name'] = name

        # title = sel.xpath('//div[@class="responsive-profile__bio responsive-profile__main-col"]/h2/text()').extract()
        # if title:
        #     bii['title'] = ' '.join([x.strip() for x in title[0].split('\r\n') if x.strip()])
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


