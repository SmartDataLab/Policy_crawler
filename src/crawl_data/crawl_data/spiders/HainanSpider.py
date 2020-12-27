import scrapy
import json
import pickle
import os
import ast
from urllib import parse
from scrapy.selector import Selector

class HainanSpider(scrapy.Spider):
    name = "Hainan"
    if not os.path.exists('../../data/HTML_pk/%s' % name):
        os.makedirs('../../data/HTML_pk/%s' % name)
    if not os.path.exists('../../data/text/%s' % name):
        os.makedirs('../../data/text/%s' % name)
    def start_requests(self):
        total_page = 486
        # total_page = 3 
        url_base = 'http://www.hainan.gov.cn/u/search/wjk/rs?keywords=&docYear=&docName=&fwzh=&column=undefined&curPage={0}&PageSize=15'
        for i in range(total_page):
            yield scrapy.Request(url=url_base.format(i+1), callback=self.parse)

    def parse(self,response):
        detail_page_links = []
        for item in json.loads(response.text)['page']['list']:
            UID = item['url'].split('/')[-1][:-6]
            item['url'] = response.urljoin(item['url'])
            item['UID'] = UID
            date = item['pubDate']
            if date and len(date) > 10:
                date = date[:10]
            item['date'] = date
            item['FileNumber'] = item['c_wjbh']
            if '?' not in UID:
                detail_page_links.append(item['url'])
            item['crawl state'] = 'half'
            item['text length'] = 0 
            yield item
        yield from response.follow_all(detail_page_links, callback = self.parse_content)

    def parse_content(self, response):
        UID = response.url.split('/')[-1][:-6]
        paragraph_list = response.css('div#zoom p *::text').getall()         
        attachment_link = response.css('div#zoom p a::attr(href)').getall()         
        if len(paragraph_list) == 0:
            paragraph_list = response.css('table p *::text').getall()
        if len(paragraph_list) == 0:
            paragraph_list =  response.css('p *::text').getall() 
        length = len(''.join(paragraph_list))
        if length > 0:
            with open('../../data/text/%s/%s.txt' % (self.name,UID), 'w') as f:
                f.write('\n'.join(paragraph_list))
            with open('../../data/HTML_pk/%s/%s.pkl' % (self.name,UID), 'wb') as f:
                pickle.dump(response.text,f)
            state = 'full'
        else:
            state = 'empty'
        return {
            'UID': UID,
            'mainText': paragraph_list,
            'attachment_link': attachment_link,
            'crawl state':state,
            'text length':length,
        }
