import pickle
import os
import scrapy


class Shaanxi_shanSpider(scrapy.Spider):
    name = "Shaanxi_shan"
    if not os.path.exists("../../data/HTML_pk/%s" % name):
        os.makedirs("../../data/HTML_pk/%s" % name)
    if not os.path.exists("../../data/text/%s" % name):
        os.makedirs("../../data/text/%s" % name)

    def start_requests(self):
        url_dict = {
            "http://www.shaanxi.gov.cn/zfxxgk/fdzdgknr/zcwj/szfgz/index{0}.html": 11,
            "http://www.shaanxi.gov.cn/zfxxgk/fdzdgknr/zcwj/xzgfxwj/index{0}.html": 5,
            "http://www.shaanxi.gov.cn/zfxxgk/fdzdgknr/zcwj/szfwj/szf/index{0}.html": 70,
            "http://www.shaanxi.gov.cn/zfxxgk/fdzdgknr/zcwj/szfwj/szz/index{0}.html": 17,
            "http://www.shaanxi.gov.cn/zfxxgk/fdzdgknr/zcwj/szfwj/szrz/index{0}.html": 134,
            "http://www.shaanxi.gov.cn/zfxxgk/fdzdgknr/zcwj/szfwj/sztb/index{0}.html": 46,
            "http://www.shaanxi.gov.cn/zfxxgk/fdzdgknr/zcwj/szfwj/szh/index{0}.html": 56,
            "http://www.shaanxi.gov.cn/zfxxgk/fdzdgknr/zcwj/szfbgtwj/szbf/index{0}.html": 134,
            "http://www.shaanxi.gov.cn/zfxxgk/fdzdgknr/zcwj/szfbgtwj/szbz/index{0}.html": 6,
            "http://www.shaanxi.gov.cn/zfxxgk/fdzdgknr/zcwj/szfbgtwj/szbfmd/index{0}.html": 14,
        }
        # test_page = 2
        for url_base, max_page in url_dict.items():
            for i in range(max_page):
                page = "_%s" % i if i > 0 else ""
                yield scrapy.Request(url=url_base.format(page), callback=self.parse)

    def parse(self, response):
        detail_page_links = []
        for tr in response.css('ul[class="gov-item cf-otw"] li'):
            href = tr.css('div[class="a-news otw lf"] a::attr(href)').get()
            url = response.urljoin(href)
            UID = url.split("/")[-1].split(".")[0]

            detail_page_links.append(url)
            yield {
                "UID": UID,
                "title": tr.css('div[class="a-news otw lf"] a::attr(title)').get(),
                "date": tr.css('span[class="date rt"]::text').get().strip(),
                "FileNumber": tr.css('span[class="code-num otw lf"]::text')
                .get()
                .strip(),
                "text length": 0,
                "url": url,
                "crawl state": "half",
            }
        yield from response.follow_all(detail_page_links, callback=self.parse_content)

    def parse_content(self, response):
        UID = response.url.split("/")[-1].split(".")[0]

        paragraph_list = response.css("div#doc_left *::text").getall()
        if len(paragraph_list) == 0:
            paragraph_list = response.css("p *::text").getall()
        if len(paragraph_list) == 0:
            paragraph_list = response.css("*::text").getall()

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
