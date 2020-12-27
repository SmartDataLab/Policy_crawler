import scrapy
import pickle
import os


class ShanghaiSpider(scrapy.Spider):
    name = "Shanghai"
    if not os.path.exists("../../data/HTML_pk/%s" % name):
        os.makedirs("../../data/HTML_pk/%s" % name)
    if not os.path.exists("../../data/text/%s" % name):
        os.makedirs("../../data/text/%s" % name)

    def start_requests(self):
        total_page = 298
        url_base = "http://service.shanghai.gov.cn/XingZhengWenDangKuJyh/XZGFList.aspx?testpara=0&kw=&issueDate_userprop8=&status=1&departid=0&wenhao=&issueDate_userprop8_end=&excuteDate=&excuteDate_end=&closeDate=&closeDate_end=&departtypename=0&typename=%E5%85%A8%E9%83%A8&zhutitypename=&zhuti=&currentPage={0}&pagesize=10"
        for i in range(total_page):
            yield scrapy.Request(url=url_base.format(str(i + 1)), callback=self.parse)

    def parse(self, response):
        detail_page_links = []
        for piece in response.css('table[class="table table-list"] tr')[1:]:
            url = response.urljoin(piece.css("td a::attr(href)").get())
            UID = url.split("=")[-1]

            detail_page_links.append(url)

            date = piece.css("td")[2].css("::text").get()

            yield {
                "UID": UID,
                "title": piece.css("td a::attr(title)").get(),
                "date": date,
                "url": url,
                "text length": 0,
                "crawl state": "half",
                "FileNumber": piece.css("td")[1].css("::text").get(),
            }
        yield from response.follow_all(detail_page_links, callback=self.parse_content)

    def parse_content(self, response):
        UID = response.url.split("=")[-1]

        paragraph_list = response.css("div#ivs_content *::text").getall()

        if len(paragraph_list) == 0:
            paragraph_list = response.css("p *::text").getall()

        if len(paragraph_list) > 0 and "号" in paragraph_list[0]:
            Filenum = paragraph_list[0]
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
