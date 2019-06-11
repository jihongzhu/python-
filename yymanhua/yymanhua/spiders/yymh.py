# -*- coding: utf-8 -*-
import scrapy
import re
import json
from copy import deepcopy

# hktbgu
#
# 密码：636010

class YymhSpider(scrapy.Spider):
    name = 'yymh'
    allowed_domains = ['kuyi.9ifa.com']
    start_urls = ['http://kuyi.9ifa.com/home/user/index.html']
    def __init__(self):
        super().__init__()
        with open(r'G:\python\pyhon_PyChar\爬虫项目\Scrapy框架\venv\Scrapy_12\yymanhua\yymanhua\spiders\yymh_json.json', "r") as f:
            self.href_list = json.loads(f.read())


    def start_requests(self):
        cookies = "UM_distinctid=16b27cb6ad7848-0b3f2e3c921a83-e353165-1fa400-16b27cb6ad8133; userid=3078664; password=ad07d7c1cc2ccf988f21ecd88272059a; username=hktbgu; Qs_lvt_312019=1559911594; CNZZDATA1277113641=777923930-1559738154-https%253A%252F%252Fwww.baidu.com%252F%7C1559921908; PHPSESSID=34sunuio6hr8t9qda0t5tg1366; __51cke__=; __tins__20090269=%7B%22sid%22%3A%201559922843284%2C%20%22vd%22%3A%2016%2C%20%22expires%22%3A%201559925241116%7D; __tins__20075093=%7B%22sid%22%3A%201559922858232%2C%20%22vd%22%3A%2014%2C%20%22expires%22%3A%201559925591381%7D; __51laig__=30; Qs_pv_312019=2998311743761397000%2C4283844520561964000%2C3135329219143935500%2C1599144478937802000%2C1601538845894795800"
        cookies = {i.split("=")[0]:i.split("=")[1] for i in cookies.split("; ")}
        # headers = {"Cookie":cookies}
        for href in self.href_list:
            yield scrapy.Request(
                href,
                callback=self.parse,
                cookies=cookies
                # headers=headers
            )

    def parse(self, response):
        item = {}
        # print(re.findall("id: (\d+)",response.body.decode()))
        number_list = re.findall("id: (\d+)", response.body.decode())
        # print(re.findall("hktbgu", response.body.decode()))
        for number in number_list:
            index_url = 'http://kuyi.9ifa.com/home/api/isread/id/' + number
            yield scrapy.Request(
                index_url,
                callback=self.parse_detail_page,
                meta={"item": deepcopy(item)}
            )

    def parse_detail_page(self,response):
        item = response.meta["item"]
        detail_number = re.findall('"capter_id":"(\d+)"',response.body.decode())[0]
        item["detail_url"] = "http://kuyi.9ifa.com/home/book/capter/id/" + str(detail_number)
        # print(item["detail_url"])
        yield scrapy.Request(
            item["detail_url"],
            callback=self.parse_image_url,
            meta={"item":deepcopy(item)}
        )

    def parse_image_url(self,response):
        item = response.meta["item"]
        page_list = re.findall(r'第\d+話',response.body.decode())
        for page in page_list:
            image_url = {}
            div_list = response.xpath('//*[@id="framework7-root"]/div[4]/div/div/div[2]/div[1]/article/section/div/img')
            item["name"] = response.xpath('/html/head/title/text()').extract_first().strip()
            for div in div_list:
                img = div.xpath('./@src').extract_first()
                alt = div.xpath('./@alt').extract_first()
                image_url[alt] = img

            if page not in item.keys():
                item[page] = image_url



        # 找出下一话的地址
        next_url = re.findall("getJSON\('(.*?)'",response.body.decode())
        if next_url:
            item["next_url"] = "http://kuyi.9ifa.com" + next_url[0] + "1"
            # print(item["next_url"])

            yield scrapy.Request(
                item["next_url"],
                callback=self.parse_next_page,
                meta={"item": item}
            )


    def parse_next_page(self,response):
        item = response.meta["item"]
        next = re.findall('"id":"(\d+)"',response.body.decode())
        if next:
            next = "http://kuyi.9ifa.com/home/book/capter/id/" + str(next[0])
            page_json = json.loads(response.body.decode())
            # print(page_json)
            title = page_json["result"]["title"].replace('.', '-') #key中不能有包含“.”
            url_dict = {}
            # print(page_json["result"]["imagelist"])
            # for i in page_json["result"]["imagelist"].split(','):
            #     print(i.split('./')[1])

            for (i, img) in enumerate(page_json["result"]["imagelist"].split(',')):
                alt = "图-{}".format(i + 1)
                url_dict[alt] = img.split('./')[1]
                url_dict[alt] = "http://cdn.utey6j.top/" + url_dict[alt]

            item[title] = url_dict
            # print(next)
            yield scrapy.Request(
                next,
                callback=self.parse_image_url,
                meta={"item": item}
            )
        else:
            # 传到管道去，保存数据库
            yield item