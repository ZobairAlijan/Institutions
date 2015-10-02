# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import University


class SystemsSpider(scrapy.Spider):
    """
    Scrape all profiles from
    http://www.sys.virginia.edu

    """
    name = "system"
    allowed_domains = ["virginia.edu"]
    start_urls = (
        'http://web.sys.virginia.edu/people/faculty.html',
    )
    other_urls = [
        'http://web.sys.virginia.edu/people/faculty.html',
    ]

    def start_requests(self):
        requests = list(super(SystemsSpider, self).start_requests())
        requests += [scrapy.Request(x, self.parse_other) for x in self.other_urls]
        return requests

    def parse(self, response):
        """
        Parsing faculty members profiles page from department of Systems and information technology

        """
        my_sel = Selector(response)
        global_sel = my_sel.xpath('//div[@class="page-content"]')

        for system_sel in global_sel:
            item = University()

            name = system_sel.xpath('//table[@width="600"]//tr/td/a[1]/text()').extract()

            if name:
                item['name'] = ' '.join([name.strip() for name in name])

            title = system_sel.xpath('//table[@width="600"]//tr/td/text()').extract()
            if title:
                item['title'] = ' '.join([title.strip() for title in title])

            item['department'] = 'Systems and information  Engineering'
            item['institution'] = 'University of Virginia'
            item['division'] = 'School of Engineering'

            email = system_sel.xpath('//table[@width="600"]//tr/td/a/text()').extract()
            if email:
                item['email'] = email

            phone = system_sel.xpath('//table[@width="600"]//tr/td/a/text()').extract()
            if phone:
                item['phone'] = ' '.join([phone.strip() for phone in phone])

            url = system_sel.xpath('//table[@width="600"]//tr/td/a/@href').extract()
            if url:
                item['url'] = ' '.join([url.strip() for url in url])
            return item

    def parse_other(self, response):
        pass
