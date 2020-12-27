import scrapy
import pickle
import os
import ast
from urllib import parse
from scrapy.selector import Selector

class XizangSpider(scrapy.Spider):
    name = "Xizang"
    if not os.path.exists('../../data/HTML_pk/%s' % name):
        os.makedirs('../../data/HTML_pk/%s' % name)
    if not os.path.exists('../../data/text/%s' % name):
        os.makedirs('../../data/text/%s' % name)
    def start_requests(self):
        # total_page = 3
        total_page = 54
        url_base = 'http://www.xizang.gov.cn/zwgk/xxfb/gsgg_428/index{0}.html'
        for i in range(total_page):
            page = '_'+ str(i+1) if i > 0 else ''
            yield scrapy.Request(url=url_base.format(page), callback=self.parse)

    def parse(self,response):
        detail_page_links = []
        for li in response.css('ul.zwyw_list li'):
            url = response.urljoin(li.css('a::attr(href)').get())
            UID = url.split('/')[-1][:-5]
            if '?' not in UID:
                detail_page_links.append(url)
            yield {
                'UID': UID,
                'title': li.css('a::text').get(),
                'date': li.css('span::text').get(),
                'FileNumber':None,
                'url': url,
                'text length':0,
                'crawl state':'half'
            }
        yield from response.follow_all(detail_page_links, callback = self.parse_content)

    def parse_content(self, response):
        UID = response.url.split('/')[-1][:-5]
        doc_info_dict = {}
        th_list = response.css('table.table tr td.th')
        td_list = response.css('table.table tr td.td')
        for i in range(len(th_list)):
            key = th_list[i].css('::text').get()
            value = td_list[i].css('::text').get()
            doc_info_dict[key] = value
        File_num = None
        if '文 \xa0\xa0\xa0\xa0 号' in doc_info_dict.keys():
            File_num = doc_info_dict['文 \xa0\xa0\xa0\xa0 号']
        paragraph_list = response.css('div.view *::text').getall()
        if len(paragraph_list) == 0:
            paragraph_list = response.css('div *::text').getall()
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
            'FileNumber':File_num,
            'mainText': paragraph_list,
            'doc_info_dict':doc_info_dict,
            'crawl state':state,
            'text length':length,
        }
