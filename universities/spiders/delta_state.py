# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import University


class DeltaEduSpider(scrapy.Spider):
    """
    Scrape all profiles from
    http://www.deltastate.edu

    """
    name = "delta"
    allowed_domains = ["deltastate.edu"]
    start_urls = (
        'http://www.deltastate.edu/contacts/',
        'http://www.deltastate.edu/contacts/page/2/',
        'http://www.deltastate.edu/contacts/page/3/',
        'http://www.deltastate.edu/contacts/page/4/',
        'http://www.deltastate.edu/contacts/page/5/',
        'http://www.deltastate.edu/contacts/page/6/',
        'http://www.deltastate.edu/contacts/page/7/',
        'http://www.deltastate.edu/contacts/page/8/',
        'http://www.deltastate.edu/contacts/page/9/',
        'http://www.deltastate.edu/contacts/page/10/',
        'http://www.deltastate.edu/contacts/page/11/',

    )

    def parse(self, response):
        """
        Parse profiles page

        """
        sel = Selector(response)
        people_sel = sel.xpath('//table[@class="ecc-contact-table responsive-table"]')

        for delta_sel in people_sel:
            item = University()

            name = delta_sel.xpath('//tr/td[@data-title="Name"]/a/text()').extract()
            if name:
                item['name'] = ' '.join([name.strip() for name in name])

            department = delta_sel.xpath('//tr/td[@data-title="Department"]/a/text()').extract()
            if department:
                item['department'] = department

            title = delta_sel.xpath('//tr/td[@class="ecc-contact-position"]/a/text()').extract()
            if title:
                item['title'] = ' '.join([title.strip() for title in title])

            item['institution'] = 'Delta State University'

            email = delta_sel.xpath('//tr/td[@data-title="Email"]/a/text()').extract()
            if email:
                item['email'] = email

            phone = delta_sel.xpath('//tr/td[@data-title="Phone"]/a/text()').extract()
            if phone:
                item['phone'] = phone

            url = delta_sel.xpath('//tr/td[@data-title="Name"]/a/@href').extract()
            if url:
                item['url'] = url
            yield item


