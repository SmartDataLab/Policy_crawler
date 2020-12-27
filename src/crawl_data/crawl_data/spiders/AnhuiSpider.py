import scrapy
import pickle
import os
import ast
from urllib import parse
from scrapy.selector import Selector

class AnhuiSpider(scrapy.Spider):
    name = "Anhui"
    if not os.path.exists('../../data/HTML_pk/%s' % name):
        os.makedirs('../../data/HTML_pk/%s' % name)
    if not os.path.exists('../../data/text/%s' % name):
        os.makedirs('../../data/text/%s' % name)
    def start_requests(self):
        total_page = 448
        # total_page = 3 

        headers = {
            'Cookie':'yfx_c_g_u_id_10006888=_ck20032823561110758413715353987; yfx_f_l_v_t_10006888=f_t_1585410971071__r_t_1585410971071__v_t_1585410971071__r_c_0; UM_distinctid=17121db9612ad6-0ec7fe709cb527-31760856-ff000-17121db9613ce3; CNZZDATA3688016=cnzz_eid%3D1930396560-1585409032-%26ntime%3D1585409032; membercenterjsessionid=MWViOWE2ZDktYmRlNC00NWMzLWFiMWUtNjQ3NWU0OGYzNTFl; wzws_cid=7187a7347902f0d7885c71d456e608136714b577f2ee24a43314ebd9d84b64b6f438b3bf396c3d7cf59f1f30cc019242417df6f600b6f2ee80692577b8f7754ab14524ba3008de665fdf770f7f231f9a; SHIROJSESSIONID=82f1243e-8bc8-4770-8f88-8438524086a6',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
        }
        url_base = 'http://www.ah.gov.cn/site/label/8888?IsAjax=1&dataType=html&_=0.42568734060518776&siteId=6781961&pageSize=16&pageIndex={0}&action=list&isDate=true&dateFormat=yyyy-MM-dd&length=46&organId=1681&type=4&catId=&cId=&result=%E6%9A%82%E6%97%A0%E7%9B%B8%E5%85%B3%E4%BF%A1%E6%81%AF&searchType=&keyWords=&specialCatIds=6708451%2C6708461%2C6708471&catIdExplainType=6711101tp_explain%2C6711111xwfbh_explain%2C6711121sp_explain%2C6711131ft_explain&labelName=publicInfoList&file=%2Fahxxgk%2FpublicInfoList-an-new'
        for i in range(total_page):
            yield scrapy.Request(url=url_base.format(i+1),headers=headers, callback=self.parse)

    def parse(self,response):
        detail_page_links = []
        for div in response.css('div.xxgk_navli'):
            url = div.css('a::attr(href)').get()
            UID = url.split('/')[-1][:-5]
            date = div.css('span.date::text').get()
            if date and len(date) > 1:
                date = date.replace('\r','')
                date = date.replace('\n','')
                date = date.replace('\t','')
            if '?' not in UID:
                detail_page_links.append(url)
            yield {
                'UID': UID,
                'title': div.css('a::attr(title)').get(),
                'date': date,
                'FileNumber':None,
                'url': url,
                'text length':0,
                'crawl state':'half'
            }
        try:
            yield from response.follow_all(detail_page_links, callback = self.parse_content)
        except:
            print(response.text)

    def parse_content(self, response):
        UID = response.url.split('/')[-1][:-5]
        doc_info_dict = {}
        td_list = response.css('tbody')[0].css('td')
        th_list = response.css('tbody')[0].css('th')
        for i in range(len(th_list)):
            key = ''.join(th_list[i].css('::text').getall())
            value = ''.join(td_list[i].css('::text').getall())
            doc_info_dict[key] = value
        File_num = None
        if '文号：' in doc_info_dict.keys():
            File_num = doc_info_dict['文号：']
        paragraph_list =  response.css('div.wzcon p *::text').getall() 
        if len(paragraph_list) == 0:
            paragraph_list =  response.css('p *::text').getall() 
        length = len(''.join(paragraph_list))
        if length > 0:
            with open('../../data/HTML_pk/%s/%s.pkl' % (self.name,UID), 'wb') as f:
                pickle.dump(response.text,f)
            with open('../../data/text/%s/%s.txt' % (self.name,UID), 'w') as f:
                f.write('\n'.join(paragraph_list))
            return {
                'UID': UID,
                'FileNumber':File_num,
                'mainText': paragraph_list,
                'doc_info_dict':doc_info_dict,
                'crawl state':'full',
                'text length':length,
            }
        else:
            return {
                'UID': UID,
                'mainText': paragraph_list,
                'crawl state':'empty',
                'text length':0,
            }
