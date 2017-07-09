# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

# open_spider, close_spider, process_item, 基本上是三部曲不用修改，唯一需要修改的是open 中的file名称
#

from scrapy.exporters import CsvItemExporter


class AirQualityPipeline(object):

    def open_spider(self,spider):
        self.file = open('air_quaility.csv','w+b')
        self.exporter = CsvItemExporter(self.file)
        self.exporter.start_exporting()

    def close_spider(self,spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item



