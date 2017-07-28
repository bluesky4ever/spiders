#!/bin/bash
house='中环岛 五洲花园 光明城市 千居朝阳 华润二十四城 华润凤凰城 向阳小区 天悦府 左岸花都 戛纳滨江 蜀郡'

for h in $house
do
    echo "scrapy crawl deal -a community=$h"
    scrapy crawl deal -a community=$h
done
