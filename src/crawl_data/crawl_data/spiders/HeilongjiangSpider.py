import scrapy
import pickle
import os
import ast
from urllib import parse
from scrapy.selector import Selector
import json
import time


class HeilongjiangSpider(scrapy.Spider):
    name = "Heilongjiang"
    if not os.path.exists("../../data/HTML_pk/%s" % name):
        os.makedirs("../../data/HTML_pk/%s" % name)
    if not os.path.exists("../../data/text/%s" % name):
        os.makedirs("../../data/text/%s" % name)

    def start_requests(self):
        total_page = 192
        url_base = "http://zwgk.hlj.gov.cn/zwgk/publicInfo/searchFile?chanPath=2,&chanP=2%2C&page={0}&limit=10&total=0"
        for i in range(total_page):
            yield scrapy.Request(url=url_base.format(str(i + 1)), callback=self.parse)

    def parse(self, response):
        detail_page_links = []
        detail_url_base = "http://zwgk.hlj.gov.cn/zwgk/publicInfo/detail?id={0}"
        json_dict = json.loads(response.text)
        for piece_dict in json_dict["data"]["records"]:
            UID = piece_dict["id"]
            piece_dict["UID"] = str(UID)
            local_time = time.localtime(piece_dict["publishTime"])
            piece_dict["date"] = time.strftime("%Y-%m-%d", local_time)

            detail_page_links.append(detail_url_base.format(UID))
            piece_dict["crawl state"] = "half"
            piece_dict["text length"] = 0
            yield piece_dict
        yield from response.follow_all(detail_page_links, callback=self.parse_content)

    def parse_content(self, response):
        UID = response.url.split("=")[-1]
        paragraph_list = response.css("div[class=zwnr] \*::text").getall()
        # new_text = parse.unquote_plus(response.text[7:-6])
        # for escape_text in Selector(text=new_text).css("div.zwnr *::text").getall():
        #     paragraph = (
        #         escape_text.replace("%", "\\").encode("utf-8").decode("unicode_escape")
        #     )
        #     paragraph_list.append(paragraph)
        length = len("".join(paragraph_list))
        if length > 0:
            state = "full"
            with open("../../data/HTML_pk/%s/%s.pkl" % (self.name, UID), "wb") as f:
                pickle.dump(response.text, f)
            with open("../../data/text/%s/%s.txt" % (self.name, UID), "w") as f:
                f.write("\n".join(paragraph_list))
        else:
            state = "empty"
        return {
            "UID": UID,
            "mainText": paragraph_list,
            "crawl state": state,
            "text length": length,
        }
