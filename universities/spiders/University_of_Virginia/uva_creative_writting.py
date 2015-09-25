# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
import urlparse

from universities.items import uva_edu


class CreativeWritingSpider(scrapy.Spider):
    """
    Scrape all profiles from
    http://www.engl.virginia.edu

    """
    name = "creative"
    allowed_domains = ["engl.virginia.edu"]
    start_urls = (
        'http://www.engl.virginia.edu/faculty/',
        'http://www.engl.virginia.edu/faculty?keys=&field_specialties_tid=All&page=1',
        'http://www.engl.virginia.edu/faculty?keys=&field_specialties_tid=All&page=2',
        'http://www.engl.virginia.edu/faculty?keys=&field_specialties_tid=All&page=3',
        'http://www.engl.virginia.edu/faculty?keys=&field_specialties_tid=All&page=4',
        'http://www.engl.virginia.edu/faculty?keys=&field_specialties_tid=All&page=5',
        'http://www.engl.virginia.edu/faculty?keys=&field_specialties_tid=All&page=6',

   )

    rules = (
        Rule(SgmlLinkExtractor(allow=(), restrict_xpaths=('//ul[contains(@class, "pager")]//a[contains(., "next")]')),
             callback='parse_listings', follow=True),
    )

    def parse(self, response):
        """
        Parsing creative writing department faculty members profiles page

        """
        response = Selector(response)
        creative_sel = response.xpath('//div[@class="clearfix"]//div')

        for profile_sel in creative_sel:
            my_selector = uva_edu()

            name = profile_sel.xpath('//tr/td[@class="views-field views-field-title"]/h4/a/text()').extract()
            if name:
                my_selector['name'] = name

            title = profile_sel.xpath('//tr/td[@class="views-field views-field-title"]/h5/a/text()').extract()
            if title:
                my_selector['title'] = title

            my_selector['department'] = 'Creative Writing'
            my_selector['institution'] = 'University of virginia'
            my_selector['division'] = 'Arts and Science'

            email = profile_sel.xpath('//tr/td[4][@class="views-field views-field-field-email"]/a/text()').extract()
            if email:
                my_selector['email'] = email

            phone = profile_sel.xpath('//tr/td[4][@class="views-field views-field-field-email"]/span/text()').extract()
            if phone:
                my_selector['phone'] = phone

            url = profile_sel.xpath('//tr/td[@class="views-field views-field-title"]/h4/a/@href').extract()
            if url:
                my_selector['url'] = url

            discipline = profile_sel.xpath('//tr/td[2][@class="views-field views-field-title"]/h5/a/text()').extract()
            if discipline:
                my_selector['discipline'] = discipline
            return my_selector


