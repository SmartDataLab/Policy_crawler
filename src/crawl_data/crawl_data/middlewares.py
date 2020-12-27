# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.http import HtmlResponse
import time
import random
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
import requests
import json

user_agent_list = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 "
    "(KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 "
    "(KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 "
    "(KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 "
    "(KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 "
    "(KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 "
    "(KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 "
    "(KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 "
    "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 "
    "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
]


class RandomUserAgent(UserAgentMiddleware):  # 如何运行此中间件? settings 直接添加就OK
    def process_request(self, request, spider):
        ua = random.choice(user_agent_list)
        # 在请求头里设置ua
        request.headers.setdefault("User-Agent", ua)


class CrawlDataSpiderMiddleware(object):
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

        # Should return either None or an iterable of Request, dict
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
        spider.logger.info("Spider opened: %s" % spider.name)


class CrawlDataDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

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
        return None

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
        spider.logger.info("Spider opened: %s" % spider.name)


class SeleniumDownloaderMiddleware(object):
    def __init__(self):
        self.lasttime = time.time()
        self.lastip = self.get_proxy()

    # 可以拦截到request请求
    def process_request(self, request, spider):
        if spider.name in [
            "Central",
            "Henan",
            "Xizang",
            "Tianjin",
            "Anhui",
            "Yunnan",
            "Shaanxi_shan",
            "Shandong",
        ]:
            t = time.time()
            if t - self.lasttime <= 10:
                ret_proxy = self.lastip
            else:
                ret_proxy = self.get_proxy()
                if len(ret_proxy) > 0:
                    self.lastip = ret_proxy
                    self.lasttime = t
                else:
                    ret_proxy = self.lastip
            request.meta["proxy"] = ret_proxy
            print("为%s添加代理%s" % (request.url, ret_proxy), end="")
        else:
            # 在进行url访问之前可以进行的操作, 更换UA请求头, 使用其他代理等
            pass

    # 可以拦截到response响应对象(拦截下载器传递给Spider的响应对象)
    def process_response(self, request, response, spider):
        """
        三个参数:
        # request: 响应对象所对应的请求对象
        # response: 拦截到的响应对象
        # spider: 爬虫文件中对应的爬虫类 WangyiSpider 的实例对象, 可以通过这个参数拿到 WangyiSpider 中的一些属性或方法
        """

        #  对页面响应体数据的篡改, 如果是每个模块的 url 请求, 则处理完数据并进行封装
        if spider.name in ["Hubei"]:
            spider.browser.get(url=request.url)
            spider.browser.refresh()
            time.sleep(0.5)
            row_response = spider.browser.page_source
            return HtmlResponse(
                url=spider.browser.current_url,
                body=row_response,
                encoding="utf8",
                request=request,
            )  # 参数url指当前浏览器访问的url(通过current_url方法获取), 在这里参数url也可以用request.url
            # 参数body指要封装成符合HTTP协议的源数据, 后两个参数可有可无
        else:
            return response  # 是原来的主页的响应对象

    # 请求出错了的操作, 比如ip被封了,可以在这里设置ip代理
    def process_exception(self, request, exception, spider):
        if spider.name in [
            "Central",
            "Xizang",
            "Tianjin",
            "Anhui",
            "Yunnan",
            "Shaanxi_shan",
            "Shandong",
        ]:
            print("添加代理开始")
            t = time.time()
            if t - self.lasttime <= 10:
                ret_proxy = self.lastip
            else:
                ret_proxy = self.get_proxy()
                if len(ret_proxy) > 0:
                    self.lastip = ret_proxy
                    self.lasttime = t
                else:
                    ret_proxy = self.lastip
            request.meta["proxy"] = ret_proxy
            print("为%s添加代理%s" % (request.url, ret_proxy), end="")
            return request
        else:
            return None

    def get_proxy(self):
        url = "https://api.xiaoxiangdaili.com/ip/get?appKey=660304975683276800&appSecret=GUCGRDQv&cnt=1&method=http&releaseAuto=false&wt=json"

        s = ""
        resp = requests.get(url)
        if resp.status_code == 200:
            x = json.loads(resp.text)
            s = "http://%s:%s" % (x["data"][0]["ip"], x["data"][0]["port"])
        return s
