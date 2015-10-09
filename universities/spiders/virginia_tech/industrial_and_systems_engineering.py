# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import University


class IndustrialSysEngineeringSpider(scrapy.Spider):
    """
    Scrape all faculty members profiles from
    http://www.ise.vt.edu

    """
    name = "industrial_system"
    allowed_domains = ["ise.vt.edu"]
    start_urls = (
        'http://www.ise.vt.edu/People/Faculty/Faculty_index.html',
    )

    def parse(self, response):
        """
        Getting links from department of Industrial Systems Engineering

        """
        params = Selector(response)

        educational_links = params.xpath('//div[@class="col-lg-6"]//ul/li/a/@href').extract()
        for industrial_systems_link in educational_links:
            engineering_link = 'http://www.ise.vt.edu%s' % industrial_systems_link
            request = Request(engineering_link,
                              callback=self.parse_system_engineering)
            print request
            yield request

    def parse_system_engineering(self, response):
        """
        Parsing profile page

        """

        industrial_system = University()

        params = Selector(response)

        name = params.xpath('//h2[@class="vt_bioTitle"]/text()').extract()
        if name:
            industrial_system['name'] = ' '.join([x.strip() for x in name[0].split('\r\n') if x.strip()])

        title = params.xpath('//h3[@class="vt_bioTitle"]/text()').extract()
        if title:
            industrial_system['title'] = ' '.join([x.strip() for x in title[0].split('\r\n') if x.strip()])

        industrial_system['institution'] = 'Virginia Tech'
        industrial_system['department'] = 'Industrial and Systems Engineering'
        industrial_system['division'] = 'College of Engineering'

        email = params.xpath('//li[@class="vt_cl_email"]/a/text()').extract()
        if email:
            industrial_system['email'] = email[0].strip()

        phone = params.xpath('//li[@class="vt_cl_phone"]/text()').extract()
        if phone:
            industrial_system['phone'] = phone[0].strip()

        url = params.xpath('//div[@class="col-lg-6"]//ul/li/a/@href').extract()
        if url:
            industrial_system['url'] = url

        print industrial_system
        return industrial_system

"""
The above faculty member also has the following information:
Address, personal website, research area, professional history, Recent Courses Taught, Recent Publications
and Professional Affiliation.

"""
