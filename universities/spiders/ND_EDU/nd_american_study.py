# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import University


class AmericanSignSpider(scrapy.Spider):
    """
    Scrape all profiles from
    http://www.nursing.virginia.edu

    """
    name = "nursing"
    allowed_domains = ["americanstudies.nd.edu"]
    start_urls = (
        'http://americanstudies.nd.edu/faculty-and-staff/',
    )

    other_urls = [
        'http://www.nd.edu',
    ]

    def start_requests(self):
        requests = list(super(AmericanSignSpider, self).start_requests())
        requests += [scrapy.Request(x, self.parse_other) for x in self.other_urls]
        return requests

    def parse(self, response):
        """
        Parsing faculty members profiles page from School of nursing

        """
        my_sel = Selector(response)
        global_sel = my_sel.xpath('//div[@id="divDirectoryMain"]')

        for socio_sel in global_sel:
            item = University()

            name = socio_sel.xpath('//p[@class="mName"]/a/text()').extract()
            if name:
                item['name'] = ' '.join([name.strip() for name in name])

            title = socio_sel.xpath('//div[@class="mTitle"]/p/text()').extract()
            if title:
                item['title'] = ' '.join([title.strip() for title in title])

            department = socio_sel.xpath('//div[@class="mDept"]/p/span/text()').extract()
            if department:
                item['department'] = ' '.join([department.strip() for department in department])

            item['institution'] = 'University of Virginia'
            item['division'] = 'School of Nursing'

            email = socio_sel.xpath('//div[@class="mContact"]/p/a/text()').extract()
            if email:
                item['email'] = email

            phone = socio_sel.xpath('//div[@class="mContact"]/p/text()').extract()
            if phone:
                item['phone'] = ' '.join([phone.strip() for phone in phone])

            url = socio_sel.xpath('//p[@class="mName"]/a/@href').extract()
            if url:
                item['url'] = ' '.join([url.strip() for url in url])
            return item

    def parse_other(self, response):
        pass
