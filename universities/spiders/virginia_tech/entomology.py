# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import University


class EntomologSpider(scrapy.Spider):
    """
    Scrape all profiles from
    http://www.ento.vt.edu

    """
    name = "entomology"
    allowed_domains = ["ento.vt.edu"]
    start_urls = (
        'http://www.ento.vt.edu/people/tenure/index.html',
    )

    def parse(self, response):
        """
        Get links from entomology department

        """
        sel = Selector(response)

        links =  sel.xpath('//div[@class="col-lg-9"]//tr/td[2]/a[1]/@href').extract()
        for link in links:
            p_link = 'http://www.ento.vt.edu%s' %link
            request = Request(p_link, callback=self.parse_entomology_page)
            yield request

    def parse_entomology_page(self, response):
        """
        Parse profile page

        """
        item = University()
        sel = Selector(response)

        name = sel.xpath('//div[@id="vt_bio_top"]/h2/text()').extract()
        if name:
            item['name'] = name

        title = sel.xpath('//div[@id="vt_bio_top"]/h3/text()').extract()
        if title:
            item['title'] = title

        department = sel.xpath('//li[@class="vt_cl_address"]/text()').extract()
        if department:
            item['department'] = ' '.join([department.strip() for department in department])

        item['institution'] = 'Virginia Tech'
        item['division'] = 'Agriculture and life science'

        email = sel.xpath('//li[@class="vt_cl_email"]/a/text()').extract()
        if email:
            item['email'] = email

        phone = sel.xpath('//li[@class="vt_cl_phone"]/text()').extract()
        if phone:
            item['phone'] = ' '.join([phone.strip() for phone in phone])

        url = sel.xpath('//div[@class="col-lg-9"]/p/a[1]/@href').extract()
        if url:
            item['url'] = url
        return item
