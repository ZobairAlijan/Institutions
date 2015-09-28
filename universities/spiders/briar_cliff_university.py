# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import University


class BriarCliffSpider(scrapy.Spider):
    """
    Scrape all profiles from
    http://www.briarcliff.edu

    """
    name = "briar"
    allowed_domains = ["briarcliff.edu"]
    start_urls = (
        'http://www.briarcliff.edu/directory/',
    )

    def parse(self, response):
        """
        Parse faculty page

        """
        sel = Selector(response)
        link_sel = sel.xpath('//table[@class="listings data"]/tr')

        for cliff_sel in link_sel:
            eid_mu = University()

            name = cliff_sel.xpath('//tr/td/strong/a/text()').extract()
            if name:
                eid_mu['name'] = name

            title = cliff_sel.xpath('//tr/td/span/text()').extract()
            if title:
                eid_mu['title'] = title

            department = cliff_sel.xpath('//tr/td/span[@class="department"]/text()').extract()

            if department:
                eid_mu['department'] = department

            eid_mu['institution'] = 'Briar Cliff University'

            email = cliff_sel.xpath('//p[contains(text(), "Email:")]/following-sibling::a/text()').extract()
            if email:
                eid_mu['email'] = email

            phone = cliff_sel .xpath('//tr/td[2]/strong/text()').extract()

            if phone:
                eid_mu['phone'] = phone

            url = cliff_sel .xpath('//tr/td/strong/a/@href').extract()

            if url:
                eid_mu['url'] = url
            return eid_mu
