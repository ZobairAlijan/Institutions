# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import University


class CommerceSpider(scrapy.Spider):
    """
    Scrape all profiles from
    http://www.politics.virginia.edu

    """
    name = "commerce"
    allowed_domains = ["politics.virginia.edu"]
    start_urls = (
        'https://www.commerce.virginia.edu/faculty',
    )

    def parse(self, response):
        """
        Parsing faculty members profiles page from department of Politics

        """
        the_sel = Selector(response)
        marketing_sel = the_sel.xpath('//div[@class="view-content"]')

        for comm_sel in marketing_sel:
            the_commerce = University()

            name = comm_sel.xpath('//div/h3/a/text()').extract()
            if name:
                the_commerce['name'] = ' '.join([name.strip() for name in name])

            title = comm_sel.xpath('//div[@class="Information-Technology"]/p/text()').extract() + \
                comm_sel.xpath('//div[@class="Finance"]/p/text()').extract() + \
                comm_sel.xpath('//div[@class="Marketing"]/p/text()').extract() + \
                comm_sel.xpath('//div[@class="Management"]/p/text()').extract()
            if title:
                the_commerce['title'] = ' '.join([title.strip() for title in title])

            the_commerce['department'] = 'Commerce'
            the_commerce['institution'] = 'University of Virginia'
            the_commerce['division'] = 'McIntire school of Commerce'

            email = comm_sel.xpath('//div/p[1]/a/text()').extract()
            if email:
                the_commerce['email'] = ' '.join([email.strip() for email in email])

            phone = comm_sel.xpath('//div[@class="views-field views-field-field-phone-number"]/p/text()').extract()
            if phone:
                the_commerce['phone'] = ' '.join([phone.strip() for phone in phone])

            url = comm_sel.xpath('//div/h3/a/@href').extract()
            if url:
                the_commerce['url'] = url
            return the_commerce
