# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re

class AqSpider(CrawlSpider):
    name = 'aq'
    allowed_domains = ['aqdydl.com']
    start_urls = ['http://aqdydl.com/lusi/']

    rules = (
        Rule(LinkExtractor(allow=r'/shebao/(.*?)/'), callback='parse_item'),
        Rule(LinkExtractor(allow=r'/shebao/(.*?).html'), follow=True),
    )

    def parse_item(self, response):
        item = {}
        item["play_pic_url"] = response.xpath('//*[@id="先锋影音-pl-list"]/div[2]/p/a/@href').extract_first()
        item["play_pic_url"] = "http://aqdydl.com" + item["play_pic_url"]
        # print(item["play_pic_url"])
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        yield scrapy.Request(
            item["play_pic_url"],
            callback=self.parse_play_url,
            meta={"item": item}
        )

    def parse_play_url(self,response):
        item = response.meta["item"]
        item["play_url"] = response.xpath('//*[@id="player"]/script[1]/@src').extract_first()
        item["play_url"] = "http://aqdydl.com" + item["play_url"]
        yield scrapy.Request(
            item["play_url"],
            callback=self.parse_xfplay_links,
            meta={"item": item}
        )
    def parse_xfplay_links(self,response):
        item = response.meta["item"]
        item["xfplay_link"] =  re.findall("xfplay:(.*?)']]]", str(response.body))
        item["xfplay_link"] = "xfplay:" + item["xfplay_link"][0]
        yield item
