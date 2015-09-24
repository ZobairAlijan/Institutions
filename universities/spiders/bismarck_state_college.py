# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import BabsonEduItem


class BismarckSpider(scrapy.Spider):
    """
    Scrape all profiles from
    http://www.bismarckstate.edu

    """
    name = "bismarck"
    allowed_domains = ["bismarckstate.edu"]
    start_urls = (
        'http://www.bismarckstate.edu/staff/directory/?nType=fac',
        'http://www.bismarckstate.edu/staff/directory/?nType=staff'
    )

    def parse(self, response):
        """
        Parse faculty page

        """
        sel = Selector(response)
        link_sel = sel.xpath('//table[@class="layoutTable"]/tr')

        for bism_sel in link_sel:
            eid_mubarak = BabsonEduItem()

            name = bism_sel.xpath('//td[@class="copyTbold"]/text()').extract()
            if name:
                eid_mubarak['name'] = name

            title = bism_sel.xpath('//td[contains(text(), "Title")]/following-sibling::td/text()').extract()
            if title:
                eid_mubarak['title'] = title

            department = bism_sel.xpath('//td[contains(text(), "Discipline:")]/following-sibling::td/text()').extract() + \
                bism_sel.xpath('//td[contains(text(), "Department:")]/following-sibling::td/text()').extract()

            if department:
                eid_mubarak['department'] = department

            eid_mubarak['institution'] = 'Bismarck State College'

            email = bism_sel.xpath('//td[contains(text(), "Email Address:")]/following-sibling::td/a/text()').extract()
            if email:
                eid_mubarak['email'] = email

            phone = bism_sel.xpath('//td[contains(text(), "Department Chair:")]/following-sibling::td/text()').extract() + \
                bism_sel.xpath('//td[contains(text(), "Telephone:")]/following-sibling::td/text()').extract()

            if phone:
                eid_mubarak['phone'] = phone

            return eid_mubarak

