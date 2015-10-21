# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import University


class CropSoilSpider(scrapy.Spider):
    """
    Scrape all faculty members profiles from
    http://www.cses.vt.edu

    """
    name = "soil"
    allowed_domains = ["cses.vt.edu"]
    start_urls = (
        'http://www.cses.vt.edu/people/tenure/index.html',
    )

    def parse(self, response):
        """
        Getting links from department of Animal Poultry Sciences

        """
        sel = Selector(response)

        links = sel.xpath('//div[@class="col-lg-9"]//tr/td[1]/a/@href').extract()
        for link in links:
            p_link = 'http://www.cses.vt.edu%s' % link
            request = Request(p_link,
                              callback=self.parse_crop_soil)
            assert isinstance(request, object)
            print request
            yield request

    def parse_crop_soil(self, response):
        """
        Parse faculty members profile from the department of  Crop, Soil, and Environmental Science

        """
        soil_sel = Selector(response)

        item = University()

        name = soil_sel.xpath('//div[@id="vt_bio_top"]/h2/text()').extract()
        if name:
            item['name'] = ' '.join([this.strip() for this in name[0].split('\r\n') if this.strip()])

        title = soil_sel.xpath('//div[@id="vt_bio_top"]/h3/text()').extract()
        if title:
            item['title'] = ' '.join([this.strip() for this in title[0].split('\r\n') if this.strip()])
        item['department'] = 'Crop, Soil, and Environmental Science'
        item['division'] = 'College of Agriculture and Life Sciences'
        item['institution'] = 'Virginia Tech'

        email = soil_sel.xpath('//li[@class="vt_cl_email"]/a/text()').extract()
        if email:
            item['email'] = ' '.join([this.strip() for this in email[0].split('\r\n') if this.strip()])

        phone = soil_sel.xpath('//li[@class="vt_cl_phone"]/text()').extract()
        if phone:
            item['phone'] = ' '.join([x.strip() for x in phone[0].split('\r\n') if x.strip()])

        return University(item)
