# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import University

class BellevueEduSpider(scrapy.Spider):
    name = "bellevue"
    allowed_domains = ["bellevue.edu"]
    start_urls = (
        'http://www.bellevue.edu/about/leadership/faculty-profiles',
    )

    def parse(self, response):
        """
        Getting links to profiles

        """
        sel = Selector(response)

        links = sel.xpath('//div[@class="col-750 shadow"]/section/ul/li/a/@href').extract()
        for link in links:
            p_link = 'http://www.bellevue.edu%s' %link
            request = Request(p_link, callback=self.parse_profile_page)
            yield request

    def parse_profile_page(self, response):
        """
        Parse profile page

        """
        item = University()
        sel = Selector(response)

        name = sel.xpath('//div[@class="col-750 shadow"]/section/h1/text()').extract()
        if name:
            item['name'] = ' '.join([x.strip() for x in name[0].split('\r\n') if x.strip()])

        title = sel.xpath('//ul[@class="noBullets"]/li[1]/text()').extract()
        if title:
            item['title'] = ' '.join([x.strip() for x in title[0].split('\r\n') if x.strip()])

        department = sel.xpath('//ul[@class="noBullets"]/li[2]/text()').extract()
        if department:
            item['department'] = department

        item['institution'] = 'Bellevue University'

        email = sel.xpath('//ul[@class="noBullets"]/li[3]/a/text()').extract()
        if email:
            item ['email'] = email[0].strip()

        phone = sel.xpath('//ul[@class="noBullets"]/li[4]/text()').extract()
        if phone:
            item['phone'] = phone[0].strip()

        url = sel.xpath('//div[@class="col-750 shadow"]/section/ul/li/a/@href').extract()
        if url:
            item['url'] = phone[0].strip()
        return item
