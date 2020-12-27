import scrapy
import pickle
import os
import ast
from urllib import parse
from scrapy.selector import Selector
import json


class GuangxiSpider(scrapy.Spider):
    name = "Guangxi"
    if not os.path.exists("../../data/HTML_pk/%s" % name):
        os.makedirs("../../data/HTML_pk/%s" % name)
    if not os.path.exists("../../data/text/%s" % name):
        os.makedirs("../../data/text/%s" % name)

    def start_requests(self):
        total_page = 163
        # total_page = 3
        url_base = "http://www.gxzf.gov.cn/igs/front/search/list.html?index=file2-index-alias&type=governmentdocuments&pageNumber={0}&pageSize=10&filter[AVAILABLE]=true&filter[fileNum-like]=&filter[Effectivestate]=&filter[fileYear]=&filter[fileYear-lte]=&filter[FileName,DOCCONTENT,fileNum-or]=&siteId=14&filter[SITEID]=3&orderProperty=PUBDATE&orderDirection=desc"
        for i in range(total_page):
            yield scrapy.Request(url=url_base.format(i + 1), callback=self.parse)

    def parse(self, response):
        detail_page_links = []
        for piece_dict in json.loads(response.text)["page"]["content"]:

            piece_dict["UID"] = piece_dict["_id"]
            piece_dict["title"] = piece_dict["DOCTITLE"]
            piece_dict["date"] = piece_dict["PUBDATE"].split("T")[0]
            piece_dict["mainText"] = [piece_dict["DOCCONTENT"]]
            piece_dict["FileNumber"] = piece_dict["CHNLDESC"] + piece_dict["IdxID"]
            piece_dict["url"] = piece_dict["DOCPUBURL"]
            piece_dict["text length"] = len(piece_dict["DOCCONTENT"])
            piece_dict["crawl state"] = "full"

            yield piece_dict
        yield from response.follow_all(detail_page_links)
