# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver import ChromeOptions
import time

class YymanhuaSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class YymanhuaDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
    def __init__(self):
        self.cookies = "UM_distinctid=16b27cb6ad7848-0b3f2e3c921a83-e353165-1fa400-16b27cb6ad8133; userid=3078664; password=ad07d7c1cc2ccf988f21ecd88272059a; username=hktbgu; Qs_lvt_312019=1559911594; CNZZDATA1277113641=777923930-1559738154-https%253A%252F%252Fwww.baidu.com%252F%7C1559921908; PHPSESSID=34sunuio6hr8t9qda0t5tg1366; __51cke__=; __tins__20090269=%7B%22sid%22%3A%201559922843284%2C%20%22vd%22%3A%2016%2C%20%22expires%22%3A%201559925241116%7D; __tins__20075093=%7B%22sid%22%3A%201559922858232%2C%20%22vd%22%3A%2014%2C%20%22expires%22%3A%201559925591381%7D; __51laig__=30; Qs_pv_312019=2998311743761397000%2C4283844520561964000%2C3135329219143935500%2C1599144478937802000%2C1601538845894795800"
        self.cookies = {i.split("=")[0]:i.split("=")[1] for i in self.cookies.split("; ")}
        # chrome_options = ChromeOptions()
        # chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--disable-gpu')
        #
        # self.browser = webdriver.Chrome(options=chrome_options)
        self.browser = webdriver.Chrome()
        time.sleep(2)
        self.browser.get('http://kuyi.9ifa.com')
        time.sleep(2)

        for key, value in self.cookies.items():
            self.browser.add_cookie({'name': key, 'value': value})
        time.sleep(3)



    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        if spider.name == "yymh":
            self.browser.get(request.url)
            time.sleep(1)
            origin_code = self.browser.page_source
            res = HtmlResponse(url=request.url, encoding="utf-8", body=origin_code, request=request)
            return res


    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
