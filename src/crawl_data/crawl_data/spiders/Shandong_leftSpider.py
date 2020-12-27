import scrapy
import pickle
import os
import ast
from urllib import parse
import pandas as pd
from scrapy.selector import Selector

class Shandong_leftSpider(scrapy.Spider):
    name = "Shandong_left"
    if not os.path.exists('../../data/HTML_pk/%s' % name):
        os.makedirs('../../data/HTML_pk/%s' % name)
    if not os.path.exists('../../data/text/%s' % name):
        os.makedirs('../../data/text/%s' % name)
    def start_requests(self):
        yield scrapy.Request('http://www.shandong.gov.cn',callback=self.parse)

    def parse(self,response):
        detail_page_links = []
        df = pd.read_csv('../../data/empty/Shandong_empty_list.csv')     
        for i in range(len(df)):
            UID = str(df.loc[i,'UID'])
            if '?' not in UID:
                title = df.loc[i,'title']
                date = df.loc[i,'date']
                url = df.loc[i,'url']
                detail_page_links.append(url)
                yield {
                        'UID': UID,
                        'title': title,
                        'date': date,
                        'FileNumber':None,
                        'text length':0,
                        'url': url,
                        'crawl state':'half'
                    }
        yield from response.follow_all(detail_page_links, callback = self.parse_content)

    def parse_content(self, response):
        UID = response.url.split('/')[-1][:-16]

        paragraph_list = response.css('div.wip_art_con p *::text').getall()
        if len(paragraph_list) == 0:
            paragraph_list = response.css('div#zoom p *::text').getall()
        if len(paragraph_list) == 0:
            paragraph_list = response.css('p *::text').getall()
        if len(paragraph_list) == 0:
            paragraph_list = response.css('*::text').getall()
        if len(response.css('div.wip_art_con p')) >= 2:
            File_num = response.css('div.wip_art_con p')[1].css('::text').get()
        else:
            File_num = None
        if File_num and '号' not in File_num:
            File_num = None
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
            'crawl state':state,
            'text length':length,
        }
