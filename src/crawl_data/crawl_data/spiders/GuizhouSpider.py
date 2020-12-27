import scrapy
import pickle
import os

class GuizhouSpider(scrapy.Spider):
    name = "Guizhou"
    if not os.path.exists('../../data/HTML_pk/%s' % name):
        os.makedirs('../../data/HTML_pk/%s' % name)
    if not os.path.exists('../../data/text/%s' % name):
        os.makedirs('../../data/text/%s' % name)
    def start_requests(self):
        url_dict = {
            'http://www.guizhou.gov.cn/zwgk/zcfg/szfwj_8191/qff_8193/index{0}.html':28,
            'http://www.guizhou.gov.cn/zwgk/zcfg/gfxwj/index{0}.html':17,
        }
        # test_page = 2
        for url_base, max_page in url_dict.items():
            for i in range(max_page):
                page = '_' + str(i) if i>0 else ''
                yield scrapy.Request(url=url_base.format(page), callback=self.parse)

    def parse(self,response):
        detail_page_links = []

        for li in response.css('div.right-list-box ul li'):
            url = li.css('a::attr(href)').get()
            UID = url.split('/')[-1][:-5]
            if '?' not in UID:
                detail_page_links.append(url)
            title = li.css('a::attr(title)').get()
            file_num = title.split('（')[-1]
            file_num = file_num.split('(')[-1][:-1]
            date = li.css('span::text').get()
            if date and len(date) > 10:
                date = date[:10]
            yield {
                'UID': UID,
                'title': title,
                'date': date,
                'FileNumber': file_num,
                'url': url,
                'text length':0,
                'crawl state':'half'
            }
        yield from response.follow_all(detail_page_links, callback = self.parse_content)

    def parse_content(self, response):
        UID = response.url.split('/')[-1][:-5]
        paragraph_list = response.css('div.view p *::text').getall()  
        if len(paragraph_list) == 0:
            paragraph_list = response.css('div#Zoom p *::text').getall()  
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

