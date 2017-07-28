import sys
import scrapy
import re
import string
import random
from scrapy.loader import ItemLoader
from house_spider.items import HouseSpiderItem

class lianjiaSpider(scrapy.Spider):
    iteration = 0
    name = 'lianjia1'
    allowed_domains = ['lianjia.com']
    start_urls = [
            'https://cd.lianjia.com/chengjiao/'
            ]
    houses = []

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0], callback=self.parse, errback=self.handle_error)

    def find_next_page(self, response):

        self.iteration += 1
        nextPage = None

        try:
            page_url = response.xpath("//div[@class='page-box house-lst-page-box']").extract_first()
            m = re.match(r'<div class="page-box house-lst-page-box" comp-module="page" page-url="(\/\w+\/\w+)\{page\}/" page-data=\'{"totalPage":(\d+),"curPage":(\d+)}\'></div>', page_url)

            totalPage = int(m.group(2))
            curPage = int(m.group(3))

            if curPage+1 < totalPage:
                nextPage = self.start_urls[0]+'pg'+str(curPage+1)

        except Exception as ex:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            self.logger.error("EXCEPTION at line: " + str(exc_tb.tb_lineno) +", " + str(ex))
            pass

        return None

      #  if self.iteration < 1:
      #      return nextPage
      #  else:
      #      return None

    def parse_detail(self, response):
        houseItem = HouseSpiderItem()
        loader = ItemLoader(item=houseItem, response=response)

        try:
            loader.add_value('houseId', ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10)))
            loader.add_xpath('TotalPrice', '//span[@class="dealTotalPrice"]//text()')
            loader.add_css('UnitPrice','div.price b::text')
            title = response.xpath('//div[@class="house-title"]/div[@class="wrapper"]//text()').extract()[0]
            loader.add_value('Name', title.split(" ")[0])
            all_info = response.xpath('//div[@class="introContent"]//li/text()').extract()
            loader.add_value('Rooms', all_info[0].strip())
            loader.add_value('Floor', all_info[1].strip())
            loader.add_value('ConstructionSize', all_info[2].strip())
            loader.add_value('RoomStructure', all_info[3].strip())
            loader.add_value('InnerSize', all_info[4].strip())
            loader.add_value('ConstructionType', all_info[5].strip())
            loader.add_value('Orientation', all_info[6].strip())
            loader.add_value('CompletionDate',all_info[7].strip())
            loader.add_value('Decoration', all_info[8].strip())
            loader.add_value('ConstructionStructure', all_info[9].strip())
            loader.add_value('HeatingMethod', all_info[10].strip())
            loader.add_value('ElevatorRatio', all_info[11].strip())
            loader.add_value('PropertyRights', all_info[12].strip())
            loader.add_value('Usage', all_info[17].strip())
            exchange_record = response.xpath("//p[@class='record_detail']//text()").extract()[0]
            loader.add_value('DealDate', exchange_record.split(',')[2])
        except IndexError as err:
            self.logger.error(str(err))

        loader.load_item()
        self.houses.append(houseItem)
        yield houseItem


    def handle_error(self, failure):
        self.logger.error(repr(failure))

    def parse(self, response):
        allinfo = response.xpath("//div[@class='info']")
        for i, info in enumerate(allinfo):
            name, rooms, size = info.css('a::text').extract()[0].split(" ")
            detail_link = info.css('a::attr(href)').extract()[0]
            # print("{0}: {1} | {2} | {3} | {4}".format(i, name, rooms, size, detail_link))
            yield scrapy.Request(detail_link, callback=self.parse_detail)

        next_page = self.find_next_page(response)
        if next_page is not None:
            yield scrapy.Request(next_page, callback=self.parse, errback=self.handle_error)



