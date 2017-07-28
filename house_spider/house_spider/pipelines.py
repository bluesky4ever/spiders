# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import os
import re

class HouseSpiderPipeline(object):
    fp = None
    json_file = '/tmp/house.json'
    floor_dict = {
        "低楼层":0,
        "中楼层":1,
        "高楼层":2
    }

    def open_spider(self, spider):
        if os.path.exists(self.json_file):
            print("remove {0}".format(self.json_file))
            os.remove(self.json_file)
        self.fp = open(self.json_file, 'a+')

    def close_spider(self, spider):
        self.fp.close()

    def process_item(self, item, spider):
        item['houseId'] = item['houseId'][0]
        item['Name'] = item['Name'][0]
        item['Rooms'] = item['Rooms'][0]
        # Parse Floor
        try:
            floor = item['Floor'][0]
            if len(floor) > 3:
                floor = floor[:3]
            item['Floor'] = self.floor_dict[floor]
        except Exception as err:
            item['Floor'] = -1
        # Parse Size
        for key in ['ConstructionSize', 'InnerSize']:
            csize = item[key][0]
            m = re.match('(\d+.\d+)*',csize)
            if len(m.group(0)) == 0:
                item[key] = -1 # not find, set to -1
            else:
                item[key] = float(m.group(0)) # digital value

        item['RoomStructure'] = item['RoomStructure'][0]


        line = json.dumps(dict(item), ensure_ascii=False, indent=4) + "\n"
        self.fp.write(line)
        return item
