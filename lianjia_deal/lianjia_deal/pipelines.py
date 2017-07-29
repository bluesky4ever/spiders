# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import lianjia_deal.myutils.draw as mydraw
import lianjia_deal.myutils.dumpjs as mydumpjs

class LianjiaDealPipeline(object):
    line = None
    item_collection = []

    fp = None
    json_file = ''

    def open_spider(self, spider):
        pass


    def close_spider(self, spider):
        draw = mydraw.Draw(self.item_collection)
        draw.draw_line(spider.community)

        js = mydumpjs.DumpJs(self.item_collection, spider.community, '.')
        js.dump_to_js()

    def process_item(self, item, spider):

        self.item_collection.append(item)

        return item
