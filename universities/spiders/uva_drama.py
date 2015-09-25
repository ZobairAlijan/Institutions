# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import uva_edu


class DramaSpider(scrapy.Spider):
    """
    Scrape all profiles from
    http://www.drama.virginia.edu

    """
    name = "uva_drama"
    allowed_domains = ["drama.virginia.edu"]
    start_urls = (
        'http://drama.virginia.edu/faculty',
        'http://drama.virginia.edu/faculty?page=1',
    )

    def parse(self, response):
        """
        Parsing faculty members profiles page from department of drama

        """
        this_selector = Selector(response)
        drama_sel = this_selector.xpath('//div[@class="content clearfix"]//div')

        for profile_sel in drama_sel:
            zextractor_genisys = uva_edu()

            name = profile_sel.xpath('//tr/td[@class="views-field views-field-title"]/h4/a/text()').extract()
            if name:
                zextractor_genisys['name'] = name

            title = profile_sel.xpath('//tr/td[@class="views-field views-field-title"]/h5/text()').extract()
            if title:
                zextractor_genisys['title'] = title

            zextractor_genisys['department'] = 'drama'
            zextractor_genisys['institution'] = 'University of Virginia'
            zextractor_genisys['division'] = 'Arts and Science'

            email = profile_sel.xpath('//tr/td[@class="views-field views-field-field-email"]/a/text()').extract()
            if email:
                zextractor_genisys['email'] = email

            phone = profile_sel.xpath('//tr/td[@class="views-field views-field-field-email"]/span/text()').extract()
            if phone:
                zextractor_genisys['phone'] = phone

            url = profile_sel.xpath('//tr/td[@class="views-field views-field-title"]/h4/a/@href').extract()
            if url:
                zextractor_genisys['url'] = url
            return zextractor_genisys


