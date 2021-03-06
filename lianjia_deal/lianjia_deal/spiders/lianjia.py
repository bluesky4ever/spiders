import sys
import re
import scrapy
import numpy

from scrapy.loader import ItemLoader
from lianjia_deal.items import LianjiaDealItem

class lianjia(scrapy.Spider):
    name = "deal"
    allowed_domains = ['lianjia.com']
    community = None

    def __init__(self, community='', *args, **kwargs):
        super(lianjia, self).__init__(*args, **kwargs)
        self.community = community

        if self.community == '':
            self.start_urls.append('https://cd.lianjia.com/chengjiao/')
        else:
            self.start_urls.append('https://cd.lianjia.com/chengjiao/rs%s/' % self.community)

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse)

    def find_next_page(self, response):
        nextPage = None

        try:
            page_url = response.xpath("//div[@class='page-box house-lst-page-box']").extract_first()

            totalPage = int(re.findall(r'"totalPage":(\d+)', page_url)[0])
            curPage = int(re.findall(r'"curPage":(\d+)', page_url)[0])

            if curPage+1 <= totalPage:
                index = self.start_urls[0].find('rs')
                if index >=0:
                    nextPage = self.start_urls[0][:index]+'pg'+str(curPage+1)+self.start_urls[0][index:]
                else:
                    nextPage = self.start_urls[0]+'pg'+str(curPage+1)

        except Exception as ex:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            self.logger.error("EXCEPTION at line: " + str(exc_tb.tb_lineno) +", " + str(ex))
            pass
        
        return nextPage

    def parse(self, response):
        unitPriceCollection = []
        unitPriceMean = 0
        allInfo = response.xpath('//div[@class="info"]')
        for info in allInfo:
            try:
                totalPrice, unitPrice = info.css('span.number::text').extract()
                dealDate = info.css('div.dealDate::text').extract()[0]
            except Exception as ex:
                print(str(ex))
                continue

            if unitPriceMean == 0:
                unitPriceMean = int(unitPrice) 

            if int(unitPrice) > 2*unitPriceMean or int(unitPrice) < unitPriceMean/2:
                continue

            unitPriceCollection.append(int(unitPrice))
            unitPriceMean = numpy.mean(unitPriceCollection)

            dealItem = LianjiaDealItem()
            loader = ItemLoader(item=dealItem, response = response)
            loader.add_value('dealDate', dealDate)
            loader.add_value('totalPrice', totalPrice)
            loader.add_value('unitPrice', unitPrice)
            loader.load_item()
            yield dealItem

        next_page = self.find_next_page(response)
        if next_page is not None:
            yield scrapy.Request(next_page, callback=self.parse)