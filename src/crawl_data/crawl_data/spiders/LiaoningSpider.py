import scrapy
import pickle
import os

class LiaoningSpider(scrapy.Spider):
    name = "Liaoning"
    if not os.path.exists('../../data/HTML_pk/%s' % name):
        os.makedirs('../../data/HTML_pk/%s' % name)
    if not os.path.exists('../../data/text/%s' % name):
        os.makedirs('../../data/text/%s' % name)
    def start_requests(self):
        url_dict = {
            'http://www.ln.gov.cn/zfxx/zfwj/szfl/index{0}.html':9,
            'http://www.ln.gov.cn/zfxx/zfwj/szfbgtwj/zfwj2011_136268/index{0}.html':2,
            'http://www.ln.gov.cn/zfxx/zfwj/szfwj/zfwj2011_140407/index{0}.html':1,
            'http://www.ln.gov.cn/zfxx/zfwj/bmwj/index{0}.html':1
        }
        #test_page = 1
        for url_base, max_page in url_dict.items():
            for i in range(max_page):
                page = '_' + str(i) if i>0 else ''
                yield scrapy.Request(url=url_base.format(page), callback=self.parse)

    def parse(self,response):
        url_sign = response.url.split('/')[-2]
        if url_sign == 'zfwj2011_136268' or url_sign == 'zfwj2011_140407':
            td_base = 0
        elif url_sign == 'szfl':
            td_base = 1
        elif url_sign == 'bmwj':
            td_base = 2
        detail_page_links = []
        for tr in response.css('table.dataList tr')[1:]:
            td_list = tr.css('td')
            href = response.urljoin(td_list[0+td_base].css('a::attr(href)').get())
            UID = href.split('/')[-1][:-5]
            if '?' not in UID:
                detail_page_links.append(href)
            date = td_list[2+td_base].css('::text').get() 
            if date and len(date) > 3:
                date = date.replace('年','-').replace('月','-').replace('日','')
            yield {
                'UID': UID,
                'title': td_list[0+td_base].css('a::attr(title)').get(),
                'date': date,
                'FileNumber':td_list[1+td_base].css('::text').get(),
                'url': href,
                'text length':0,
                'crawl state':'half'
            }
        yield from response.follow_all(detail_page_links, callback = self.parse_content)

    def parse_content(self, response):
        UID = response.url.split('/')[-1][:-5]
        paragraph_list = response.css('div#main *::text').getall()
        
        if len(paragraph_list) == 0:
            paragraph_list =  response.css('div *::text').getall() 
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

