# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient

class AqdyPipeline(object):
    def process_item(self, item, spider):
        xfplay_link = {}
        xfplay_link["_id"] = self.count
        xfplay_link["play_pic_url"] = item["play_pic_url"]
        xfplay_link["xfplay_link"] = item["xfplay_link"]
        # 插入数据库
        # self.collection.insert(xfplay_link)
        self.count += 1
        return item
    def open_spider(self,spider):
        self.client = MongoClient()
        self.collection = self.client["pySpider"]["lusi"]
        self.count = 1
        print("数据库以连接...")

    def close_spider(self,spider):
        self.client.close()
        print("数据库连接关闭")
