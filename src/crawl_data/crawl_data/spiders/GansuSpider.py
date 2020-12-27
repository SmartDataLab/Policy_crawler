import scrapy
import pickle
import os
import ast
from urllib import parse
from scrapy.selector import Selector

class GansuSpider(scrapy.Spider):
    name = "Gansu"
    if not os.path.exists('../../data/HTML_pk/%s' % name):
        os.makedirs('../../data/HTML_pk/%s' % name)
    if not os.path.exists('../../data/text/%s' % name):
        os.makedirs('../../data/text/%s' % name)
    def start_requests(self):
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/60.0",
            'Referer': "http://www.gansu.gov.cn/col/col4729/index.html",
            "Host": "www.gansu.gov.cn",
            "Origin":"http://www.gansu.gov.cn"
        }
        total_page = 9
        # total_page = 2
        url_base = "http://www.gansu.gov.cn/module/jslib/jquery/jpage/dataproxy.jsp?startrecord={0}&endrecord={1}&perpage=27&appid=1&webid=1&path=%2F&columnid=4729&sourceContentType=3&unitid=18064&webname=%E4%B8%AD%E5%9B%BD%C2%B7%E7%94%98%E8%82%83&permissiontype=0"
        for i in range(total_page):
            yield scrapy.Request(url=url_base.format(i*81+1,(i+1)*81),headers=headers, callback=self.parse)

    def parse(self,response):
        detail_page_links = []
        for table_text in ast.literal_eval(response.text[69:-1]):
            table = Selector(text=table_text)
            url = 'http://www.gansu.gov.cn/'+table.css('a::attr(href)').get()
            UID = url.split('/')[-1][:-5]
            detail_page_links.append(url)
            yield {
                'UID': UID,
                'title': table.css('a::attr(title)').get(),
                'date': table.css('span::text').get(),
                'url': url,
                'text length':0,
                'crawl state':'half'
            }
        yield from response.follow_all(detail_page_links, callback = self.parse_content)

    def parse_content(self, response):
        UID = response.url.split('/')[-1][:-5]
        paragraph_list = response.css('div#zoom p *::text').getall() 
        
        if len(paragraph_list) == 0:
            paragraph_list =  response.css('p *::text').getall() 
        length = len(''.join(paragraph_list))
        if length > 0:
            state = 'full'
            with open('../../data/HTML_pk/%s/%s.pkl' % (self.name,UID), 'wb') as f:
                pickle.dump(response.text,f)
            with open('../../data/text/%s/%s.txt' % (self.name,UID), 'w') as f:
                f.write('\n'.join(paragraph_list))
        else:
            state = 'empty'
        filenum = None
        if '号' in paragraph_list[0]:
            filenum = paragraph_list[0]
        return {
            'UID': UID,
            'mainText': paragraph_list,
            'FileNumber': filenum,
            'crawl state':state,
            'text length':length,
        }
