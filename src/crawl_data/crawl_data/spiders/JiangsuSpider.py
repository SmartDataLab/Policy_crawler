import scrapy
import pickle
import os
import ast
from urllib import parse
from scrapy.selector import Selector

class JiangsuSpider(scrapy.Spider):
    name = "Jiangsu"
    if not os.path.exists('../../data/HTML_pk/%s' % name):
        os.makedirs('../../data/HTML_pk/%s' % name)
    if not os.path.exists('../../data/text/%s' % name):
        os.makedirs('../../data/text/%s' % name)
    def start_requests(self):
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/60.0",
            'Referer': "http://www.jiangsu.gov.cn/col/col76841/index.html?uid=297589&pageNum=3",
            "Host": "www.jiangsu.gov.cn",
            "Origin":"http://www.jiangsu.gov.cn"
        }

        total_page = 63
        # total_page = 8
        # url_base = "http://www.jiangsu.gov.cn/module/web/jpage/dataproxy.jsp?col=1&appid=1&webid=1&path=%2F&columnid=76841&sourceContentType=1&unitid=297589&webname=%E6%B1%9F%E8%8B%8F%E7%9C%81%E4%BA%BA%E6%B0%91%E6%94%BF%E5%BA%9C&permissiontype=0"
        # url_base = 'http://www.jiangsu.gov.cn/col/col76841/index.html?uid=297589&pageNum={0}&col=1&appid=1&webid=1&path=%2F&columnid=76841&sourceContentType=1&unitid=297589&webname=%E6%B1%9F%E8%8B%8F%E7%9C%81%E4%BA%BA%E6%B0%91%E6%94%BF%E5%BA%9C&permissiontype=0'
        url_base = 'http://www.jiangsu.gov.cn/col/col76841/index.html?uid=297589&pageNum={0}&col=1&appid=1&webid=1&path=%2F&columnid=76841&sourceContentType=1&unitid=297589&webname=%C3%83%C2%A6%C3%82%C2%B1%C3%82%C2%9F%C3%83%C2%A8%C3%82%C2%8B%C3%82%C2%8F%C3%83%C2%A7%C3%82%C2%9C%C3%82%C2%81%C3%83%C2%A4%C3%82%C2%BA%C3%82%C2%BA%C3%83%C2%A6%C3%82%C2%B0%C3%82%C2%91%C3%83%C2%A6%C3%82%C2%94%C3%82%C2%BF%C3%83%C2%A5%C3%82%C2%BA%C3%82%C2%9C&permissiontype=0'
        url_base = 'http://www.jiangsu.gov.cn/module/web/jpage/dataproxy.jsp?startrecord={0}&endrecord={0}&perpage=25&col=1&appid=1&webid=1&path=%2F&columnid=76841&sourceContentType=1&unitid=297589&webname=%E6%B1%9F%E8%8B%8F%E7%9C%81%E4%BA%BA%E6%B0%91%E6%94%BF%E5%BA%9C&permissiontype=0'
        for i in range(total_page):
            yield scrapy.Request(url=url_base.format(i*75+1,i*75+75),headers=headers, callback=self.parse)

    def parse(self,response):
        detail_page_links = []
        for html_text in response.css('record *::text').getall():
            record = Selector(text = html_text)
            url = record.css('a::attr(href)').get()
            UID = url.split('/')[-1][:-5]+'_'+url.split('/')[-4]+url.split('/')[-3]+url.split('/')[-2]
            detail_page_links.append(url)
            yield {
                'UID': UID,
                'title': record.css('a::attr(title)').get(),
                'date': record.css('b::text').get(),
                'FileNumber':None,
                'text length':0,
                'url': url,
                'crawl state':'half'
            }
        for url in detail_page_links:
            yield scrapy.Request(url=url, callback = self.parse_content)

    def parse_content(self, response):
        url = response.url
        UID = url.split('/')[-1][:-5]+'_'+url.split('/')[-4]+url.split('/')[-3]+url.split('/')[-2]
        doc_info_dict = {}
        count = 0
        for td in response.css('tbody td'):
            if count % 2 == 0:
                key = td.css("::text").get()
            else:
                value = td.css("::text").get()
                doc_info_dict[key] = value
            count+=1
        file_num = doc_info_dict['文\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0号'] if '文\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0号' in doc_info_dict.keys() else  None
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
        return {
            'UID': UID,
            'mainText': paragraph_list,
            'FileNumber': file_num,
            'crawl state':state,
            'text length':length,
        }
