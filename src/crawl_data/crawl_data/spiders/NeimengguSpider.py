import scrapy
import pickle
import os


class NeimengguSpider(scrapy.Spider):
    name = "Neimenggu"
    if not os.path.exists("../../data/HTML_pk/%s" % name):
        os.makedirs("../../data/HTML_pk/%s" % name)
    if not os.path.exists("../../data/text/%s" % name):
        os.makedirs("../../data/text/%s" % name)

    def start_requests(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/60.0",
            "Referer": "http://www.nmg.gov.cn/col/col1686/index.html",
            "Host": "www.nmg.gov.cn",
            "Origin": "http://www.nmg.gov.cn",
        }
        url_dict = {
            "http://www.nmg.gov.cn/zwgk/zfxxgk/zfxxgkml/gzxzgfxwj/xzgfxwj/index{0}.html": 71,
            "http://www.nmg.gov.cn/zwgk/zfxxgk/zfxxgkml/zzqzfjbgtwj/index{0}.html": 152,
        }
        for url_base, max_page in url_dict.items():
            for i in range(max_page):
                page = "_" + str(i) if i > 0 else ""
                yield scrapy.Request(url=url_base.format(page), callback=self.parse)

    def parse(self, response):
        detail_page_links = []

        for piece in response.css("tbody tr"):
            url = piece.css("td")[1].css("a::attr(href)").get()
            UID = url.split("/")[-1].split(".")[0]

            detail_page_links.append(url)
            yield {
                "UID": UID,
                "title": piece.css("td")[1].css("a::text").get(),
                "date": piece.css("td")[-1].css("::text").get(),
                "FileNumber": piece.css("td")[-3].css("::text").get(),
                "text length": 0,
                "url": url,
                "crawl state": "half",
            }
        yield from response.follow_all(detail_page_links, callback=self.parse_content)

    def parse_content(self, response):
        UID = response.url.split("/")[-1].split(".")[0]
        paragraph_list = response.css(
            'div[class="view TRS_UEDITOR trs_paper_default trs_external"] \*::text'
        ).getall()

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
