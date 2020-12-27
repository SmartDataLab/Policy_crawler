import scrapy
import pickle
import os
import ast
from urllib import parse
from scrapy.selector import Selector

class ZhejiangSpider(scrapy.Spider):
    name = "Zhejiang"
    if not os.path.exists('../../data/HTML_pk/%s' % name):
        os.makedirs('../../data/HTML_pk/%s' % name)
    if not os.path.exists('../../data/text/%s' % name):
        os.makedirs('../../data/text/%s' % name)
    def start_requests(self):
        total_page = 509
        # total_page = 3 
        url_base = 'http://www.zj.gov.cn/module/xxgk/search.jsp?infotypeId=&jdid=3096&area=000014349&divid=div1551294&vc_title=&vc_number=&sortfield=,compaltedate:0&currpage={0}&vc_filenumber=&vc_all=&texttype=0&fbtime=&texttype=0&fbtime=&vc_all=&vc_filenumber=&vc_title=&vc_number=&currpage=3&sortfield=,compaltedate:0'
        for i in range(total_page):
            yield scrapy.Request(url=url_base.format(i+1), callback=self.parse)

    def parse(self,response):
        detail_page_links = []
        for tr in response.css('tr')[4:-2]:
            url = response.urljoin(tr.css('a::attr(href)').get())
            UID = url.split('/')[-1][:-5]
            if '?' not in UID:
                detail_page_links.append(url)
            yield {
                'UID': UID,
                'title': tr.css('a::attr(mc)').get(),
                'date': tr.css('a::attr(rq)').get(),
                'FileNumber':tr.css('a::attr(wh)').get(),
                'url': url,
                'crawl state':'half',
                'text length':0,
            }
        yield from response.follow_all(detail_page_links, callback = self.parse_content)

    def parse_content(self, response):
        UID = response.url.split('/')[-1][:-5]
        paragraph_list = response.css('div.bt_content p *::text').getall()          
        if len(paragraph_list) == 0:
            paragraph_list =response.css('div#zoom p *::text').getall()           
        if len(paragraph_list) == 0:
            paragraph_list =  response.css('p *::text').getall() 
        if len(paragraph_list) == 0:
            paragraph_list =  response.css('tbody *::text').getall() 
        length = len(''.join(paragraph_list))
        if length > 0:
            with open('../../data/HTML_pk/%s/%s.pkl' % (self.name,UID), 'wb') as f:
                pickle.dump(response.text,f)
            with open('../../data/text/%s/%s.txt' % (self.name,UID), 'w') as f:
                f.write('\n'.join(paragraph_list))
            return {
                'UID': UID,
                'mainText': paragraph_list,
                'crawl state':'full',
                'text length':length,
            }
        else:
            return {
                'UID': UID,
                'mainText': paragraph_list,
                'crawl state':'empty',
                'text length':0,
            }
