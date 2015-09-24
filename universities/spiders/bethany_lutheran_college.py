# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import University


class BethanyLutheranSpider(scrapy.Spider):
    """
    Scrape all profiles from
    http://www.mendoza.nd.edu

    """
    name = "blc"
    allowed_domains = ["blc.edu"]
    start_urls = (
        'http://www.blc.edu/directory/faculty-staff',
    )

    def parse(self, response):
        """
        Parse profiles page

        """
        sel = Selector(response)
        people_sel = sel.xpath('//div[@class="view-content"]')

        for profile_sel in people_sel:
            bii = University()

            name = profile_sel.xpath('br','//td[@class="views-field views-field-title"]/text()').extract()
            if name:
                bii['name'] = name
            #
            # title = profile_sel.xpath('//td[@class="views-field views-field-field-job-title"]/text()').extract()
            # if title:
            #     bii['title'] = title

            # department = [profile_sel.xpath('''.//td/text()[count(preceding-sibling::br)=%d]
            #                                                 [not(self::br)]''' % i).extract()
            # for i in range(0, len(sel.xpath('.//td/br')) + 1)]
            #
            # if department:
            #     bii['department'] = department[0].strip()

            # bii['institution'] = 'Bethany Lutheran College'

            # phone = profile_sel.xpath('//td[@class="views-field views-field-nid"]/text() | //td[@class="views-field views-field-nid"]/br').extract()
            # if phone:
            #     bii['phone'] = phone
            return bii


