import scrapy
import pickle
import os
import ast
from urllib import parse
from scrapy.selector import Selector

class NingxiaSpider(scrapy.Spider):
    name = "Ningxia"
    if not os.path.exists('../../data/HTML_pk/%s' % name):
        os.makedirs('../../data/HTML_pk/%s' % name)
    if not os.path.exists('../../data/text/%s' % name):
        os.makedirs('../../data/text/%s' % name)
    def start_requests(self):
        total_page = 48 
        # total_page = 3 
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/60.0",
            'Referer': "http://www.nx.gov.cn/zwgk/qzfwj/",
            "Host": "www.nx.gov.cn",
            "Origin":"http://www.nx.gov.cn"
        }
        url_base = 'http://www.nx.gov.cn/zwgk/qzfwj/list{0}.html'
        for i in range(total_page):
            page = '_'+ str(i) if i > 0 else ''
            yield scrapy.Request(url=url_base.format(page),headers=headers, callback=self.parse)

    def parse(self,response):
        detail_page_links = []
        for li in response.css('ul.nx-list li'):
            url = response.urljoin(li.css('a::attr(href)').get())
            UID = url.split('/')[-1][:-5]
            if '?' not in UID:
                detail_page_links.append(url)
            FileNumber = None
            doc_info_dict = {}
            for p in li.css('div.nx-conmtab p'):
                key = p.css('span.tt::text').get()
                value = p.css('span.value::text').get()
                doc_info_dict[key] = value
                if key == '发文字号：':
                    FileNumber = value
            yield {
                'UID': UID,
                'title': li.css('a::attr(title)').get(),
                'date': li.css('span.date::text').get(),
                'FileNumber': FileNumber,
                'doc_info_dict':doc_info_dict,
                'text length':0,
                'url': url,
                'crawl state':'half'
            }
        yield from response.follow_all(detail_page_links, callback = self.parse_content)

    def parse_content(self, response):
        UID = response.url.split('/')[-1][:-5]
        paragraph_list = response.css('div.view p *::text').getall()
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
        return {
            'UID': UID,
            'mainText': paragraph_list,
            'crawl state':state,
            'text length':length,
        }
