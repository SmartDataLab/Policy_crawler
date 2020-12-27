import scrapy
import pickle
import os
import json
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

options = Options()
options.headless = True


class TianjinSpider(scrapy.Spider):
    name = "Tianjin"
    if not os.path.exists("../../data/HTML_pk/%s" % name):
        os.makedirs("../../data/HTML_pk/%s" % name)
    if not os.path.exists("../../data/text/%s" % name):
        os.makedirs("../../data/text/%s" % name)

    def __init__(self):
        self.browser = webdriver.Firefox(options=options)
        self.browser.get("http://gk.tj.gov.cn/")
        super().__init__()

    def close(self, spider):
        self.browser.quit()

    def start_requests(self):
        total_page = 1000
        url_base = "http://www.tj.gov.cn/igs/front/search/list.html?index=zcwj-index-200424&type=zcfg&filter[AVAILABLE]=true&siteId=&pageSize=10&pageNumber={0}&filter%5BFWJG_name%5D=&filter%5BBT%2CZW%2CFWZH-or%5D=&orderProperty=FBRQ&orderDirection=desc&filter%5BWZFL_name%5D=&filter%5BFBRQ-lte%5D=&filter%5BFBRQ-gte%5D="
        for i in range(total_page):
            req = scrapy.Request(url=url_base.format(str(i + 1)), callback=self.parse)
            req.meta["dont_redirect"] = True
            req.meta["handle_httpstatus_list"] = [302]
            yield req

    def parse(self, response):
        for piece in json.loads(response.text)["page"]["content"]:
            piece["url"] = piece["DOCPUBURL"]
            piece["UID"] = piece["url"].split("/")[-1].split(".")[0]
            piece["title"] = piece["BT"]
            piece["date"] = piece["FBRQ"].split("T")[0]
            piece["mainText"] = piece["ZW"]
            piece["crawl state"] = "full"
            piece["text length"] = 0
            piece["FileNumber"] = piece["FWZH"]
            yield piece
