# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HouseSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    houseId = scrapy.Field()
    Name = scrapy.Field()
    Rooms = scrapy.Field()
    Floor = scrapy.Field()
    ConstructionSize = scrapy.Field()
    RoomStructure = scrapy.Field()
    InnerSize = scrapy.Field()
    ConstructionType = scrapy.Field()
    Orientation = scrapy.Field()
    CompletionDate = scrapy.Field()
    Decoration = scrapy.Field()
    ConstructionStructure = scrapy.Field()
    HeatingMethod = scrapy.Field()
    ElevatorRatio = scrapy.Field()
    PropertyRights = scrapy.Field()
    Usage = scrapy.Field()
    DealDate = scrapy.Field()
    TotalPrice = scrapy.Field()
    UnitPrice = scrapy.Field()
    Quote = scrapy.Field()
    CycleTime = scrapy.Field()
    OtherInfo = scrapy.Field()
