import scrapy
import pickle
import os

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
options = Options()
options.headless = True

class HubeiSpider(scrapy.Spider):
    name = "Hubei"
    if not os.path.exists('../../data/HTML_pk/%s' % name):
        os.makedirs('../../data/HTML_pk/%s' % name)
    if not os.path.exists('../../data/text/%s' % name):
        os.makedirs('../../data/text/%s' % name)
    
    def __init__(self):
        self.browser = webdriver.Firefox(options=options)
        self.browser.get('http://www.hubei.gov.cn')
        super().__init__()
    
    def close(self,spider):
        self.browser.quit()

    def start_requests(self):
        url_dict = {
            'http://www.hubei.gov.cn/zfwj/szfl/index{0}.shtml':10,
            'http://www.hubei.gov.cn/zfwj/ezf/index{0}.shtml':47,
            'http://www.hubei.gov.cn/zfwj/ezh/index{0}.shtml':12,
            'http://www.hubei.gov.cn/zfwj/ezd/index{0}.shtml':1,
            'http://www.hubei.gov.cn/zfwj/ezbf/index{0}.shtml':50,
            'http://www.hubei.gov.cn/zfwj/qt/index{0}.shtml':8, 
        }
        # test_page = 1
        for url_base, max_page in url_dict.items():
            for i in range(max_page):
                page = '_' + str(i) if i>0 else ''
                yield scrapy.Request(url=url_base.format(page), callback=self.parse)

    def parse(self,response):
        detail_page_links = []

        for li in response.css('div.list_block li'):
            url = response.urljoin(li.css('a::attr(href)').get())
            UID = url.split('/')[-1][:-6]
            date = li.css('span::text').get()
            detail_page_links.append(url)
            if date and len(date)>10:
                date = date[:10]
            yield {
                'UID': UID,
                'title': li.css('a::attr(title)').get(),
                'date': date,
                'url': url, 
                'crawl state':'half',
                'text length':0,
                'FileNumber':None
            }
        yield from response.follow_all(detail_page_links, callback = self.parse_content)

    def parse_content(self, response):
        UID = response.url.split('/')[-1][:-6]
        doc_info_dict = {}
        div_list = response.css('div.metadata_content div.col-xs-12')
        for div in div_list:
            row = div.css('::text').getall()
            if len(row) == 3:
                key = row[1]
                value = row[2]
            elif len(row) == 5:
                key = row[1]
                value = row[3]
            doc_info_dict[key] = value
        FileNum =None
        if '文    号：' in doc_info_dict.keys():
            FileNum = doc_info_dict['文    号：']
        paragraph_list = response.css('div.content_block *::text').getall()
        if len(paragraph_list) == 0:
            paragraph_list =  response.css('*::text').getall() 
        length = len(''.join(paragraph_list))
        if length > 0:
            state = 'full'
            with open('../../data/text/%s/%s.txt' % (self.name,UID), 'w') as f:
                f.write('\n'.join(paragraph_list))
            with open('../../data/HTML_pk/%s/%s.pkl' % (self.name,UID), 'wb') as f:
                pickle.dump(response.text,f)
        else:
            state = 'empty'
        return {
            'UID': UID,
            'doc_info_dict': doc_info_dict,
            'mainText': paragraph_list,
            'crawl state':state,
            'text length':length,
            'FileNumber':FileNum,
        }

