# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import University


class liberal_studiesSpider(scrapy.Spider):
    """
    Scrape all faculty members profiles from
    http://www.liberal_studies.nd.edu

    """
    name = "liberal"
    allowed_domains = ["pls.nd.edu"]
    start_urls = (
        'http://pls.nd.edu/faculty-and-staff/',
    )

    def parse(self, response):
        """
        Getting links from Notre Dame university's liberal_studies department

        """
        selection = Selector(response)

        liberal_links = selection.xpath('//div[@role="main"]/ul/li/a/@href').extract()
        for this_link in liberal_links:
            p_link = 'http://www.pls.nd.edu%s' % this_link
            request = Request(p_link,
                              callback=self.parse_liberal_studies)
            print request
            yield request

    def parse_liberal_studies(self, response):
        """
        Parse profile page

        """

        liberal_studies = University()

        sel = Selector(response)

        name = sel.xpath('//h1[@class="page-title"]/text()').extract()
        if name:
            liberal_studies['name'] = ' '.join([x.strip() for x in name[0].split('\r\n') if x.strip()])

        title = sel.xpath('//div[@role="main"]/h2/text()').extract()
        if title:
            liberal_studies['title'] = ' '.join([x.strip() for x in title[0].split('\r\n') if x.strip()])

        liberal_studies['department'] = 'Liberal Studies'
        liberal_studies['division'] = 'Arts and Letters'
        liberal_studies['institution'] = 'Virginia Tech'

        phone = sel.xpath('//h3[contains(text(), "Contact Information")]/following-sibling::p/text()').extract()[3]
        if phone:
            liberal_studies['phone'] = ''.join(phone for phone in phone if phone.isdigit())

        email = sel.xpath('//h3[contains(text(), "Contact Information")]/following-sibling::p/a/text()').extract()
        if email:
            liberal_studies['email'] = email[0].strip()
        url = sel.xpath('//div[@role="main"]/ul/li/a/@href').extract()
        if url:
            liberal_studies['url'] = ' '.join([url.strip() for url in url])
        return liberal_studies

"""
The department of liberal_studies in Notre Dame also has the following information for faculty memebers

Specialization, Education, Research and Teaching Interests, Profiles and CV

"""


