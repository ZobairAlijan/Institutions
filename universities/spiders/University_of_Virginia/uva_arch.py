# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor


from universities.items import University


class SociologySpider(scrapy.Spider):
    """
    Scrape all profiles from
    http://www.sociology.virginia.edu

    """
    name = "arch"
    allowed_domains = ["arch.virginia.edu"]
    start_urls = (
        'http://www.arch.virginia.edu/people/directory',
        'http://www.arch.virginia.edu/people/directory?p=2',
        'http://www.arch.virginia.edu/people/directory?p=3',
        'http://www.arch.virginia.edu/people/directory?p=4',
        'http://www.arch.virginia.edu/people/directory?p=5',
        'http://www.arch.virginia.edu/people/directory?p=6',
        'http://www.arch.virginia.edu/people/directory?p=7',
        'http://www.arch.virginia.edu/people/directory?p=8',
        'http://www.arch.virginia.edu/people/directory?p=9',
        'http://www.arch.virginia.edu/people/directory?p=10',
        'http://www.arch.virginia.edu/people/directory?p=11',
        'http://www.arch.virginia.edu/people/directory?p=12',
        'http://www.arch.virginia.edu/people/directory?p=13',
    )
    rules = (
        Rule(SgmlLinkExtractor(allow=(), restrict_xpaths=('//a[@class="next"]',)), callback="parse_item", follow= True),
    )

    def parse_item(self, response):
        """
        Parsing faculty members profiles page from department of Sociology

        """
        my_sel = Selector(response)
        global_sel = my_sel.xpath('//div[@class="region region-content"]/div')

        for socio_sel in global_sel:
            item = University()

            name = socio_sel.xpath('//a[@class="result clearfix"]/h4/text()').extract()
            if name:
                item['name'] = ' '.join([name.strip() for name in name])

            title = socio_sel.xpath('//span[@class="position"]/text()').extract()
            if title:
                item['title'] = ' '.join([title.strip() for title in title])

            item['department'] = 'Architecture'
            item['institution'] = 'University of Virginia'
            item['division'] = 'School of Architecture'

            email = socio_sel.xpath('//span[@class="email"]/text()').extract()
            if email:
                item['email'] = email

            phone = socio_sel.xpath('//span[@class="phone"]/text()').extract()
            if phone:
                item['phone'] = ' '.join([phone.strip() for phone in phone])

            url = socio_sel.xpath('//a[@class="result clearfix"]/@href').extract()
            if url:
                item['url'] = ' '.join([url.strip() for url in url])
            return item

