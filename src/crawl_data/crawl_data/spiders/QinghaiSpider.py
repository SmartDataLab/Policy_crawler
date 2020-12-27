import scrapy
import pickle
import os
import ast
from urllib import parse
from scrapy.selector import Selector


class QinghaiSpider(scrapy.Spider):
    name = "Qinghai"
    if not os.path.exists("../../data/HTML_pk/%s" % name):
        os.makedirs("../../data/HTML_pk/%s" % name)
    if not os.path.exists("../../data/text/%s" % name):
        os.makedirs("../../data/text/%s" % name)

    def start_requests(self):
        total_page = 59
        # total_page = 3
        url_base = "http://zwgk.qh.gov.cn/xxgk/fd/zfwj/index{0}.html"
        for i in range(total_page):
            page = "_" + str(i) if i > 0 else ""
            yield scrapy.Request(url=url_base.format(page), callback=self.parse)

    def parse(self, response):
        detail_page_links = []
        for li in response.css('table[class="zctb"] tr')[1:]:
            url = li.css("td")[0].css("a::attr(href)").get()
            UID = url.split("/")[-1].split(".")[0]
            detail_page_links.append(url)
            date = UID.split("_")[0][1:]
            date = "-".join([date[:4], date[4:6], date[6:8]])
            yield {
                "UID": UID,
                "title": "".join(li.css("td")[0].css("a \*::text").getall()),
                "date": date,
                "FileNumber": li.css("td")[1].css("::text").get(),
                "text length": 0,
                "url": url,
                "crawl state": "half",
            }
        yield from response.follow_all(detail_page_links, callback=self.parse_content)

    def parse_content(self, response):
        UID = response.url.split("/")[-1].split(".")[0]

        paragraph_list = response.css("div#contentlf \*::text").getall()
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
            "crawl state": state,
            "text length": length,
        }
