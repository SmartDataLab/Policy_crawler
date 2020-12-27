import scrapy
import pickle
import os

class HunanSpider(scrapy.Spider):
    name = "Hunan"
    if not os.path.exists('../../data/HTML_pk/%s' % name):
        os.makedirs('../../data/HTML_pk/%s' % name)
    if not os.path.exists('../../data/text/%s' % name):
        os.makedirs('../../data/text/%s' % name)
    def start_requests(self):
        url_dict = {
            'http://www.hunan.gov.cn/hnszf/xxgk/wjk/szfwj/wjk_glrb{0}.html':34,
            'http://www.hunan.gov.cn/hnszf/xxgk/wjk/szfbgt/wjk_glrb{0}.html':34,
        }
        # test_page = 2
        for url_base, max_page in url_dict.items():
            for i in range(max_page):
                page = '_' + str(i+1) if i>0 else ''
                yield scrapy.Request(url=url_base.format(page), callback=self.parse)

    def parse(self,response):
        detail_page_links = []
        for tr in response.css('tbody tr'):
            url = tr.css('a::attr(href)').get()
            url = response.urljoin(url)
            UID = url.split('/')[-1][:-5]
            if '?' not in UID:
                detail_page_links.append(url)
            yield {
                'UID': UID,
                'title': tr.css('a::text').get(),
                'date': tr.css('td')[-2].css('::text').get(),
                'FileNumber': tr.css('td')[-3].css('::text').get().split("'")[1],
                'url': url,
                'text length':0,
                'crawl state':'half'
            }
        yield from response.follow_all(detail_page_links, callback = self.parse_content)

    def parse_content(self, response):
        UID = response.url.split('/')[-1][:-5]
        paragraph_list = response.css('div#zoom p *::text').getall() 
        attachment_list = response.css('div#zoom a::attr(href)').getall() 
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
            'attachment_link': attachment_list,
            'crawl state':state,
            'text length':length,
        }

