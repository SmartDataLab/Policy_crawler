import scrapy
import pickle
import os
import ast
from urllib import parse
from scrapy.selector import Selector


class YunnanSpider(scrapy.Spider):
    name = "Yunnan"
    if not os.path.exists("../../data/HTML_pk/%s" % name):
        os.makedirs("../../data/HTML_pk/%s" % name)
    if not os.path.exists("../../data/text/%s" % name):
        os.makedirs("../../data/text/%s" % name)

    def start_requests(self):
        url_dict = {
            "http://www.yn.gov.cn/zwgk/zcwj/szfl/index{0}.html": 5,
            "http://www.yn.gov.cn/zwgk/zcwj/yzf/index{0}.html": 42,
            "http://www.yn.gov.cn/zwgk/zcwj/yzg/index{0}.html": 1,
            "http://www.yn.gov.cn/zwgk/zcwj/yzh/index{0}.html": 7,
            "http://www.yn.gov.cn/zwgk/zcwj/yunzf/index{0}.html": 12,
            "http://www.yn.gov.cn/zwgk/zcwj/yzr/index{0}.html": 42,
            "http://www.yn.gov.cn/zwgk/zcwj/yfmd/index{0}.html": 1,
            "http://www.yn.gov.cn/zwgk/zcwj/yzfb/index{0}.html": 42,
            "http://www.yn.gov.cn/zwgk/zcwj/yzbg/index{0}.html": 2,
            "http://www.yn.gov.cn/zwgk/zcwj/yzbh/index{0}.html": 28,
            "http://www.yn.gov.cn/zwgk/zcwj/yzbmd/index{0}.html": 5,
            "http://www.yn.gov.cn/zwgk/zcwj/qtwj/index{0}.html": 5,
        }
        for url_base, max_page in url_dict.items():
            for i in range(max_page):
                page = "_" + str(i) if i > 0 else ""
                yield scrapy.Request(url=url_base.format(page), callback=self.parse)

    def parse(self, response):
        detail_page_links = []
        for ul in response.css("tbody tr")[1:]:
            url = response.urljoin(ul.css("td")[1].css("a::attr(href)").get())
            UID = url.split("/")[-1].split(".")[0]

            detail_page_links.append(url)
            date = ul.css("td")[2].css("::text").get()

            yield {
                "UID": UID,
                "title": ul.css("td")[1].css("a::text").get(),
                "date": date,
                "FileNumber": ul.css("td")[0].css("::text").get(),
                "url": url,
                "text length": 0,
                "crawl state": "half",
            }
        yield from response.follow_all(detail_page_links, callback=self.parse_content)

    def parse_content(self, response):
        UID = response.url.split("/")[-1].split(".")[0]
        paragraph_list = response.css('div[class="arti"] \*::text').getall()
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
