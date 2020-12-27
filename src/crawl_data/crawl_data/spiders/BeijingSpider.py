import scrapy
import os
import pickle

class BeijingSpider(scrapy.Spider):
    name = "Beijing"
    if not os.path.exists('../../data/HTML_pk/%s' % name):
        os.makedirs('../../data/HTML_pk/%s' % name)
    if not os.path.exists('../../data/text/%s' % name):
        os.makedirs('../../data/text/%s' % name)
    def start_requests(self):
        total_page = 264
        # total_page = 3
        url_base = 'http://www.beijing.gov.cn/zhengce/zhengcefagui/index'
        for i in range(total_page):
            ref = '.html' if i == 0 else '_%s.html' % i 
            yield scrapy.Request(url=url_base + ref, callback=self.parse)

    def parse(self,response):
        detail_page_links = []
        for piece in response.css('div.listBox ul.list li'):
            href = piece.css('a::attr(href)').get()
            url = response.urljoin(href)
            detail_page_links.append(href)
            UID = href.split('/')[-1][:-5]
            if '?' not in UID:
                detail_page_links.append(url)
            #response.follow(href, callbak = self.parse_content)
            yield {
                'UID': UID,
                'title': piece.css('a::text').get(),
                'date': piece.css('span::text').get(),
                'url': url,
                'text length':0,
                'FileNumber': None,
                'crawl state':'half'
            }
        yield from response.follow_all(detail_page_links, callback = self.parse_content)

    def parse_content(self, response):
        UID = response.url.split('/')[-1][:-5]
        doc_info_dict = {}
        container = response.css('div.container')[0]
        for doc_info in container.css('ol li'):
            doc_info_l = doc_info.css('::text').getall()
            if len(doc_info_l) == 2:
                key,value = doc_info_l
            elif len(doc_info_l) == 1:
                key = doc_info_l[0]
                value = ''
            doc_info_dict[key] = value
        full_tittle = container.css('div.header p::text').get()
        paragraph_list = container.css('div.mainTextBox p::text').getall()
        if len(paragraph_list) == 0:
            paragraph_list =  response.css('p *::text').getall() 
        Filenum = doc_info_dict["[发文字号] "] if "[发文字号] " in doc_info_dict.keys() else paragraph_list[0]
        if Filenum and '号' not in Filenum:
            Filenum = None
        length = len(''.join(paragraph_list))
        if length > 0:
            with open('../../data/text/%s/%s.txt' % (self.name,UID), 'w') as f:
                f.write('\n'.join(paragraph_list))
            with open('../../data/HTML_pk/%s/%s.pkl' % (self.name,UID), 'wb') as f:
                pickle.dump(response.text,f)
            return {
                'UID': UID,
                'full_tittle': full_tittle,
                'FileNumber':Filenum,
                'doc_info_dict': doc_info_dict,
                'mainText': paragraph_list,
                'text length':length,
                'crawl state': 'full',
            }
        else:
            return {
                'UID': UID,
                'full_tittle': full_tittle,
                'FileNumber':Filenum,
                'doc_info_dict': doc_info_dict,
                'mainText': paragraph_list,
                'text length':length,
                'crawl state': 'empty',
            }
            

