import scrapy
import pickle
import os
import ast
from urllib import parse
from scrapy.selector import Selector


class HenanSpider(scrapy.Spider):
    name = "Henan"
    if not os.path.exists("../../data/HTML_pk/%s" % name):
        os.makedirs("../../data/HTML_pk/%s" % name)
    if not os.path.exists("../../data/text/%s" % name):
        os.makedirs("../../data/text/%s" % name)

    def start_requests(self):
        url_dict = {
            "https://www.henan.gov.cn/zwgk/fgwj/szfl/index{0}.html": 5,
            "https://www.henan.gov.cn/zwgk/fgwj/yz/index{0}.html": 46,
            "https://www.henan.gov.cn/zwgk/fgwj/yzb/index{0}.html": 82,
            "https://www.henan.gov.cn/zwgk/fgwj/yzr/index{0}.html": 98,
        }
        # test_page = 2
        for url_base, max_page in url_dict.items():
            for i in range(max_page):
                page = "_%s" % i if i > 0 else ""
                yield scrapy.Request(url=url_base.format(page), callback=self.parse)

    def parse(self, response):
        detail_page_links = []
        for a in response.css('div[class="con-box"] li'):
            url = response.urljoin(a.css("a::attr(href)").get())
            detail_page_links.append(url)
            UID = url.split("/")[-1].split(".")[0]
            title = a.css("a::text").get()
            file_num = a.css("p::text").get()
            date = a.css("span::text").get()
            yield {
                "UID": UID,
                "title": title,
                "date": date,
                "FileNumber": file_num,
                "url": url,
                "crawl state": "half",
                "text length": 0,
            }
        yield from response.follow_all(detail_page_links, callback=self.parse_content)

    def parse_content(self, response):
        UID = response.url.split("/")[-1].split(".")[0]
        paragraph_list = response.css('div[class="content"] \*::text').getall()
        if len(paragraph_list) == 0:
            paragraph_list = response.css("table p *::text").getall()
        if len(paragraph_list) == 0:
            paragraph_list = response.css("p *::text").getall()
        length = len("".join(paragraph_list))
        if length > 0:
            with open("../../data/text/%s/%s.txt" % (self.name, UID), "w") as f:
                f.write("\n".join(paragraph_list))
            with open("../../data/HTML_pk/%s/%s.pkl" % (self.name, UID), "wb") as f:
                pickle.dump(response.text, f)
            state = "full"
        else:
            state = "empty"
        return {
            "UID": UID,
            "mainText": paragraph_list,
            "crawl state": state,
            "text length": length,
        }
