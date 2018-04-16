# -*- coding: utf-8 -*-
import scrapy

from tencent_hr.items import TencentHrItem


class TencentSpider(scrapy.Spider):
    name = 'tencent'
    setoff = 0
    allowed_domains = ['hr.tencent.com']
    start_urls = ['https://hr.tencent.com/position.php?keywords=python&start=0#a']

    def parse(self, response):
        teccent_item = TencentHrItem()
        tables = response.xpath('//table[@class="tablelist"]//tr')
        for table in tables:
            teccent_item['position']  = table.xpath('./td[1]/a/text()').extract()
            teccent_item['number'] = table.xpath('./td[3]/text()').extract()
            teccent_item['place'] = table.xpath('./td[4]/text()').extract()
            yield teccent_item

        if self.setoff<200:
            self.setoff+=10
        newurl = 'https://hr.tencent.com/position.php?keywords=python&start='+str(self.setoff)+'#a'
        yield scrapy.Request(newurl,callback=self.parse)