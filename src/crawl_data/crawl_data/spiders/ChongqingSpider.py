import scrapy
import pickle
import os


class ChongqingSpider(scrapy.Spider):
    name = "Chongqing"
    if not os.path.exists("../../data/HTML_pk/%s" % name):
        os.makedirs("../../data/HTML_pk/%s" % name)
    if not os.path.exists("../../data/text/%s" % name):
        os.makedirs("../../data/text/%s" % name)

    def start_requests(self):
        url_dict = {
            "http://www.cq.gov.cn/zwgk/fdzdgknr/lzyj/zfgz/zfgz_52609/index{0}.html": 12,
            "http://www.cq.gov.cn/zwgk/fdzdgknr/lzyj/xzgfxwj/szf_38655/index{0}.html": 23,
            "http://www.cq.gov.cn/zwgk/fdzdgknr/lzyj/xzgfxwj/szfbgt_38656/index{0}.html": 33,
            "http://www.cq.gov.cn/zwgk/fdzdgknr/lzyj/qtgw/index{0}.html": 34,
            "http://www.cq.gov.cn/zwgk/fdzdgknr/lzyj/rsrm/index{0}.html": 3,
        }
        for url_base, max_page in url_dict.items():
            for i in range(max_page):
                page = "_" + str(i) if i > 0 else ""
                yield scrapy.Request(url=url_base.format(page), callback=self.parse)

    def parse(self, response):
        detail_page_links = response.css("ul.list-cont li.w400 a::attr(href)").getall()
        release_inst_l = response.css("ul.list-cont li.w120::text").getall()
        title_l = response.css("ul.list-cont li.w400 a::text").getall()
        release_date_l = response.css("ul.list-cont li.w172::text").getall()
        date_l = response.css("ul.list-cont li.w110 span::text").getall()

        for i in range(len(detail_page_links)):
            href = detail_page_links[i]
            UID = href.split("/")[-1][:-5]
            yield {
                "UID": UID,
                "title": title_l[i],
                "date": date_l[i],
                "release_date": release_date_l[i],
                "release_inst": release_inst_l[i],
                "url": response.urljoin(href),
                "crawl state": "half",
                "text length": 0,
                "FileNumber": None,
            }
        yield from response.follow_all(detail_page_links, callback=self.parse_content)

    def parse_content(self, response):
        UID = response.url.split("/")[-1][:-5]
        doc_info_dict = {}
        td_list = response.css("table.gkxl-top td")
        for i in range(len(td_list) // 2):
            key = td_list[2 * i].css("::text").get()
            value = td_list[2 * i + 1].css("::text").get()
            doc_info_dict[key] = value
        FileNum = None
        if "文 号：" in doc_info_dict.keys():
            FileNum = doc_info_dict["文 号："]
        paragraph_list = response.css("div.gkxl-article p *::text").getall()
        if len(paragraph_list) == 0:
            paragraph_list = response.css("p *::text").getall()
        length = len("".join(paragraph_list))
        if length > 0:
            state = "full"
            with open("../../data/text/%s/%s.txt" % (self.name, UID), "w") as f:
                f.write("\n".join(paragraph_list))
            with open("../../data/HTML_pk/%s/%s.pkl" % (self.name, UID), "wb") as f:
                pickle.dump(response.text, f)
        else:
            state = "empty"
        return {
            "UID": UID,
            "doc_info_dict": doc_info_dict,
            "mainText": paragraph_list,
            "url": response.url,
            "crawl state": state,
            "text length": length,
            "FileNumber": FileNum,
        }
