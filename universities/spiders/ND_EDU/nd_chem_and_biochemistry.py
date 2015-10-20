# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from scrapy.selector import Selector

from universities.items import University


class BioChemistrySpider(scrapy.Spider):
    """
    Scrape all faculty members profiles from
    http://www.chemistry.nd.edu

    """
    name = "nd_chemistry"
    allowed_domains = ["chemistry.nd.edu"]
    start_urls = (
        'http://chemistry.nd.edu/faculty-research/',
    )

    def parse(self, response):
        """
        Getting links from department of Chemistry and Biochemistry in Notre Dame university

        """
        selection = Selector(response)

        bio_chem_links = selection.xpath('//ul[@class="faculty-list"]/li/h3/a/@href').extract()
        for that_link in bio_chem_links:
            ch_link = 'http://www.chemistry.nd.edu%s' % that_link
            request = Request(ch_link,
                              callback=self.parse_chemistry)
            print request
            yield request

    def parse_chemistry(self, response):
        """
        Parse profile page

        """

        history_design = University()

        sel = Selector(response)

        name = sel.xpath('//div[@class="caption position-left"]/h2/text()').extract() + \
            sel.xpath('//div[@class="caption position-right"]/h2/text()').extract() + \
            sel.xpath('//div[@class="info-content"]/header/h1/text()').extract()
        if name:
            history_design['name'] = ' '.join([name.strip() for name in name])

        title = sel.xpath('//div[@class="info-secondary"]/ul/li[1]/text()').extract()
        if title:
            history_design['title'] = ' '.join([title.strip() for title in title])

        history_design['department'] = 'Chemistry and Bio chemistry'
        history_design['division'] = 'College of Science'
        history_design['institution'] = 'Notre Dame'

        phone = sel.xpath('//div[@class="info-secondary"]/ul/li[3]/text()').extract()
        if phone:
            history_design['phone'] = ''.join([phone for phone in phone if phone])

        email = sel.xpath('//div//a[contains(@href,"mailto:")]/@href').extract()
        if email:
            history_design['email'] = ' '.join([email.strip() for email in email])
        return University(**history_design)

"""
The department of Chemsitry and Biochemistry in Notre Dame also has the following information for faculty members

Bio, selected awards, research interests, research specialties, recenet papers, gallery

"""
