# -*- coding: utf-8 -*-
import scrapy
import datetime
import urlparse
import socket



from scrapy.loader.processors import MapCompose, Join
from scrapy.loader import ItemLoader
from scrapy.http import Request
from chuji.items import ChujiItem


class ZcoolSpider(scrapy.Spider):
    name = "zcool"
    allowed_domains = ["zcool.com"]
    start_urls = (
        'http://www.zcool.com.cn/works/33!0!!0!0!200!1!1!!!/',
    )

    def parse(self, response):
        next_selector = response.xpath("//a[@class='pageNext']/@href")
        for url in next_selector.extract():
            yield Request(urlparse.urljoin('http://www.zcool.com.cn', url),dont_filter=True)

        # Iterate through products and create PropertiesItems
        selectors = response.xpath('//ul[@class="layout camWholeBoxUl"]/li/a/@href')
        for selector in selectors.extract():
            yield Request(selector,callback=self.parse_item,dont_filter=True)

    def parse_item(self,response):
        l = ItemLoader(item=ChujiItem(),response=response)
        l.add_xpath('image_urls', '//div[@class="wsContent wsContentPo"]/a[2]/img/@src')
        return l.load_item()