# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import University


class MendozaNdEduSpider(scrapy.Spider):
    """
    Scrape all profiles from
    http://www.acms.nd.edu

    """
    name = "acms"
    allowed_domains = ["acms.nd.edu"]
    start_urls = (
        'http://acms.nd.edu/people/faculty/',
    )

    def parse(self, response):
        """
        Parse profiles page

        """
        sel = Selector(response)
        people_sel = sel.xpath('//div[@id="page-content"]')

        for profile_sel in people_sel:
            applied_computational = University()

            name = profile_sel.xpath('//div[@id="page-content"]/h3/strong/a/text()').extract() + \
                profile_sel.xpath('//div[@id="page-content"]/h2/a/strong/text()').extract() + \
                profile_sel.xpath('//div[@id="page-content"]/h3/a/strong/text()').extract()

            if name:
                applied_computational['name'] = ' '.join([name.strip() for name in name])

            title = profile_sel.xpath('//div[@id="page-content"]/h3/text()').extract()
            if title:
                applied_computational['title'] = ' '.join([title.strip() for title in title])

            applied_computational['department'] = 'Applied and Computational Math and Statistics'

            applied_computational['division'] = 'Mendoza College of Business'
            applied_computational['institution'] = 'Notre Dame'

            email = profile_sel.xpath('//div[@id="page-content"]/ul/li[2]/strong/a/text()').extract()
            if email:
                applied_computational['email'] = ' '.join([email.strip() for email in email])

            phone = profile_sel.xpath('//div[@id="page-content"]/ul/li[4]/text()').extract()
            if phone:
                applied_computational['phone'] = ' '.join([phone.strip() for phone in phone])

            url = profile_sel.xpath('//div[@id="page-content"]/h3/strong/a/@href').extract() + \
                profile_sel.xpath('//div[@id="page-content"]/h2/a/strong/@href').extract() + \
                profile_sel.xpath('//div[@id="page-content"]/h3/a/strong/@href').extract()

            if url:
                applied_computational['url'] = ' '.join([url.strip() for url in url])
            return applied_computational



