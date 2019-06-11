# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient

class YymanhuaPipeline(object):
    def process_item(self, item, spider):
        # 插入数据库
        item["_id"] = self.count
        self.collection.insert(item)
        self.count += 1

        return item

    def open_spider(self,spider):
        self.client = MongoClient()
        self.collection = self.client["pySpider"]["yymh_2"]
        self.count = 1
        print("数据库以连接...")

    def close_spider(self, spider):
        self.client.close()
        print("数据库连接关闭")