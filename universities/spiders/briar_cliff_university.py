# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import University

class BellevueEduSpider(scrapy.Spider):
    name = "briar"
    allowed_domains = ["briarcliff.edu"]
    start_urls = (
        'http://www.briarcliff.edu/directory/',
    )

    def parse(self, response):
        """
        Getting links to profiles

        """
        sel = Selector(response)

        links = sel.xpath('//table[@class="listings data"]//tr/td/strong/a/@href').extract()
        for link in links:
            p_link = 'http://www.briarcliff.edu%s' % link
            request = Request(p_link, callback=self.parse_profile_page)
            yield request

    def parse_profile_page(self, response):
        """
        Parse profile page

        """
        item = University()
        sel = Selector(response)

        name = sel.xpath('//div[@class="column full article"]/h1/text()').extract()
        if name:
            item['name'] = ' '.join([x.strip() for x in name[0].split('\r\n') if x.strip()])

        title = sel.xpath('//div[@class="left-side"]/h3/text()').extract()
        if title:
            item['title'] = ' '.join([x.strip() for x in title[0].split('\r\n') if x.strip()])

        department = sel.xpath('//strong[contains(text(), "Department:")]/following-sibling::text()').extract()
        if department:
            item['department'] = department[0]

        item['institution'] = 'Briar Cliff College'

        email = sel.xpath('//strong[contains(text(), "Email:")]/following-sibling::a/text()').extract()
        if email:
            item ['email'] = email[0].strip()

        phone = sel.xpath('//strong[contains(text(), "Phone:")]/following-sibling::text()').extract()
        if phone:
            item['phone'] = phone[0].strip()

        url = sel.xpath('//table[@class="listings data"]//tr/td/strong/a/@href').extract()
        if url:
            item['url'] = url
        return item


"""
The Briar Cliff College also has the following information for faculty members

Education, Bio and Curriculum

"""