# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import University


class MathematicsSpider(scrapy.Spider):
    """
    Scrape all profiles from
    http://www.mediastudies.virginia.edu

    """
    name = "music"
    allowed_domains = ["virginia.edu"]
    start_urls = (
        'http://music.virginia.edu/faculty',
        'http://philosophy.virginia.edu/faculty',
        'http://ppl.virginia.edu/faculty',
    )

    def parse(self, response):
        """
        Parsing faculty members profiles page from department of Media Studies

        """
        my_sel = Selector(response)
        m_sel = my_sel.xpath('//div[@class="view-content"]')

        for music_sel in m_sel:
            the_global = University()

            name = music_sel.xpath('//tr/td[@class="views-field views-field-title"]/h3/a/text()').extract() + \
                music_sel.xpath('//tr/td[@class="views-field views-field-field-position"]/h3/a/text()').extract() + \
                music_sel.xpath('//tr/td[@class="views-field views-field-title"]/h2/a/text()').extract()


            if name:
                the_global['name'] = ' '.join([name.strip() for name in name])

            title = music_sel.xpath('//tr/td[@class="views-field views-field-title"]/h5/text()').extract() + \
                music_sel.xpath('//tr/td[@class="views-field views-field-field-position"]/p/em/text()').extract() + \
                music_sel.xpath('//tr/td[@class="views-field views-field-title"]/text()').extract()
            if title:
                the_global['title'] = ' '.join([title.strip() for title in title])

            the_global['department'] = 'Music, philosophy and political philosophy'
            the_global['institution'] = 'University of Virginia'
            the_global['division'] = 'Arts and Science'

            email = music_sel.xpath('//tr/td[@class="views-field views-field-field-email"]/a/text()').extract() + \
                music_sel.xpath('//tr/td[@class="views-field views-field-field-email"]/p/a/text()').extract()
            if email:
                the_global['email'] = email
            phone = music_sel.xpath('//tr/td[@class="views-field views-field-field-email"]/p/a/text()').extract() + \
                    music_sel.xpath('//tr/td[@class="views-field views-field-field-e-mail"]/a/text()').extract()

            if phone:
                the_global['phone'] = ' '.join([phone.strip() for phone in phone])

            url = music_sel.xpath('//tr/td[@class="views-field views-field-title"]/h3/a/@href').extract() + \
                music_sel.xpath('//tr/td[@class="views-field views-field-field-position"]/h3/a/@href').extract() + \
                music_sel.xpath('//tr/td[@class="views-field views-field-title"]/h2/a/@href').extract()
            if url:
                the_global['url'] = url
            return the_global
