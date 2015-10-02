# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import University


class SchoolOfCommerceSpider(scrapy.Spider):
    """
    Scrape all profiles from
    http://www.sociology.virginia.edu

    """
    name = "mcintire"
    allowed_domains = ["sociology.virginia.edu"]
    start_urls = (
        'https://www.commerce.virginia.edu/faculty',
    )
    other_urls = [
        'https://www.commerce.virginia.edu/faculty',
    ]

    def start_requests(self):
        requests = list(super(SchoolOfCommerceSpider, self).start_requests())
        requests += [scrapy.Request(x, self.parse_other) for x in self.other_urls]
        return requests

    def parse(self, response):
        """
        Parsing faculty members profiles page from department of Commerce

        """
        my_sel = Selector(response)
        global_sel = my_sel.xpath('//div[@class="view-content"]')

        for socio_sel in global_sel:
            item = University()

            name = socio_sel.xpath('//div/h3/a/text()').extract()
            if name:
                item['name'] = ' '.join([name.strip() for name in name])

            title = socio_sel.xpath('//div[@class="Information-Technology"]/p/text()').extract() + \
                socio_sel.xpath('//div[@class="Finance"]/p/text()').extract() + \
                socio_sel.xpath('//div[@class="Accounting"]/p/text()').extract() + \
                socio_sel.xpath('//div[@class="Marketing"]/p/text()').extract() + \
                socio_sel.xpath('//div[@class="Management"]/p/text()').extract()

            if title:
                item['title'] = ' '.join([title.strip() for title in title])

            item['department'] = 'Commerce'
            item['institution'] = 'University of Virginia'
            item['division'] = 'McIntire School of Commerce'

            email = socio_sel.xpath('//div/p/a/text()').extract()
            if email:
                item['email'] = email

            phone = socio_sel.xpath('//div[@class="views-field views-field-field-phone-number"]/p/text()').extract()
            if phone:
                item['phone'] = ' '.join([phone.strip() for phone in phone])

            url = socio_sel.xpath('//div/h3/a/@href').extract()
            if url:
                item['url'] = ' '.join([url.strip() for url in url])
            return item

    def parse_other(self, response):
        pass
