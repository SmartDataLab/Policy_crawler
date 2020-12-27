import scrapy
import pickle
import os
import ast
import json
from urllib import parse
from scrapy.selector import Selector

class FujianSpider(scrapy.Spider):
    name = "Fujian"
    if not os.path.exists('../../data/HTML_pk/%s' % name):
        os.makedirs('../../data/HTML_pk/%s' % name)
    if not os.path.exists('../../data/text/%s' % name):
        os.makedirs('../../data/text/%s' % name)
    def start_requests(self):
        total_page = 655
        # total_page = 3
        url_base = 'http://www.fujian.gov.cn/was5/web/search?channelid=229105&templet=docs.jsp&sortfield=-pubdate&classsql=chnlid%3E22054*chnlid%3C22084&prepage=10&page={0}'
        for i in range(total_page):
            yield scrapy.Request(url=url_base.format(str(i+1)), callback=self.parse)

    def parse(self,response):
        detail_page_links = []
        raw = response.text
        raw = raw.replace('\r','')
        raw = raw.replace('\n','')
        d = json.loads(raw)
        for piece_dict in d['docs']:
            url = piece_dict['url']
            UID = url.split('/')[-1][:-4]
            title = piece_dict['title']
            if '?' not in UID:
                detail_page_links.append(url)
            if 'fileno' in piece_dict.keys():
                file_num = piece_dict['fileno']
            else:
                break
            date = piece_dict['time']
            if date and len(date) > 10:
                date = date[:10]
            yield {
                'UID':UID,
                'title':title,
                'url':url,
                'date':date,
                'FileNumber':file_num,
                'text length':0,
                'crawl state': 'half'
            }
        yield from response.follow_all(detail_page_links, callback = self.parse_content)

    def parse_content(self, response):
        UID = response.url.split('/')[-1][:-4]
        paragraph_list = response.css('div.xl-bk p *::text').getall() 
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
