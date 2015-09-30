from os.path import exists, abspath, join, dirname
from os import makedirs
import string

from scrapy.conf import settings
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy.exporters import CsvItemExporter
import datetime


class CsvExportPipeline(object):

    def __init__(self):
        dispatcher.connect(self.spider_opened, signals.spider_opened)
        dispatcher.connect(self.spider_closed, signals.spider_closed)
        self.files = {}

    def spider_opened(self, spider):
        current_date = datetime.datetime.now()

        filename = open(
            join(dirname(__file__),
                '../scrape_results/%s_%s.csv' % (
                spider.name,
                current_date.strftime("%Y%m%d_%H%M"))), 'w+b')

        self.files[spider] = filename
        self.exporter = CsvItemExporter(filename)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        filename = self.files.pop(spider)
        filename.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item



