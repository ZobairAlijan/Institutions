# -*- coding: utf-8 -*-
import scrapy
from universities.items import University


class EngineeringSpider(scrapy.Spider):
    name = "eng"
    allowed_domains = ["engineering.nd.edu"]
    start_urls = (
        'http://engineering.nd.edu/people#c1=nd.content.member&c12=enabled&c9=last_name&c5=all&b_start=0',
    )

    def parse(self, response):

        if 'next_page' in response.request.meta:
            pass

        for e_url in response.xpath('//div[@class="faceted-results"]//dt/div[@class="memberName"]/a/@href').extract():
            yield scrapy.Request(e_url, meta={}, callback=self.parse_member)

        for e in response.xpath('//div[@class="listingBar"]/span[@class="next"]/a/@href').extract():
            yield scrapy.Request(e, meta={'next_page': True}, callback=self.parse)

    def parse_member(self, response):
        result = dict(
            name=' '.join(response.xpath('//h1[@class="documentFirstHeading memberName"]/text()')
                          .extract_first().replace('\n', '').split()),
            title=' '.join(response.xpath('//div[@class="affiliations"]/h2[@class="organisation"]/text()')
                           .extract_first().replace('\n', '').split()),
            email=' '.join(response.xpath('//div[@class="contact-info"]/p/a/@title')
                           .extract_first().replace('\n', '').split()),
            department=' '.join(response.xpath('//div[@class="affiliations"]/p/a/text()')
                           .extract_first().replace('\n', '').split()),
            division=' '.join(response.xpath('//div[@class="other-affiliation"]/p/a/text()')
                           .extract_first().replace('\n', '').split()),
            phone=response.xpath('//div[@class="contact-info"]/p[2]').re(r'</strong>(.*)<br>')[0])

        result['institution'] = 'Notre Dame'
        return result
