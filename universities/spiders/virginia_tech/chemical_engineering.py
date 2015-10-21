# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import University


class ChemicalEngineeringSpider(scrapy.Spider):
    """
    Scrape all faculty members profiles from
    http://www.bse.vt.edu website

    """
    name = "chemeng"
    allowed_domains = ["che.vt.edu"]
    start_urls = (
        'http://www.che.vt.edu/people_faculty.php',
    )

    def parse(self, response):
        """
        Getting links from department of Chemical Engineering

        """
        sel = Selector(response)

        links = sel.xpath('//ul[@class="facultylist"]/li/h2/a/@href').extract()
        for link in links:
            p_link = 'http://www.che.vt.edu%s' % link
            request = Request(p_link, callback=self.max_parse)
            yield request

    def max_parse(self, response):
        """
        Parse profile page from Virginia Tech

        """

        item = University()
        sel = Selector(response)

        name = sel.xpath('//li[@class="facultymember indentmore"]/h2/text()').extract()
        if name:
            item['name'] = name

        title = sel.xpath('//span[@class="title"]/text()').extract()
        if title:
            item['title'] = ' '.join([x.strip() for x in title[0].split('\r\n') if x.strip()])

        item['institution'] = 'Virginia Tech'
        item['department'] = 'Chemical Engineering'
        item['division'] = 'College of Engineering'

        email = sel.xpath('//li[contains(text(), "Email:")]/following-sibling::a/text()').extract()
        if email:
            item['email'] = email[0].strip()

        phone = sel.xpath('//h4[contains(text(), "Contact:")]/following-sibling::ul/li/text()').extract()
        if phone:
            item['phone'] = phone[0].strip()
        url = sel.xpath('//li[@class="facultymember indentmore"]/h2/@href').extract()
        if url:
            item['url'] = url
        return item
