import scrapy
import pickle
import os
import ast
from urllib import parse
from scrapy.selector import Selector


class SichuanSpider(scrapy.Spider):
    name = "Sichuan"
    if not os.path.exists("../../data/HTML_pk/%s" % name):
        os.makedirs("../../data/HTML_pk/%s" % name)
    if not os.path.exists("../../data/text/%s" % name):
        os.makedirs("../../data/text/%s" % name)

    def start_requests(self):
        url_dict = {
            "http://www.sc.gov.cn/10462/c102914/list_ft{0}.shtml": 7,
            "http://www.sc.gov.cn/10462/c103043/stt_list{0}.shtml": 4,
            "http://www.sc.gov.cn/10462/c103044/stt_list{0}.shtml": 14,
            "http://www.sc.gov.cn/10462/c103045/stt_list{0}.shtml": 15,
            "http://www.sc.gov.cn/10462/c103046/stt_list{0}.shtml": 15,
            "http://www.sc.gov.cn/10462/c103047/stt_list{0}.shtml": 15,
            "http://www.sc.gov.cn/10462/c103048/stt_list{0}.shtml": 2,
        }
        # test_page = 1
        for url_base, max_page in url_dict.items():
            for i in range(max_page):
                page = "_" + str(i + 1) if i > 0 else ""
                yield scrapy.Request(url=url_base.format(page), callback=self.parse)

    def parse(self, response):
        detail_page_links = []
        for tr in response.css("div#content table#dash-table tr"):
            url = response.urljoin(tr.css("td")[1].css("a::attr(href)").get())
            UID = url.split("/")[-1].split(".")[0]
            if "?" not in UID:
                detail_page_links.append(url)

            yield {
                "UID": UID,
                "title": tr.css("td")[1].css("a::attr(title)").get(),
                "date": None,
                "FileNumber": None,
                "text length": 0,
                "url": url,
                "crawl state": "half",
            }
        yield from response.follow_all(detail_page_links, callback=self.parse_content)

    def parse_content(self, response):
        UID = response.url.split("/")[-1].split(".")[0]
        paragraph_list = response.css("td[class=contText] \*::text").getall()
        attachment_link = []
        filenumber = (
            response.css('td[bgcolor="#fbfbfb"] tr')[1]
            .css("td")[3]
            .css("\*::text")
            .get()
            .strip()
        )
        date = (
            response.css('td[bgcolor="#fbfbfb"] tr')[1]
            .css("td")[1]
            .css("\*::text")
            .get()
            .strip()
        )

        if len(paragraph_list) == 0:
            paragraph_list = response.css("p *::text").getall()
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
            "attachment_link": attachment_link,
            "crawl state": state,
            "FileNumber": filenumber,
            "date": date,
            "text length": length,
        }
