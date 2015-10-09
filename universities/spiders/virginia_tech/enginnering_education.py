# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import University


class EngEducationSpider(scrapy.Spider):
    """
    Scrape all faculty members profiles from
    http://www.enge.vt.edu

    """
    name = "engineering_education"
    allowed_domains = ["enge.vt.edu"]
    start_urls = (
        'http://www.enge.vt.edu/people/teaching-research-faculty.html',
    )

    def parse(self, response):
        """
        Getting links from department of Engineering Education

        """
        params = Selector(response)

        educational_links = params.xpath('//div[@class="contact-category"]//p/a/@href').extract()
        for eng_education_link in educational_links:
            engineering_link = 'http://www.enge.vt.edu%s' % eng_education_link
            request = Request(engineering_link,
                              callback=self.parse_engineering_education)
            print request
            yield request

    def parse_engineering_education(self, response):
        """
        Parsing profile page

        """

        eng_education = University()

        params = Selector(response)

        name = params.xpath('//span[@class="contact-name"]/text()').extract()
        if name:
            eng_education['name'] = ' '.join([x.strip() for x in name[0].split('\r\n') if x.strip()])

        title = params.xpath('//p[@class="contact-position"]/text()').extract()
        if title:
            eng_education['title'] = ' '.join([x.strip() for x in title[0].split('\r\n') if x.strip()])

        eng_education['institution'] = 'Virginia Tech'
        eng_education['department'] = 'Engineering Education'
        eng_education['division'] = 'College of Engineering'

        email = params.xpath('//span[@class="contact-emailto"]/a/text()').extract()
        if email:
            eng_education['email'] = email[0].strip()

        phone = params.xpath('//span[@class="contact-telephone"]/text()').extract()
        if phone:
            eng_education['phone'] = phone[0].strip()

        url = params.xpath('//div[@class="contact-category"]//p/a/@href').extract()
        if url:
            eng_education['url'] = url

        print eng_education
        return eng_education
