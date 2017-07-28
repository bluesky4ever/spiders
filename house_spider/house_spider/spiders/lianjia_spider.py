import sys
import scrapy
import re
import string
import random
import json

class lianjiaSpider(scrapy.Spider):
    name = 'lianjia'
    allowed_domains = ['lianjia.com']
    start_urls = [
            'https://cd.lianjia.com/chengjiao/'
            ]

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0], callback=self.parse, errback=self.handle_error)


    def find_next_page(self, response):

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

        return nextPage

    def parse_house_info(self, house_info):
        house_list = house_info.extract()
        start = 0
        end = 0
        for i, c in enumerate(house_list):
            if c.find('成交周期') >= 0:
                end = i
                yield house_list[start:end+1]
                start = end + 1

    def compose_single_house(self, ahouse):
        # pad the ahouse to 13 elements
        diff = 13 - len(ahouse)
        pad = ["" for _ in range(diff)]
        # pad end at 11th elements
        index = 11 - diff

        ahouse[index:index] = pad

        title, rooms, size = ahouse[0].split(" ")
        houseid = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10)) # assign unique id  to the room
        houses = dict()
        houses[houseid] = dict()
        houses[houseid]['title'] = title
        houses[houseid]['rooms'] = rooms
        houses[houseid]['size'] = size
        houses[houseid]['info'] = ahouse[1] + ' | ' + ahouse[9] + ' | ' + ahouse[10]
        houses[houseid]['dealDate'] = ahouse[2]
        houses[houseid]['totalPrice'] = float(ahouse[3])*10000 if ahouse[3].isdecimal() else 'N/A'
        houses[houseid]['houseType'] = ahouse[5]
        houses[houseid]['unitPrice'] = float(ahouse[7]) if ahouse[7].isdecimal() else 'N/A'
        # find quotes. chinese charactor ranges from \u4e00 to \u9fa5
        m = re.match(u'[\u4e00-\u9fa5]*(\d+\.?\d+)[\u4e00=\u9fa5]*', ahouse[11])
        quote = float(m.group(1)) if m is not None else ''
        houses[houseid]['quote'] = quote
        houses[houseid]['cycleTime'] = ahouse[12]

        # write to json file
        with open("house.json", 'a+') as fp:
            json.dump(houses, fp, ensure_ascii=False, indent=4 )


    def handle_error(self, failure):
        self.logger.error(repr(failure))

    def parse(self, response):
        house_info = response.xpath("//div[@class='info']//text()")
        if not house_info: # list is empty
            # possible captcha
            redirect_urls = response.request.meta.get('redirect_urls')
            for url in redirect_urls:
                self.logger.info("REDIRECT: " + url)
        else:
            for single_house in self.parse_house_info(house_info):
                self.compose_single_house(single_house)

            next_page = self.find_next_page(response)
            if next_page is not None:
                yield scrapy.Request(next_page, callback=self.parse, errback=self.handle_error)



