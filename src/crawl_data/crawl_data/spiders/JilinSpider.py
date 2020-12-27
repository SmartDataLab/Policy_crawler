import scrapy
import pickle
import os
import json
from urllib import parse
from scrapy.selector import Selector

class JilinSpider(scrapy.Spider):
    name = "Jilin"
    if not os.path.exists('../../data/HTML_pk/%s' % name):
        os.makedirs('../../data/HTML_pk/%s' % name)
    if not os.path.exists('../../data/text/%s' % name):
        os.makedirs('../../data/text/%s' % name)
    def start_requests(self):
        total_page = 173
        # total_page = 3
        url_base = 'http://infogate.jl.gov.cn/govsearch/jsonp/zf_jd_list.jsp?page={0}&lb=134657&callback=result&sword=&searchColumn=all&searchYear=all&pubURL=http%3A%2F%2Fxxgk.jl.gov.cn%2F&SType=1&searchColumnYear=all&searchYear=all&pubURL=&SType=1&channelId=134657&_=1585041673815'
        for i in range(total_page):
            yield scrapy.Request(url=url_base.format(str(i+1)), callback=self.parse)

    def parse(self,response):
        detail_page_links = []
        for piece_dict in json.loads(response.text[66:-4])['data']:
            item = {
                'UID':piece_dict['MetaDataId'],
                'url':piece_dict['puburl'],
                'title':piece_dict['tip']['title'],
                'date':piece_dict['tip']['dates'],
                'FileNumber':piece_dict['tip']['filenum'],
                'publisher':piece_dict['tip']['publisher'],
                'text length':0,
                'crawl state':'half',
            }
            if '?' not in item['UID']:
                detail_page_links.append(item['url'])
            yield item
        yield from response.follow_all(detail_page_links, callback = self.parse_content)

    def parse_content(self, response):
        UID = response.url.split('_')[-1][:-5]
        state = 'full' if response.status == 200 else 'half'
        paragraph_list = response.css('div.zlyxwz_t2a p *::text').getall()
        attachment_links = response.css('div.zlyxwz_t2a p a::attr(href)').getall()        
        
        if len(paragraph_list) == 0:
            paragraph_list =  response.css('p *::text').getall() 
        if len(paragraph_list) == 0:
            paragraph_list =  response.css('*::text').getall() 
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
            'attachment_links':attachment_links,
            'crawl state':state,
            'text length':length,
        }
