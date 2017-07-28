# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pyecharts import Line

class LianjiaDealPipeline(object):
    line = None
    x_axis = []
    points = []

    def open_spider(self, spider):
        self.line = Line(spider.community[0])

    def close_spider(self, spider):
        self.line.add(spider.community[0], self.x_axis, self.points)
        self.line.show_config()
        self.line.render(spider.community[0] + '.html')

    def process_item(self, item, spider):
        self.x_axis.append(item['dealDate'][0])
        self.points.append(item['unitPrice'][0])
        return item
