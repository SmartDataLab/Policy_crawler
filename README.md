# Policy_crawler

**声明:爬取内容皆为政府对外公示文件，使用用途为学术研究。**

爬取中国 34 个省份办公厅的公文数据。
开发与运行系统:ubuntu18

技术栈:

- python3
- mongodb 默认配置
- scrapy2.0
- pymongo

项目于 2020 年 4 月 14 日结束，只要网站 html 结构不变的情况下可以爬取至运行日期，如果网站结果变换，欢迎开源爱好者 fork 进行修改并提交 merge master 申请。

## quick start

```
git clone https://github.com/JinhuaSu/Policy_crawler.git
cd src/crawl_data
bash crawl_all.sh
```

运行结束后，存在爬取速度过快导致 fail 的省份，这时考虑配置 selenium,middlewares 已经配置示例，根据需要修改 settings,然后重新爬取各省份即可。

**上述爬取中湖北和中央运行了反爬，需要使用 selenium 的 firefox 来处理**

## project log

**add splash**

pip install scrapy-splash
sudo apt install docker.io
docker pull scrapinghub/splash
docker run -p 8050:8050 scrapinghub/splash

**useful index**

scrapy shell -s USER_AGENT="Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/60.0"

if contain ?, url must have ''.

next_page = response.urljoin(next_page)

> > > from scrapy.selector import Selector
> > > body = '<html><body><span>good</span></body></html>'
> > > Selector(text=body).xpath('//span/text()').get()

js escape 编码 https://www.cnblogs.com/yoyoketang/p/8058873.html

headers = {
'User-Agent': "Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/60.0",
'Referer': "http://service.shanghai.gov.cn/pagemore/iframePagerIndex_12344_2_22.html?objtype=&nodeid=&pagesize=&page=13"
}

**Jiangxi**

total page 106

"文 号:"

scrapy shell -s USER_AGENT="Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/60.0" 'http://www.jiangxi.gov.cn/module/xxgk/subjectinfo.jsp?sortfield=compaltedate:0&fbtime=&texttype=0&vc_all=&vc_filenumber=&vc_title=&vc_number=&currpage=2&binlay=&c_issuetime='

response.css('tr.tr_main_value_odd')[0].css('td a::attr()').getall()

response.css('div.bt-article-y')
response.css('div.bt-article-y')[0].css('tr td::text').getall()
response.css('div.bt-article-y')[0].css('tr td b::text').getall()
response.css('div.bt-article-y')[0].css('tr td b').text
response.css('div.bt-article-y')[0].css('tr td b')[0].text
response.css('div.bt-article-y')[0].css('tr td b::text').getall()
response.css('div.bt-article-y')[0].css('tr td b span::text').getall()
response.css('div.bt-article-y p.sp_title')
response.css('div.bt-article-y p.sp_title::text')
response.css('div.bt-article-y p.sp_title::text').get()
response.css('div.bt-article-y p.sp_title::text').data
response.css('div.bt-article-y p.sp_title::data')
response.css('div.bt-article-y p.sp_title::text')
response.css('div.bt-article-y p.sp_title::text').getall()
response.css('div.bt-article-y div#zoom').getall()
response.css('div.bt-article-y div#zoom')
response.css('div.bt-article-y div#zoom p')
response.css('div.bt-article-y div#zoom p::text')
response.css('div.bt-article-y div#zoom p::text').getall()
response.css('div.bt-article-y div#zoom p a::href').getall()
response.css('div.bt-article-y div#zoom p a::attr(href)').getall()

**Shanghai**

total page 298

http://service.shanghai.gov.cn/XingZhengWenDangKuJyh/XZGFList.aspx?testpara=0&kw=&issueDate_userprop8=&status=1&departid=0&wenhao=&issueDate_userprop8_end=&excuteDate=&excuteDate_end=&closeDate=&closeDate_end=&departtypename=0&typename=%E5%85%A8%E9%83%A8&zhutitypename=&zhuti=&currentPage=2&pagesize=10

In [11]: response.css('table[class="table table-list"] tr')[1:][0].css('td a::attr(title)').get()  
Out[11]: '上海市人民政府办公厅关于印发《上海市农村房屋安全隐患排查整治工作方案》的通知'

In [12]: response.css('table[class="table table-list"] tr')[1:][0].css('td a::attr(href)').get()  
Out[12]: 'XZGFDetails.aspx?docid=REPORT_NDOC_006873'

In [13]: response.css('table[class="table table-list"] tr')[1:][0].css('td')[1].css('::text').get()  
Out[13]: '沪府办规〔2020〕17 号'

In [14]: response.css('table[class="table table-list"] tr')[1:][0].css('td')[2].css('::text').get()  
Out[14]: '2020-12-04'

response.css('div#ivs_content \*::text').getall()

**Tianjin**

'date2'文号
'date3'发文日期

total page:1000

json_site:
http://www.tj.gov.cn/igs/front/search/list.html?index=zcwj-index-200424&type=zcfg&filter[AVAILABLE]=true&siteId=&pageSize=10&pageNumber=2&filter%5BFWJG_name%5D=&filter%5BBT%2CZW%2CFWZH-or%5D=&orderProperty=FBRQ&orderDirection=desc&filter%5BWZFL_name%5D=&filter%5BFBRQ-lte%5D=&filter%5BFBRQ-gte%5D=

{'filter': {'AVAILABLE': 'true',
'BT,ZW,FWZH-or': None,
'FBRQ-gte': None,
'FBRQ-lte': None,
'FWJG_name': None,
'WZFL_name': None},
'**index': 'zcwj-index-200424',
'**type': 'zcfg',
'pageable': {},
'queryFilter': {'filter': {'AVAILABLE': 'true',
'BT,ZW,FWZH-or': None,
'FBRQ-gte': None,
'FBRQ-lte': None,
'FWJG_name': None,
'WZFL_name': None},
'fieldAndValues': None},
'hasFilter': True,
'page': {'content': [{'AttachPic': 0,
'GJC': '',
'WZFL': '1751',
'FZYJ': '',
'ZCJD': '',
'OriginMetaDataId': 5100726,
'ChannelId': 67466,
'AttachVideo': 0,
'highlight': {},
'BT': '市商务局 市卫生健康委 市工业和信息化局 市生态环境局关于做好我市医疗卫生机构产生的可回收输液瓶（袋）回收管理工作的通知', // title
'DOCPUBURL': 'http://shangwuju.tj.gov.cn/tjsswjzz/zwgk/zcfg_48995/swjwj/202012/t20201221_5100726.html', // url
'WCMMetaTableGovZhengCeWenJianID': 184359,
'MetaDataId': 5100726,
'XGBD': '',
'YXX': '0',
'FBRQ': '2020-12-21T00:00:00.000+0800', //date
'IDXID': '11120000MB1908811Q/2020-04798',
'FWZH': '津商流通〔2020〕20 号', //FileNumber
'WZFL_name': '津商流通',
'LHFWDW': '1408,1392,1400',
'ZTFL': '1119,1124,1250',
'CWRQ': '2020-12-18T00:00:00.000+0800',
'ZTFL_name': '政务公开',
'AVAILABLE': True,
'VersionNum': 0,
'OrganCat': '1337',
'JB': '1',
'CrUser': 'changtao_swj',
'DXFL': '0,1',
'DocRelTime': '2020-12-21T00:00:00.000+0800',
'trs_warehouse_time': '2020-12-21T07:54:21.625Z',
'_id': '5100726',
'ThumbFiles': '',
'FWJG_name': '天津市商务局',
'ZW': '市商务局\u2002 市卫生健康委', // mainText
'CrTime': '2020-12-21T07:37:08.000Z'}],
'total': '38546',
'pageSize': 10,
'pageNumber': 2,
'searchProperty': None,
'searchValue': None,
'orderProperty': 'FBRQ',
'orderDirection': 'desc',
'totalPages': 1000}}

In [4]: response.css('div.index_right_content ul li')[0].css('a::attr(href)').get()  
Out[4]: 'http://gk.tj.gov.cn/gkml/000125014/202003/t20200316_87172.shtml'

In [5]: response.css('div.index_right_content ul li')[0].css('a::attr(title)').get()  
Out[5]: '天津市人民政府关于李志荣等任职的通知'

In [6]: response.css('div.index_right_content ul li')[0].css('span.date1::text').get()  
Out[6]: '索引号：000125014/2020-00025'

In [7]: response.css('div.index_right_content ul li')[0].css('span.date2::text').get()  
Out[7]: '文号：津政人〔2020〕33 号'

In [8]: response.css('div.index_right_content ul li')[0].css('span.date3::text').get()  
Out[8]: '发文日期：2020 年 03 月 16 日'

response.css('table.table*key').get()
response.css('table.table_key tr').get()
response.css('table.table_key tr')
response.css('table.table_key tr')[0]
response.css('table.table_key tr')[0].css('td *::text')
response.css('table.table*key tr')[0].css('td *::text').getall()
response.css('table.table*key tr')[0].css('td::text').getall()
response.css('table.table_key tr')[0].css('td *::text').getall()
response.css('table.table*key tr')[3].css('td *::text').getall()
response.css('div.TRS*PreAppend p::text').get()
response.css('div.TRS_PreAppend p *::text').get()
response.css('div.TRS*PreAppend p::text').getall()
response.css('div.TRS_PreAppend p 8::text').getall()
response.css('div.TRS_PreAppend p *::text').getall()

**Chongqing**

不爬取市政府内部细分部门文件和已经废止和失效的文件

doc_info_dict
"文 号："

content_list:
http://www.cq.gov.cn/zwgk/fdzdgknr/lzyj/zfgz/zfgz_52609/index_11.html
http://www.cq.gov.cn/zwgk/fdzdgknr/lzyj/xzgfxwj/szf_38655/index_22.html
http://www.cq.gov.cn/zwgk/fdzdgknr/lzyj/xzgfxwj/szfbgt_38656/index_32.html
http://www.cq.gov.cn/zwgk/fdzdgknr/lzyj/qtgw/index_33.html
http://www.cq.gov.cn/zwgk/fdzdgknr/lzyj/rsrm/index_2.html

response.css('ul.list-cont')
response.css('ul.list-cont li.w120')
len(response.css('ul.list-cont li.w120'))
len(response.css('ul.list-cont li.w400'))
len(response.css('ul.list-cont li.w172'))
len(response.css('ul.list-cont li.w110'))
response.css('ul.list-cont li.w120::text').getall()
response.css('ul.list-cont li.w400 a::text').getall()
response.css('ul.list-cont li.w172::text').getall()
response.css('ul.list-cont li.w110 span::text').getall()
response.css('ul.list-cont li.w400 a::attr(href)').getall()

response.text
response.css('table.gkxl-top')
response.css('table.gkxl-top td')
response.css('table.gkxl-top td::text').getall()
len(response.css('table.gkxl-top td::text').getall())
response.css('table.gkxl-top td').getall()
len(response.css('table.gkxl-top td').getall())
response.css('table.gkxl-top td').getall()[-1].get()
response.css('table.gkxl-top td').[-1].get()
response.css('table.gkxl-top td')[-1].get()
response.css('table.gkxl-top td')[-1].css('::text').get()
type(response.css('table.gkxl-top td')[-1].css('::text').get())
{'2':2}
{'2':response.css('table.gkxl-top td')[-1].css('::text').get()}
response.css('div.gkxl-article p \*::text').getall()

**Heilongjiang**

http://zwgk.hlj.gov.cn/zwgk/publicInfo/searchFile?chanPath=2,&chanP=2%2C&page=2&limit=10&total=0

total_page 192

{'code': '0',
'serverTime': 1608904201,
'data': {'records': [{'docType': 2,
'id': 448586,
'title': '黑龙江省人民政府关于调整 3 个议事协调机构组成人员的通知',
'publishTime': 1606376547,
'editTime': 1606147200,
'createTime': 1606376692,
'deptName': '省政府办公厅',
'fileNumber': '黑政调〔２０２０〕６号'},
{'docType': 2,
'id': 448555,
'title': '黑龙江省人民政府关于金银华等任免职的通知',
'publishTime': 1604397663,
'editTime': 1604332800,
'createTime': 1604395962,
'deptName': '省政府办公厅',
'fileNumber': '黑政干〔２０２０〕１８号'}],
'total': 1913,
'size': 10,
'current': 2,
'orders': [],
'searchCount': True,
'pages': 192}}

http://zwgk.hlj.gov.cn/zwgk/publicInfo/detail?id=448572

response.css('div[class=zwnr] \*::text').getall()

In [5]: ast.literal_eval(response.text[25:-29])['data'][0]  
Out[5]:
{'title': '司法行政法制工作规定',
'url': 'http://www.hlj.gov.cn/gkml/detail.html?t=2&d=175325',
'time': '1990 年 8 月 18 日',
'IndexNumber': '001697444\x814-00546',
'Name': '省司法厅',
'longtitle': '司法行政法制工作规定',
'Fenlei': '公安、安全、司法',
'FileNumber': '司法部令第 10 号',
'SubjectIterms': '',
'number': '1',
'ID': '175325'}

response.text[8:-6]
from scrapy.selector import Selector
Selector(text=response.text[8:-6]).css('div.zwnr').get()
Selector(text=response.text[8:-6]).css('div.zwnr')
Selector(text=response.text[8:-6]).css('div')
Selector(text=response.text[7:-6]).css('div')
response.text[7:-6]
from urllib import parse
new*text = parse.unquote_plus(response.text[7:-6])
new_text
Selector(text=new_text).css('div')
Selector(text=new_text).css('div.zwnr')
Selector(text=new_text).css('div.zwnr *::text').getall()
parse.unqote*plus(Selector(text=new_text).css('div.zwnr *::text').getall()[0])
parse.unquote*plus(Selector(text=new_text).css('div.zwnr *::text').getall()[0])
new*text
parse.unquote(Selector(text=new_text).css('div.zwnr *::text').getall()[0])
parse.quote(Selector(text=new*text).css('div.zwnr *::text').getall()[0])
new*text.decode('unicode_escape')
decode(new_text,'unicode_escape')
'苏'.encode('unicode_escape')
response.body
response.body.decode.('unicode_escape')
response.body.decode('unicode_escape')
urllib.unquote(response.body.decode('unicode_escape'))
parse.unquote(response.body.decode('unicode_escape'))
Selector(text=new_text).css('div.zwnr *::text').getall()[0].replace("%","\\")
Selector(text=new_text).css('div.zwnr \*::text').getall()[0].replace("%","\\").encode("utf-8").decode("unicode_escape")

**Jilin**

total page 173

http://infogate.jl.gov.cn/govsearch/jsonp/zf_jd_list.jsp?page=6&lb=134657&callback=result&sword=&searchColumn=all&searchYear=all&pubURL=http%3A%2F%2Fxxgk.jl.gov.cn%2F&SType=1&searchColumnYear=all&searchYear=all&pubURL=&SType=1&channelId=134657&_=1585041673815

response.text
import json
len('\r\n\r\n\r\n\r\n\r\n\r\n\ufeff\r\n\r\n\r\n\r\n\r\n \r\n \r\n\r\n\r\n\r\n\r\n \r\n \r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\nresult(')
len(');\r\n')
json.loads(response.text[67:-4])
response.text[67:-4]
response.text[66:-4]
json.loads(response.text[66:-4])
json_dict = json.loads(response.text[66:-4])
json_dict['data']
json_dict['data'][0]['puburl']
json_dict['data'][0]['MetaDataId']
json_dict['data'][0]['tip']['dates']
json_dict['data'][0]['tip']['filenum']
json_dict['data'][0]['tip']['publisher']
json_dict['data'][0]['tip']['title']

response.text
response.css('tbody')
response.css('table')
response.css('table.zly_xxgk_20170802')
response.css('table.zly_xxgk_20170802 tbody')
response.css('table.zly_xxgk_20170802 tbody').get()
response.css('div.zlyxwz_t2a p \*::text').getall()
response.css('div.zlyxwz_t2a p a::attr(href)').getall()

**Hebei**

total_page 83

http://info.hebei.gov.cn/eportal/ui?pageId=6817552&currentPage=1&moduleId=3bb45f8814654e33ae014e740ccf771b&formKey=GOV_OPEN&columnName=EXT_STR7&relationId=

http://info.hebei.gov.cn/eportal/ui?pageId=6806152&articleKey=6903671&columnId=6806589

headers = {
'User-Agent': "Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/60.0",
'Referer': "http://info.hebei.gov.cn/eportal/ui?pageId=6817552"
}
Request(url="http://info.hebei.gov.cn/eportal/ui?pageId=6817552&currentPage=1&moduleId=3bb45f8814654e33ae014e740ccf771b&formKey=GOV_OPEN&columnName=EXT_STR7&relationId=",headers=headers)
scrapy.Request(url="http://info.hebei.gov.cn/eportal/ui?pageId=6817552&currentPage=1&moduleId=3bb45f8814654e33ae014e740ccf771b&formKey=GOV_OPEN&columnName=EXT_STR7&relationId=",headers=headers)
req = scrapy.Request(url="http://info.hebei.gov.cn/eportal/ui?pageId=6817552&currentPage=1&moduleId=3bb45f8814654e33ae014e740ccf771b&formKey=GOV_OPEN&columnName=EXT_STR7&relationId=",headers=headers)
fetch(req)
response
response.text
response.css('table.xxgkzclbtab3')
len(response.css('table.xxgkzclbtab3'))
response.css('table.xxgkzclbtab3')[0].css('td a::text')getall()
response.css('table.xxgkzclbtab3')[0].css('td a::text').getall()
response.css('table.xxgkzclbtab3')[0].css('td a::text').get()
response.css('table.xxgkzclbtab3')[0].css('td a::attr(href)').get()
response.css('table.xxgkzclbtab3')[0].css('td[align="left"]::text').get()
response.css('table.xxgkzclbtab3')[0].css('td[align="center"]::text').get()
response.css('table.xxgkzclbtab3')[0].css('td[align="center"]::text').getall()
response.css('table.xxgkzclbtab3')[0].css('td[align="center"]::text').getall()[-1]
response.css('table.xxgkzclbtab3')[0].css('td[align="center",width="60"]::text').get()
response.css('table.xxgkzclbtab3')[0].css('td[align="center"][width="60"]::text').get()
response.css('table.xxgkzclbtab3')[0].css('td[align="center"][width="150"]::text').get()

response.css('div.xxgk*bmxl')
response.css('div.xxgk_bmxl td')
len(response.css('div.xxgk_bmxl td'))
response.css('div.xxgk_bmxl td')[0].css('*::text').get()
response.css('div.xxgk*bmxl td')[1].css('*::text').get()
response.css('div.xxgk*bmxl td')[2].css('*::text').get()
response.css('div.xxgk*bmxl td')[3].css('*::text').get()
response.css('div.xxgk*bmxl td')[4].css('*::text').get()
response.css('div.xxgk*bmxl td')[9].css('*::text').get()
response.css('div.xxgk*bmxl td')[8].css('*::text').get()
response.css('div#zoom')
response.css('div#zoom div')
response.css('div#zoom div::text').getall()
response.css('div#zoom div \_::text').getall()

**Neimenggu**

http://www.nmg.gov.cn/zwgk/zfxxgk/zfxxgkml/gzxzgfxwj/xzgfxwj/index_2.html 71
http://www.nmg.gov.cn/zwgk/zfxxgk/zfxxgkml/zzqzfjbgtwj/index_1.html 152

In [5]: response.css('tbody tr')[0].css('td')[1].css('a::attr(href)').get()  
Out[5]: 'http://www.nmg.gov.cn/zwgk/zfxxgk/zfxxgkml/zzqzfjbgtwj/202012/t20201214_366066.html'

In [7]: response.css('tbody tr')[0].css('td')[1].css('a::text').get()  
Out[7]: '内蒙古自治区人民政府关于《根河市城市总体规划（2019—2030）》的批复'

In [9]: response.css('tbody tr')[0].css('td')[-3].css('::text').get()  
Out[9]: '内政字〔2020〕102 号'

In [10]: response.css('tbody tr')[0].css('td')[-1].css('::text').get()  
Out[10]: '2020-12-08'

In [4]: response.css('div[class="view TRS_UEDITOR trs_paper_default trs_external"] \*::text').getall()  
Out[4]:
['呼伦贝尔市人民政府：',
'你市《关于〈根河市城市总体规划（2014-2030）〉部分地块修改成果批准实施的请示》（呼政报〔2019〕83 号）收悉。经研究，现批复如下：',
'一、同意《根河市城市总体规划（2019-2030）（2019 年修改版）》（以下简称《总体规划》）。',
'二、根河市人民政府应按照局部修改后的《总体规划》，进一步修改完善相关专项规划和控制性详细规划内容，确保规划有效实施。',
'三、根河市人民政府要进一步加强规划监督管理工作，根河市自然资源主管部门要依法实施规划统一管理。',
'专此批复。',
'2020 年 11 月 30 日',
'（此件公开发布）']

headers = {
'User-Agent': "Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/60.0",
'Referer': "http://www.nmg.gov.cn/col/col1686/index.html",
'Host':'www.nmg.gov.cn',
'Origin':'http://www.nmg.gov.cn'
}

**Shanxi_jin**

很多 pdf

total page 138

http://www.shanxi.gov.cn/sxszfxxgk/index_100.shtml

http://www.shanxi.gov.cn/sxszfxxgk/sxsrmzfzcbm/sxszfbgt/flfg_7203/szfgfxwj_7205/200808/t20080812_145981.shtml

response.css('td.affaires-doc-title a::attr(title)').getall()
response.css('td.affaires-doc-title a::attr(href').getall()
response.css('td.affaires-doc-title a::attr(href)').getall()
response.css('td.affaires-doc-sizes::text').getall()
response.css('td.affaires-doc-published::text').getall()
response.css('table.affairs-document-titbar').getall()
response.css('table.affairs-document-box').getall()
response.css('table.affairs-document-box')
response.css('table.affairs-document-box tr')
response.css('table.affairs-document-box tr')[1:]
response.css('table.affairs-document-box tr')[1:][0]
response.css('table.affairs-document-box tr')[1:][0].css('td.affaires-doc-title a::attr(href)').get()
response.css('table.affairs-document-box tr')[1:][0].css('td.affaires-doc-title a::attr(title)').get()
response.css('table.affairs-document-box tr')[1:][0].css('td.affaires-doc-sizes::text').get()
response.css('table.affairs-document-box tr')[1:][0].css('td.affaires-doc-published::text').get()

response.css('table.affairs-detail-head')
response.css('table.affairs-detail-head').get()
response.css('table.affairs-detail-head td')
len(response.css('table.affairs-detail-head td'))
response.css('table.affairs-detail-head td')[0].css('_::text').get()
response.css('div[style="FONT-SIZE: 16px; LINE-HEIGHT: 160%"])
response.css('div[style="FONT-SIZE: 16px; LINE-HEIGHT: 160%"]')
response.css('div[style="FONT-SIZE: 16px; LINE-HEIGHT: 160%"] _::text').getall()

**Shaanxi_shan**

http://www.shaanxi.gov.cn/zfxxgk/fdzdgknr/zcwj/szfgz/index_1.html 11

http://www.shaanxi.gov.cn/zfxxgk/fdzdgknr/zcwj/xzgfxwj/index_2.html 5

http://www.shaanxi.gov.cn/zfxxgk/fdzdgknr/zcwj/szfwj/szf/index_1.html 70

http://www.shaanxi.gov.cn/zfxxgk/fdzdgknr/zcwj/szfwj/szz/index_2.html 17

http://www.shaanxi.gov.cn/zfxxgk/fdzdgknr/zcwj/szfwj/szrz/index_3.html 134

http://www.shaanxi.gov.cn/zfxxgk/fdzdgknr/zcwj/szfwj/sztb/index_3.html 46

http://www.shaanxi.gov.cn/zfxxgk/fdzdgknr/zcwj/szfwj/szh/index_4.html 56

http://www.shaanxi.gov.cn/zfxxgk/fdzdgknr/zcwj/szfbgtwj/szbf/index_3.html 134

http://www.shaanxi.gov.cn/zfxxgk/fdzdgknr/zcwj/szfbgtwj/szbz/index_2.html 6

http://www.shaanxi.gov.cn/zfxxgk/fdzdgknr/zcwj/szfbgtwj/szbfmd/index_3.html 14

http://www.shaanxi.gov.cn/zfxxgk/fdzdgknr/zcwj/szfbgtwj/szbh/index_2.html 57

In [6]: response.css('ul[class="gov-item cf-otw"] li')[0].css('div[class="a-news otw lf"] a::attr(title)').get()  
Out[6]: '陕西省人民政府办公厅关于为在陕全国人大代表和住陕全国政协委员征集建议提案资料的通知'

In [7]: response.css('ul[class="gov-item cf-otw"] li')[0].css('div[class="a-news otw lf"] a::attr(href)').get()  
Out[7]: './201912/t20191220_1668190.html'

In [9]: response.css('ul[class="gov-item cf-otw"] li')[0].css('span[class="code-num otw lf"]::text').get().strip()  
Out[9]: '陕政办函〔2019〕197 号'

In [10]: response.css('ul[class="gov-item cf-otw"] li')[0].css('span[class="date rt"]::text').get().strip()  
Out[10]: '2019-12-20'

response.css('div#doc_left \*::text').getall()

**Ningxia**

该网站已接入<span style="font-size: 14px;color: #006cb8;"><strong>电信云堤&bull;网站安全防护服务</strong></span>，由于您使用的请求方法存在潜在安全风险，被云堤网站安全防护拦截。如果您有任何疑问或者认为这是一个误报，请您通过以下方式联系<span style="font-size: 14px;color: #006cb8;"><strong>7X24</strong></span>小时客服：

数据最后是用我个人 pc 爬取的

Total page 48

http://www.nx.gov.cn/zwgk/qzfwj/list.html
http://www.nx.gov.cn/zwgk/qzfwj/list_2.html

response.css('ul.nx-list')
response.css('ul.nx-list li')
len(response.css('ul.nx-list li')) == 20
response.css('ul.nx-list li a')
len(response.css('ul.nx-list li a'))
response.css('ul.nx-list li a::attr(href)')
len(response.css('ul.nx-list li span'))
len(response.css('ul.nx-list li span.date'))
len(response.css('ul.nx-list li div.nx-contmtab'))
len(response.css('ul.nx-list li div.nx-conmtab'))
len(response.css('ul.nx-list li div.nx-conmtab')[0].css('p'))
len(response.css('ul.nx-list li div.nx-conmtab')[3].css('p'))
response.css('ul.nx-list li div.nx-conmtab')[3].css('p')[0].css('span.tt')
response.css('ul.nx-list li div.nx-conmtab')[3].css('p')[0].css('span.tt::text').get()
response.css('ul.nx-list li div.nx-conmtab')[3].css('p')[0].css('span.value::text').get()
response.css('ul.nx-list li span::text').get()
response.css('ul.nx-list li a::attr(href)')
response.css('ul.nx-list li a::attr(href)').get()
response.css('ul.nx-list li a::attr(title)').get()

'发文字号：'

response.text
response.css('div.view')
response.css('div.view p \*::text').getall()

**Gansuu**

实际项目编程中注意文本为空的特殊情况

http://www.gansu.gov.cn/module/jslib/jquery/jpage/dataproxy.jsp?startrecord=82&endrecord=162&perpage=27&appid=1&webid=1&path=%2F&columnid=4729&sourceContentType=3&unitid=18064&webname=%E4%B8%AD%E5%9B%BD%C2%B7%E7%94%98%E8%82%83&permissiontype=0

headers = {
'User-Agent': "Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/60.0",
'Referer': "http://www.gansu.gov.cn/col/col4729/index.html",
"Host": "www.gansu.gov.cn",
"Origin":"http://www.gansu.gov.cn"
}
req = scrapy.Request(url = "http://www.gansu.gov.cn/module/jslib/jquery/jpage/dataproxy.jsp?startrecord=82&endrecord=162&perpage=27",headers = headers)
req = scrapy.Request(url = "http://www.gansu.gov.cn/module/jslib/jquery/jpage/dataproxy.jsp?startrecord=82&endrecord=162&perpage=27&appid=1&webid=1&path=%2F&columnid=4729&sourceContentType=3&unitid=18064&webname=%E4%B8%AD%E5%9B%BD%C2%B7%E7%94%98%E8%82%83&permissiontype=0",headers = headers)
fetch(req)
response.text
len('\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\ntotalRecord=714.0;totalPage = 27;dataStore = ')
import ast
l = ast.literal_eval(response.text[69:-1])
l
from scrapy.selector import Selector
Selector(text=l[0]).css('a')
Selector(text=l[0]).css('a::attr(href)').get()
Selector(text=l[0]).css('span::text')
Selector(text=l[0]).css('span::text').get()
Selector(text=l[0]).css('a::attr(title)').get()

response.css('div#zoom p \*::text').getall()

**Qinghai**

total page = 59

http://zwgk.qh.gov.cn/xxgk/fd/zfwj/index_2.html

In [3]: response.css('table[class="zctb"] tr')[1:][0].css('td')[0].css('a::attr(href)').get()  
Out[3]: 'http://zwgk.qh.gov.cn/xxgk/fd/zfwj/202009/t20200903_169560.html'

In [4]: response.css('table[class="zctb"] tr')[1:][0].css('td')[0].css('a::text').get()  
Out[4]: ' 青海省人民政府'

In [5]: response.css('table[class="zctb"] tr')[1:][0].css('td')[0].css('a \*::text').getall()  
Out[5]: [' 青海省人民政府', '关于王勇等同志职务任免的通知']

In [6]: response.css('table[class="zctb"] tr')[1:][0].css('td')[1].css('::text').get()  
Out[6]: '青政人〔2020〕12 号'

In [7]: response.css('table[class="zctb"] tr')[1:][0].css('td')[3].css('::text').get()  
Out[7]: '2020-09-03'

response.css('div#contentlf \*::text').getall()

**Xinjiang**

很多是复印件图片，没有文本，也不提供 pdf 下载

total page 34

http://www.xinjiang.gov.cn/xinjiang/gfxwj/zfxxgk_gknrz.shtml

response.css('div.gknr_list dd')
len(response.css('div.gknr_list dd'))
response.css('div.gknr_list dd')[0].css('a.attr(href)').get()
response.css('div.gknr_list dd')[0].css('a.attr(href)').get()
response.css('div.gknr_list dd')[0].css('a').get()
response.css('div.gknr_list dd')[0].css('a::attr(href)').get()
response.css('div.gknr_list dd')[0].css('a::attr(title)').get()
response.css('div.gknr_list dd')[0].css('span').get()
response.css('div.gknr_list dd')[0].css('span::text').get()

response.css('ul.clearfix')
response.css('ul.clearfix li')
response.css('ul.clearfix li')[0].css('_::text').getall()
response.css('ul.clearfix li')[-2].css('_::text').getall()
response.css('ul.clearfix li')[0].css('_::text').getall()[0].split('：')
response.css('ul.clearfix li')[-3].css('_::text').getall()[0].split('：')
response.css('div.gknbxq*detail p *::text)').getall()
response.css('div.gknbxq*detail *::text)').getall()
response.css('div.gknbxq_detail p::text)').getall()
response.css('div.gknbxq_detail p b::text)').getall()
response.css('div.gknbxq_detail p b::text').getall()
response.css('div.gknbxq_detail p \*::text').getall()

**Sichuan**

total page = 716

http://www.sc.gov.cn/10462/c102914/list_ft_2.shtml 7 规范性
http://www.sc.gov.cn/10462/c103043/stt_list_2.shtml 4 省政府
http://www.sc.gov.cn/10462/c103044/stt_list_2.shtml 14 川府发
http://www.sc.gov.cn/10462/c103045/stt_list_2.shtml 15 川府函
http://www.sc.gov.cn/10462/c103046/stt_list_2.shtml 15 川办发
http://www.sc.gov.cn/10462/c103047/stt_list_2.shtml 15 川办函
http://www.sc.gov.cn/10462/c103048/stt_list_2.shtml 2 修订

HTML

In [6]: response.css('div#content table#dash-table tr')[0].css('td')[1].css('a::attr(title)').get()  
Out[6]: '四川省人民政府办公厅印发《关于促进全省开发区改革和创新发展的实施意见》《四川省省级开发区设立、扩区和调位管理办法》《四川省开发区发展规划（2018—2022 年）》的通知'

In [7]: response.css('div#content table#dash-table tr')[0].css('td')[2].css('font::text').get()  
Out[7]: '(01-25)'

In [8]: response.css('div#content table#dash-table tr')[0].css('td')[1].css('a::attr(href)').get()  
Out[8]: '/10462/c103046//2019/1/30/50562b8042d6473e8c258465cdbfa0ab.shtml'

http://www.sc.gov.cn/10462/c103046//2015/11/26/eb959e9aaccb40fab15e7928c8f1597e.shtml

response.css('td[class=contText] \*::text').getall()

In [11]: response.css('td[bgcolor="#fbfbfb"] tr')[1].css('td')[1].css('\*::text').get().strip()  
Out[11]: '2015-11-08'

In [12]: response.css('td[bgcolor="#fbfbfb"] tr')[1].css('td')[3].css('\*::text').get().strip()  
Out[12]: '川办发〔2015〕94 号'

**Yunnan**

total page 27

http://www.yn.gov.cn/zwgk/zcwj/szfl/index_1.html 5

http://www.yn.gov.cn/zwgk/zcwj/yzf/index_41.html 42

http://www.yn.gov.cn/zwgk/zcwj/yzg/index.html 1

http://www.yn.gov.cn/zwgk/zcwj/yzh/index_1.html 7

http://www.yn.gov.cn/zwgk/zcwj/yunzf/index_1.html 12

http://www.yn.gov.cn/zwgk/zcwj/yzr/index_11.html 42

http://www.yn.gov.cn/zwgk/zcwj/yfmd/index.html 1

http://www.yn.gov.cn/zwgk/zcwj/yzfb/index_1.html 42

http://www.yn.gov.cn/zwgk/zcwj/yzbg/index_1.html 2

http://www.yn.gov.cn/zwgk/zcwj/yzbh/index_1.html 28

http://www.yn.gov.cn/zwgk/zcwj/yzbmd/index_1.html 5

http://www.yn.gov.cn/zwgk/zcwj/qtwj/index_1.html 5

In [3]: response.css('tbody tr')[1:][0]  
Out[3]: <Selector xpath='descendant-or-self::tbody/descendant-or-self::*/tr' data='<tr style="">\n\t\t\t\t\t      <td>云政报〔2019...'>

In [4]: response.css('tbody tr')[1:][0].css('td')[0]  
Out[4]: <Selector xpath='descendant-or-self::td' data='<td>云政报〔2019〕14号</td>'>

In [5]: response.css('tbody tr')[1:][0].css('td')[0].css('::text').get()  
Out[5]: '云政报〔2019〕14 号'

In [6]: response.css('tbody tr')[1:][0].css('td')[1].css('a::attr(href)').get()  
Out[6]: './201904/t20190416_144819.html'

In [8]: response.css('tbody tr')[1:][0].css('td')[1].css('a::text').get()  
Out[8]: '云南省人民政府关于 2018 年度法治政府建设情况的报告'

In [10]: response.css('tbody tr')[1:][0].css('td')[2].css('::text').get()  
Out[10]: '2019-04-11'

response.css('div[class="arti"] \*::text').getall()

# Guizhou

total page

http://www.guizhou.gov.cn/zwgk/zcfg/szfwj_8191/qff_8193/index_1.html

28

http://www.guizhou.gov.cn/zwgk/zcfg/gfxwj/index_2.html

17

In [5]: response.css('div.right-list-box ul li')[0].css('a::attr(href)')  
Out[5]: [<Selector xpath='descendant-or-self::a/@href' data='http://www.guizhou.gov.cn/zwgk/zcfg/s...'>]

In [6]: response.css('div.right-list-box ul li')[0].css('a::attr(href)').get()  
Out[6]: 'http://www.guizhou.gov.cn/zwgk/zcfg/szfwj_8191/qff_8193/201902/t20190212_2255555.html'

In [7]: response.css('div.right-list-box ul li')[0].css('a::attr(title)').get()  
Out[7]: '省人民政府关于建立涉农资金统筹整合长效机制的实施意见（黔府发〔2019〕4 号）'

In [8]: response.css('div.right-list-box ul li')[0].css('span::text').get()  
Out[8]: '2019-02-12 16:43'

response.css('div.view p \*::text').getall()

**Guangxi**

http://www.gxzf.gov.cn/igs/front/search/list.html?index=file2-index-alias&type=governmentdocuments&pageNumber=602&pageSize=10&filter[AVAILABLE]=true&filter[fileNum-like]=&filter[Effectivestate]=&filter[fileYear]=&filter[fileYear-lte]=&filter[FileName,DOCCONTENT,fileNum-or]=&siteId=14&filter[SITEID]=3&orderProperty=PUBDATE&orderDirection=desc

total page 602

{'filter': {'AVAILABLE': 'true',
'Effectivestate': None,
'FileName,DOCCONTENT,fileNum-or': None,
'SITEID': '3',
'fileNum-like': None,
'fileYear-lte': None,
'fileYear': None},
'**index': 'file2-index-alias',
'**type': 'governmentdocuments',
'pageable': {},
'queryFilter': {'filter': {'AVAILABLE': 'true',
'Effectivestate': None,
'FileName,DOCCONTENT,fileNum-or': None,
'SITEID': '3',
'fileNum-like': None,
'fileYear-lte': None,
'fileYear': None},
'fieldAndValues': None},
'hasFilter': True,
'page': {'content': [{'SITENAME': '自治区人民政府门户',
'fileNum': '其它',
'FileName': '广西壮族自治区人民政府关于加快我区国有粮食企业改革有关问题的通知',
'PUBDATE': '2006-08-20T18:59:36.000Z',
'IdxID': '000014349/2020-405310',
'CHNLDESC': '自治区人民政府文件',
'SITEID': 3,
'Effectivestate': '0',
'DOCCONTENT': '\u3000\u3000 桂政发〔2006〕17 号\u3000\u3000 各市、县人民政府，区直各委、办、厅、局：\u3000\u3000 近年来，各地各有关部门按照中央和自治区的部署，积极推行国有粮食企业政企分开，推进兼并重组，消化历史包袱，分流富余人员，建立健全法人治理结构，不少企业已成为自主经营、自负盈亏的市场主体，提高了市场竞争能力，更好地发挥了国有粮食购销企业主渠道作用，国有粮食企业改革取得了初步成效。但是，也有一些地方对国有粮食企业改革重视不够，企业&#8220;老人&#8221;、&#8220;老账&#8221;问题未解决，职工安置资金未落实，产权制度改革欠规范，致使我区国有粮食企业改革明显滞后于其他省区，明显滞后于其他国有企业。这不仅影响了我区粮食流通体制改革的进一步深化，不利于粮食市场的繁荣稳定，也严重制约了企业自身的持续发展。为进一步加快我区国有粮食企业改革，根据中央和自治区的有关文件精神，现就有关问题通知如下：\u3000\u3000 一、积极筹措资金，妥善安置国有粮食企业职工\u3000\u3000 妥善安置职工，是加快国有粮食企业改革的关键。国有粮食企业要全面实行劳动合同制，与职工通过平等协商签订劳动合同，在确定新的劳动关系前应与职工解除原劳动关系并支付经济补偿金。对不能上岗又不符合离岗退养条件的在职职工，企业按照政策发给经济补偿金后即解除其与原企业的劳动关系，职工按政策规定享受失业保险或城镇居民最低生活保障待遇，各级人民政府按照规定将其纳入当地就业工作规划。对距国家法定退休年龄 5 年以内的职工，经本人申请、企业批准，可办理离岗退养手续，企业参照退休人员基本养老金计发办法计算和发放离岗退养生活费，并按照规定继续为其缴纳各项社会保险费至达到国家法定退休年龄，然后再办理退休手续。企业退休人员按照规定由企业移交当地社区统一管理。企业改制为国有或国有控股企业的，离休干部由改制后的企业负责管理；改制为非国有控股企业或破产的，离休干部管理单位由当地党委和政府确定。国有粮食企业职工与企业依法解除劳动关系时，应按照规定一次性补缴欠缴的社会保险费。属于企业欠缴部分，由企业补缴；属于个人欠缴部分，由职工补缴。\u3000\u3000 安置国有粮食企业职工所需的资金，由市、县(市、区)人民政府依次从以下渠道筹措：(一)企业处置土地使用权所得收入、国有资本减持和产权转让收入；(二)自治区本级粮食风险基金补助；(三)在自治区财政厅等有关部门的审批额度内，从市、县(市、区)本级粮食风险基金中安排。通过上述渠道筹措资金仍有缺口的，可再依次通过以下渠道筹措：(一)本级粮食风险基金还有结余的，可向自治区财政厅提出申请，经批准后，动用本级粮食风险基金结余；(二)本级粮食风险基金没有结余的，可向自治区财政厅申请粮食风险基金借款，自治区财政厅视各市、县(市、区)的实际情况，从自治区本级粮食风险基金中安排借款，在以后年度逐步扣回；(三)财力相对较好的市、县(市、区)，可向自治区财政厅申请补助，市、县(市、区)本级财政按照 1：1 的比例先安排配套资金，自治区财政厅审核确定后，从自治区本级粮食风险基金中安排补助款。各地要设立国有粮食企业改革专项资金专户，专项用于安置国有粮食企业职工，包括支付职工的经济补偿金、社会保险费、欠发工资或生活费、医药费等。\u3000\u3000 二、严格政策规定，把国有粮食企业职工纳入社会保障体系\u3000\u3000 把国有粮食企业职工纳入社会保障体系，是加快我区国有粮食企业改革的重要保障。尚未参加社会保险的国有粮食企业，必须于 2006 年 6 月底前依法参加社会保险，企业和职工要按照规定缴纳社会保险费。不按照规定参加社会保险并缴纳社会保险费的，要按照《社会保险费征缴暂行条例》的有关规定处理。本通知下发前国有粮食企业欠缴的社会保险费应按照规定一次性补缴，职工基本养老保险欠费中应由企业缴费的部分，企业没有能力一次性补缴的，必须制定清欠补缴计划，在 3 年内由企业筹措资金或从财政补助资金中安排补齐。\u3000\u3000 原参加机关事业单位养老保险的企业化管理事业单位，其离退休人员养老保险待遇仍按《自治区人民政府办公厅转发自治区粮食局等部门关于我区国有粮食企业改革意见的通知》(桂政办发〔2002〕119 号)的规定执行，重新核定的养老保险待遇与原享受待遇的差额，尚未落实所需资金的，由当地政府协调解决。\u3000\u3000 三、解决&#8220;老账"问题，减轻国有粮食企业负担\u3000\u3000&#8220;老账&#8221;问题是制约国有粮食企业改革和发展的一个&#8220;瓶颈&#8221;，必须妥善解决。尚未完成国有粮食购销企业 1998 年 6 月 1 日后发生的政策性粮食财务挂账清理审计工作任务的市、县(市、区)，要按照中央和自治区的要求抓紧完成。在清理审计工作中，既要防止对政策性粮食财务挂账认定不足，又要避免人为增加政策性粮食财务挂账。已完成清理审计工作任务的市、县(市、区)，要做好将国有粮食购销企业政策性粮食财务挂账从企业剥离、上划到县级以上粮食行政管理部门集中管理的准备工作，确保挂账剥离工作有序彻底，数据客观准确，会计账目不乱。对企业经营性财务挂账，可按照&#8220;债随资产走&#8221;的原则，探索集中管理的有效形式，使企业卸掉包袱，盘活存量资产，为企业产权制度改革和发展创造条件。\u3000\u3000 四、依法规范操作，防止国有粮食企业国有资产流失\u3000\u3000 产权制度改革是国有粮食企业改革的核心。要以现有仓储设施为依托，优化企业布局和结构，改造和重组国有独资或国有控股粮食购销企业，作为政府实行粮食宏观调控的重要载体，不断增强其市场竞争力。承担政策性业务的粮食储备库和军粮供应企业，原则上不实行产权制度改革，仍保持国有独资，确需改革的必须保持国有控股，仍归口粮食行政管理部门管理。对其他国有粮食企业，应采取重组、联合、兼并、租赁、承包经营、合资、转让等多种形式，优化产权结构，实行投资主体多元化。国有粮食企业产权制度改革涉及国有资产处置，必须依法规范操作，防止国有资产流失。\u3000\u3000(一)制定产权制度改革方案。国有粮食企业产权制度改革方案原则上由企业国有产权持有单位制订，报同级人民政府审批；尚未实行政企分开的企业，由粮食行政管理部门负责组织制订方案，报同级国有资产监督管理机构审批，其中改制为非国有企业的由国有资产监督管理机构审核后报同级人民政府审批。产权制度改革方案要先提交职工代表大会或全体职工大会审议，充分听取职工意见，并按照有关规定及时向广大职工公布。产权制度改革方案中的职工安置方案须按照同级劳动保障部门的审核意见修改完善并经职工代表大会或全体职工大会审议通过。\u3000\u3000(二)进行清产核资。对国有粮食企业各类资产、负债进行全面认真清查，核实和界定国有资本金及其权益。涉及资产损失认定与处理的，按照规定的审批程序办理。清产核资结果经国有产权持有单位认定，并经国有资产监督管理机构确认后，自清产核资基准日起 2 年内有效，在有效期内企业实施产权制度改革不再另行组织清产核资。\u3000\u3000(三)做好财务审计和资产评估工作。国有粮食企业实施产权制度改革须由审批改革方案的单位确定的中介机构进行财务审计和资产评估。改制为非国有企业的，应按照国家有关规定对企业法定代表人进行离任审计。财务审计和离任审计工作应由两家会计师事务所分别承担，分别出具审计报告。企业的专利权、非专利技术、商标权、商誉等无形资产要纳入资产评估范围。评估报告由依照有关规定批准企业实行产权制度改革和转让国有产权的单位核准。\u3000\u3000(四)严格土地使用权处置程序。国有粮食企业产权制度改革涉及土地使用权的，须进行土地确权登记并明确处置方式。进入企业改制资产范围的土地使用权须经具备土地估价资格的中介机构进行评估，并按照国家有关规定备案。涉及国有划拨土地使用权的，必须按照国家土地管理有关规定办理处置审批手续。\u3000\u3000(五)规范国有产权转让。国有粮食企业向其他国有企业转让国有产权，须经同级国有资产监督管理机构批准后方可以划拨方式进行。以划拨以外方式转让国有产权的，应严格按照《企业国有产权转让管理暂行办法》(国务院国资委、财政部令第 3 号)、《企业国有产权向管理层转让暂行规定》(国资发产权〔2005〕78 号)及《广西壮族自治区人民政府关于印发(广西壮族自治区企业国有产权转让监督管理办法)的通知》(桂政发〔2005〕60 号)等有关文件的规定，在省级以上国有资产监督管理机构确定的产权交易机构公开进行，规范操作。\u3000\u3000 五、转换经营机制，发挥国有粮食购销企业的主渠道作用\u3000\u3000 国有粮食企业要通过改革建立有效的约束和激励机制，转换经营机制，创新经营方式，真正成为自主经营、自负盈亏的市场主体。国有粮食购销企业要充分利用自身的仓储、运输设施优势和所享受的国家有关优惠政策，面向市场，主动服务，继续发挥粮食流通的主渠道作用，确保粮食市场稳定和粮食安全。粮食主产区的国有粮食购销企业要改进服务，与农民建立稳定的粮食购销关系，积极收购粮食，掌握粮源，促进农民增产增收。粮食主销区的国有粮食购销企业要积极从粮食主产区采购粮食，保障粮食市场供应，维护粮食市场稳定。\u3000\u3000 各地各有关部门要积极支持和鼓励国有粮食购销企业在粮食流通中发挥主渠道作用，建立产销区之间的互信机制，促进产区粮食向销区流通。要加强对粮食市场的监管，督促企业服从政府对粮食市场的宏观调控，维护正常的粮食流通秩序。要在项目开发、技术引进和创新、土地使用、财政、税收和信贷等方面给予优惠政策，积极培育、扶持产业化龙头企业，引导企业与农民建立利益共享、风险共担的合作机制，推进粮食产业化经营，提高效益。\u3000\u3000 六、切实加强领导，确保国有粮食企业改革的顺利进行\u3000\u3000 国有粮食企业改革是粮食工作行政首长负责制的重要内容之一，涉及面广，政策性强，各市、县(市、区)人民政府要切实加强领导，承担起具体组织本地区国有粮食企业改革的责任，建立健全领导机制和工作机制，结合实际，制定和完善本地区国有粮食企业改革的总体方案，分类指导，扎实推进。各级发展改革、粮食、财政、劳动保障、国资、国土资源、审计、工商、税务等部门和农业发展银行要密切配合，认真研究制定和落实有关优惠政策，在资金安排、税费减免、手续简化等方面全力支持国有粮食企业改革。各地要充分利用现有粮食购销网点和粮食产业化经营的优势，开展多种经营和招商引资，努力增加就业岗位，为国有粮食企业下岗失业人员的再就业创造机会。要加强职工思想政治工作，维护职工合法权益，妥善处理改革、发展和稳定的关系，确保国有粮食企业改革的顺利进行。\u3000\u3000 广西壮族自治区人民政府\u3000\u3000 二ＯＯ六年三月十四日',
'AVAILABLE': True,
'DOCID': 1508649,
'highlight': {},
'SITECLASS': '',
'SITETYPE': '区政府',
'DOCTITLE': '广西壮族自治区人民政府关于加快我区国有粮食企业改革有关问题的通知',
'fileYear': '2006',
'FileType': 20,
'DOCPUBURL': 'http://www.gxzf.gov.cn/zfwj/zzqrmzfwj_34845/t1508733.shtml',
'publisher': '广西壮族自治区人民政府办公厅',
'trs_warehouse_time': '2020-10-12T08:31:57.167Z',
'_id': '1508649',
'TYPE': '文件'}],
'total': '6014',
'pageSize': 10,
'pageNumber': 602,
'searchProperty': None,
'searchValue': None,
'orderProperty': 'PUBDATE',
'orderDirection': 'desc',
'totalPages': 602}}

In [22]: response.css('ul.more-list tr')[1:][4*29].css('a::text').get()  
Out[22]: '\n 广西壮族自治区人民政府\r\n 关于欧军、林春同志任免职的通知\r\n（桂政干〔2020〕68 号）\n '

In [23]: response.css('ul.more-list tr')[1:][4*29].css('td')  
Out[23]:
[<Selector xpath='descendant-or-self::td' data='<td>\n 30\n ...'>,
<Selector xpath='descendant-or-self::td' data='<td align="left" onmouseenter="td_ove...'>,
<Selector xpath='descendant-or-self::td' data='<td><strong>发文单位：</strong>\n ...'>,
<Selector xpath='descendant-or-self::td' data='<td><strong>成文日期：</strong>\n ...'>,
<Selector xpath='descendant-or-self::td' data='<td colspan="2"><strong>标\u3000\u3000 题：</strong...'>,
<Selector xpath='descendant-or-self::td' data='<td><strong>发文字号：</strong>\n ...'>,
<Selector xpath='descendant-or-self::td' data='<td><strong>发布日期：</strong>\n ...'>,
<Selector xpath='descendant-or-self::td' data='<td>\n ...'>,
<Selector xpath='descendant-or-self::td' data='<td>\n 有效\n ...'>,
<Selector xpath='descendant-or-self::td' data='<td>\n ...'>,
<Selector xpath='descendant-or-self::td' data='<td>\n ...'>]

In [24]: response.css('ul.more-list tr')[1:][4*29].css('td')[1].css('::text').get()  
Out[24]: '\n '

In [25]: response.css('ul.more-list tr')[1:][4*29].css('td')[-5].css('::text').get()  
Out[25]: '发布日期：'

In [26]: response.css('ul.more-list tr')[1:][4*29].css('td')[-4].css('::text').get()  
Out[26]: '\n 桂政干〔\n 2020〕\n 68 号\n '

In [27]: response.css('ul.more-list tr')[1:][4*29].css('td')[-2].css('::text').get()  
Out[27]: '\n 2020 年 02 月 14 日\n

response.css('div.article-con p \*::text').getall()

**Guangdong**

total page 205

http://www.gd.gov.cn/zwgk/wjk/qbwj/index_2.html

In [3]: response.css('div.viewList ul li')[0].css('a::attr(href)').get()  
Out[3]: 'http://www.gd.gov.cn/zwgk/wjk/qbwj/yfb/content/post_2894098.html'

In [4]: response.css('div.viewList ul li')[0].css('a::text').get()  
Out[4]: '广东省人民政府办公厅关于印发广东省加快半导体及集成电路产业发展若干意见的通知'

In [5]: response.css('div.viewList ul li')[0].css('span.wh::text').get()  
Out[5]: '粤府办〔2020〕2 号'

In [6]: response.css('div.viewList ul li')[0].css('span.date::text').get()  
Out[6]: '2020-02-13'

response.css('div.zw p \*::text').getall()

**Hunan**

total page
http://www.hunan.gov.cn/hnszf/xxgk/wjk/szfwj/wjk_glrb_34.html
34
http://www.hunan.gov.cn/hnszf/xxgk/wjk/szfbgt/wjk_glrb_34.html
34

In [3]: response.css('tbody tr')[0].css('a::attr(href)').get()  
Out[3]: '/hnszf/xxgk/wjk/szfwj/200908/t20090826_239811.html'

In [4]: response.css('tbody tr')[0].css('a::text').get()  
Out[4]: '湖南省人民政府关于做好第六次全国人口普查工作的通知'

In [5]: response.css('tbody tr')[0].css('td')[-2].css('::text').get()  
Out[5]: '2009-08-04'

In [6]: response.css('tbody tr')[0].css('td')[-3].css('::text').get()  
Out[6]: "var fileNum='湘政发 〔2009〕30 号';if(fileNum!='null'){document.write(fileNum)}"

In [7]: response.css('tbody tr')[0].css('td')[-3].css('::text').get().split("'")[1]

response.css('div.TRS_PreAppend p \*::text').getall()

**Hubei**

http://www.hubei.gov.cn/igs/front/search/list.html?filter[FileName,DOCCONTENT,fileNum-or]=&pageNumber=4&pageSize=10&siteId=50&index=hbsrmzf-index-alias&type=governmentdocuments&filter[CHNLDESC]=&filter[fileYear]=&filter[fileYear-lte]=&filter[SITEID]=54&filter[CNAME]=&orderProperty=PUBDATE&orderDirection=desc&MmEwMD=4khp3EogDRyXCQnl7uG6zBIUNXk6_edeT6aGBf1NPP8OGt3S8PPBEpheaxOK4qtNCa1V.EYtI_.lexlJZIPC.EbeUlbaO0uXDzR_ikueHsEGHZ8OIWAzQsasy6Pjs5PXNl36ZkvA8JBUXxDn14wB5tQTdihJdorP88uNbV2IxDPb.O5ROkzGYU3k7S6cOeFUXYcAf9LeCn.im59VR9oGErB2qOMLXLImHPHJC5f4y6zeW2dUIR4km9sMTWfXhtbT6cnaUZwiW4J0kWs29B87NJEuanj5ZZhDp7coylrR9UZAyJBB5Jm0muIDq_GnhCv9QeSzrSCGv6Ky8L_YdOMUp_u6GatAbl1oa0mv0PGGYzqBcjrT6hQ_aJhHgh08x2JMQtayfImXbEEpKfvtUo4ZZYn7sYt1N_GuFta95f1.Jd7B4bHn4uzrKdL2tjdze9rRh._.RTFr6_ljnCpfqyzemLPM4

http://www.hubei.gov.cn/igs/front/search/list.html?filter[FileName,DOCCONTENT,fileNum-or]=&pageNumber=6&pageSize=10&siteId=50&index=hbsrmzf-index-alias&type=governmentdocuments&filter[CHNLDESC]=&filter[fileYear]=&filter[fileYear-lte]=&filter[SITEID]=54&filter[CNAME]=&orderProperty=PUBDATE&orderDirection=desc&MmEwMD=4sIVR3seoxz.6WbrzO0n7dh1L5Un4z.g0v92XSD7OntbfFW0InCjxrIgSR6s_A876GDpj3rH8jdrZRAEeHCuj3ngKR0xj.xfq3UQQa4vo_5S96U.BU_lh.7hOmILB2MvRqQ4dZkdko.9pBH2lksUw2D6QNnxQNFnciNprPpJDQ3N0uLN8jP8l.BJz9a6UKU8VfsC55rv1o_4yCHlCEx9qb7o2FYNPqwgZoy60b0HeOtMHEEAnlENVkJPKogE1JuZl9I9iCZwF4R0n8m2fouVWtnmQAbAVaR5OhlqzfCJiP7bubgYaZO1w_1wpihd1D23M_OWXNxHKHzu8jiQ5g2Q34.PIet_uELrVaYTIJImbuxAkMAtLkJO6Nnq7BYUCg772yAKe2G7rZtN8eHRq.RQnmQlX2ZpXXZG2wF2ODvpyQGrw7v1a2LgUkBxdVVTVcwQvmIW4zXsu_wIFthorLbOjKw4L

cookie = {
"FSSBBIl1UgzbN7N80S":"bUU9HTDtknT3eWohpn7aYBk7k5POLVrW5Q8.C2kOwojIfXDhvNHwZmTx8lHn8_Y9", "Hm_lvt_5544783ae3e1427d6972d9e77268f25d":"1585408324", "token":"081f1405-45e2-4539-96c2-94add9b6b215","uuid":"081f1405-45e2-4539-96c2-94add9b6b215", "\_trs_uv":"k8br6wjg_3027_60lu","\_trs_ua_s_1":"k8br6wjg_3027_avg", "Hm_lpvt_5544783ae3e1427d6972d9e77268f25d":"1585408340","dataHide2":"22e65282-2deb-4725-87d4-d68222591f97",
"FSSBBIl1UgzbN7N80T":"442F_aNu9fU2V9QHihiZHUSQhKzZ3mpCUH8.JRZPqFaLcnC_ZFW9jN2C1SJwRg9PVEZIxa4recmHISjD8vWexaECTXAYNvTKlwIiIWZObBwAD4bjJ1mQhs_L_L37wAmC3yneW_RRYhAUzK4a4BeNSFloZSFdhwIo9e2kbPATqQ8bMGmTSdU00VFhzVK5ybPm9aQI5Iy5zsJL_dor6pL.R7jqMBLyubMceC45V9.MWz9VeMsbTufJ0pLE2K6_UI2MtvbfRrWuW2mrJpVdvZZm2nB6NnOQhdhhPtGk6mGiLWn9732XlxAWvOLTXGz_hZCDobxDqOjb90_3bqo.BECy8Nb89haPBUjF_ax_3YvM1DfDF.AbWWY0N6x_mSakeSUmYm9g9PQwrrg130ceiIG3q6Z7x"
}

headers = {
'User-Agent': "Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/60.0",
'Referer': "http://www.hubei.gov.cn/site/hubei/search.html?WxUg5ztDmi=1585408322959",
'Host':www.hubei.gov.cn,
}

headers = {
'User-Agent': "Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/60.0",
'Referer': "http://www.hubei.gov.cn/site/hubei/search.html?WxUg5ztDmi=1585408322959",
'Host':'www.hubei.gov.cn',
}
req = scrapy.Request(url='http://www.hubei.gov.cn/igs/front/search/list.html?filter[FileName,DOCCONTENT,fileNum-or]=&pageNumber=4&pageSize=10&siteId=50&index=hbsrmzf-index-alias&type=governmentdocuments&filter[CHNLDESC]=&filter[fileYear]=&filter[fileYear-lte]=&filter[SITEID]=54&filter[CNAME]=&orderProperty=PUBDATE&orderDirection=desc&MmEwMD=4khp3EogDRyXCQnl7uG6zBIUNXk6_edeT6aGBf1NPP8OGt3S8PPBEpheaxOK4qtNCa1V.EYtI_.lexlJZIPC.EbeUlbaO0uXDzR_ikueHsEGHZ8OIWAzQsasy6Pjs5PXNl36ZkvA8JBUXxDn14wB5tQTdihJdorP88uNbV2IxDPb.O5ROkzGYU3k7S6cOeFUXYcAf9LeCn.im59VR9oGErB2qOMLXLImHPHJC5f4y6zeW2dUIR4km9sMTWfXhtbT6cnaUZwiW4J0kWs29B87NJEuanj5ZZhDp7coylrR9UZAyJBB5Jm0muIDq_GnhCv9QeSzrSCGv6Ky8L_YdOMUp_u6GatAbl1oa0mv0PGGYzqBcjrT6hQ_aJhHgh08x2JMQtayfImXbEEpKfvtUo4ZZYn7sYt1N_GuFta95f1.Jd7B4bHn4uzrKdL2tjdze9rRh._.RTFr6_ljnCpfqyzemLPM4',headers = headers)
fetch(req)
headers = {
'User-Agent': "Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/60.0",
'Referer': "http://www.hubei.gov.cn/site/hubei/search.html?WxUg5ztDmi=1585408322959",
'Host':"www.hubei.gov.cn",
"Cookie": "Secure; FSSBBIl1UgzbN7N80S=bUU9HTDtknT3eWohpn7aYBk7k5POLVrW5Q8.C2kOwojIfXDhvNHwZmTx8lHn8*Y9; Secure; Hm_lvt_5544783ae3e1427d6972d9e77268f25d=1585408324; token=081f1405-45e2-4539-96c2-94add9b6b215; uuid=081f1405-45e2-4539-96c2-94add9b6b215; \_trs_uv=k8br6wjg_3027_60lu; \_trs_ua_s_1=k8br6wjg_3027_avg; Hm_lpvt_5544783ae3e1427d6972d9e77268f25d=1585408340; dataHide2=22e65282-2deb-4725-87d4-d68222591f97; FSSBBIl1UgzbN7N80T=4chrQxoLc3y5nwnVLnGvNXIozBkv5ZdzSCaa.G1ybO8u9h3fFOPdWAhz0EODdrtynS1lBxYFM4.VyElwg8PbBxbzsVozgD4fMB6ywNMwjahnHDkmTVpTVxLvtLims.uiZIka90VU2FzBO3RWO1H0RsbqHafXynQ_AcX20Th19FdEULoBexVaHwwYrCIKq5XogACvojsb0MrPvflemAzrkTABn5xjTF9lQmOi41Zj0faCAt2pfS89Hsmtidob.eTeX91zR3fVOPz9QIZGnCtZSvb3ej3iMpyLVH1YTfy6JGxFnAwjQp0JCASiBqi.QK1CSc.iDr3Qy6AN.eVUG.MDdZLavvTm0Od7GThwgCCC4UnClwCNrFfaGu5he9pNLp1yXNhhnFxQzAyL3bbrjD8hb2Jfa",
}
req = scrapy.Request(url='http://www.hubei.gov.cn/igs/front/search/list.html?filter[FileName,DOCCONTENT,fileNum-or]=&pageNumber=4&pageSize=10&siteId=50&index=hbsrmzf-index-alias&type=governmentdocuments&filter[CHNLDESC]=&filter[fileYear]=&filter[fileYear-lte]=&filter[SITEID]=54&filter[CNAME]=&orderProperty=PUBDATE&orderDirection=desc&MmEwMD=4khp3EogDRyXCQnl7uG6zBIUNXk6_edeT6aGBf1NPP8OGt3S8PPBEpheaxOK4qtNCa1V.EYtI*.lexlJZIPC.EbeUlbaO0uXDzR*ikueHsEGHZ8OIWAzQsasy6Pjs5PXNl36ZkvA8JBUXxDn14wB5tQTdihJdorP88uNbV2IxDPb.O5ROkzGYU3k7S6cOeFUXYcAf9LeCn.im59VR9oGErB2qOMLXLImHPHJC5f4y6zeW2dUIR4km9sMTWfXhtbT6cnaUZwiW4J0kWs29B87NJEuanj5ZZhDp7coylrR9UZAyJBB5Jm0muIDq_GnhCv9QeSzrSCGv6Ky8L_YdOMUp_u6GatAbl1oa0mv0PGGYzqBcjrT6hQ_aJhHgh08x2JMQtayfImXbEEpKfvtUo4ZZYn7sYt1N_GuFta95f1.Jd7B4bHn4uzrKdL2tjdze9rRh.*.RTFr6_ljnCpfqyzemLPM4',headers = headers)
fetch(req)
req = scrapy.Request(url='http://www.hubei.gov.cn/igs/front/search/list.html?filter[FileName,DOCCONTENT,fileNum-or]=&pageNumber=6&pageSize=10&siteId=50&index=hbsrmzf-index-alias&type=governmentdocuments&filter[CHNLDESC]=&filter[fileYear]=&filter[fileYear-lte]=&filter[SITEID]=54&filter[CNAME]=&orderProperty=PUBDATE&orderDirection=desc&MmEwMD=4sIVR3seoxz.6WbrzO0n7dh1L5Un4z.g0v92XSD7OntbfFW0InCjxrIgSR6s_A876GDpj3rH8jdrZRAEeHCuj3ngKR0xj.xfq3UQQa4vo_5S96U.BU_lh.7hOmILB2MvRqQ4dZkdko.9pBH2lksUw2D6QNnxQNFnciNprPpJDQ3N0uLN8jP8l.BJz9a6UKU8VfsC55rv1o_4yCHlCEx9qb7o2FYNPqwgZoy60b0HeOtMHEEAnlENVkJPKogE1JuZl9I9iCZwF4R0n8m2fouVWtnmQAbAVaR5OhlqzfCJiP7bubgYaZO1w_1wpihd1D23M_OWXNxHKHzu8jiQ5g2Q34.PIet_uELrVaYTIJImbuxAkMAtLkJO6Nnq7BYUCg772yAKe2G7rZtN8eHRq.RQnmQlX2ZpXXZG2wF2ODvpyQGrw7v1a2LgUkBxdVVTVcwQvmIW4zXsu_wIFthorLbOjKw4L',headers = headers)
fetch(req)

cookie = {
"FSSBBIl1UgzbN7N80S":"bUU9HTDtknT3eWohpn7aYBk7k5POLVrW5Q8.C2kOwojIfXDhvNHwZmTx8lHn8_Y9", "Hm_lvt_5544783ae3e1427d6972d9e77268f25d":"1585408324", "token":"081f1405-45e2-4539-96c2-94add9b6b215","uuid":"081f1405-45e2-4539-96c2-94add9b6b215", "\_trs_uv":"k8br6wjg_3027_60lu","\_trs_ua_s_1":"k8br6wjg_3027_avg", "Hm_lpvt_5544783ae3e1427d6972d9e77268f25d":"1585408340","dataHide2":"22e65282-2deb-4725-87d4-d68222591f97",
"FSSBBIl1UgzbN7N80T":"442F_aNu9fU2V9QHihiZHUSQhKzZ3mpCUH8.JRZPqFaLcnC_ZFW9jN2C1SJwRg9PVEZIxa4recmHISjD8vWexaECTXAYNvTKlwIiIWZObBwAD4bjJ1mQhs_L_L37wAmC3yneW_RRYhAUzK4a4BeNSFloZSFdhwIo9e2kbPATqQ8bMGmTSdU00VFhzVK5ybPm9aQI5Iy5zsJL_dor6pL.R7jqMBLyubMceC45V9.MWz9VeMsbTufJ0pLE2K6_UI2MtvbfRrWuW2mrJpVdvZZm2nB6NnOQhdhhPtGk6mGiLWn9732XlxAWvOLTXGz_hZCDobxDqOjb90_3bqo.BECy8Nb89haPBUjF_ax_3YvM1DfDF.AbWWY0N6x_mSakeSUmYm9g9PQwrrg130ceiIG3q6Z7x"
}
req = scrapy.Request(url='http://www.hubei.gov.cn/igs/front/search/list.html?filter[FileName,DOCCONTENT,fileNum-or]=&pageNumber=6&pageSize=10&siteId=50&index=hbsrmzf-index-alias&type=governmentdocuments&filter[CHNLDESC]=&filter[fileYear]=&filter[fileYear-lte]=&filter[SITEID]=54&filter[CNAME]=&orderProperty=PUBDATE&orderDirection=desc&MmEwMD=4sIVR3seoxz.6WbrzO0n7dh1L5Un4z.g0v92XSD7OntbfFW0InCjxrIgSR6s_A876GDpj3rH8jdrZRAEeHCuj3ngKR0xj.xfq3UQQa4vo_5S96U.BU_lh.7hOmILB2MvRqQ4dZkdko.9pBH2lksUw2D6QNnxQNFnciNprPpJDQ3N0uLN8jP8l.BJz9a6UKU8VfsC55rv1o_4yCHlCEx9qb7o2FYNPqwgZoy60b0HeOtMHEEAnlENVkJPKogE1JuZl9I9iCZwF4R0n8m2fouVWtnmQAbAVaR5OhlqzfCJiP7bubgYaZO1w_1wpihd1D23M_OWXNxHKHzu8jiQ5g2Q34.PIet_uELrVaYTIJImbuxAkMAtLkJO6Nnq7BYUCg772yAKe2G7rZtN8eHRq.RQnmQlX2ZpXXZG2wF2ODvpyQGrw7v1a2LgUkBxdVVTVcwQvmIW4zXsu_wIFthorLbOjKw4L',headers = headers,cookies=cookie)
fetch(req)

http://www.hubei.gov.cn/site/hubei/search.html?WxUg5ztDmi=1585408322959

headers = {
'User-Agent': "Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/60.0",
'Referer': "http://www.hubei.gov.cn/site/hubei/search.html?WxUg5ztDmi=1585408322959",
'Host':"www.hubei.gov.cn",
"Cookie": "Secure; FSSBBIl1UgzbN7N80S=bUU9HTDtknT3eWohpn7aYBk7k5POLVrW5Q8.C2kOwojIfXDhvNHwZmTx8lHn8_Y9; Secure; Hm_lvt_5544783ae3e1427d6972d9e77268f25d=1585408324; token=081f1405-45e2-4539-96c2-94add9b6b215; uuid=081f1405-45e2-4539-96c2-94add9b6b215; \_trs_uv=k8br6wjg_3027_60lu; \_trs_ua_s_1=k8br6wjg_3027_avg; Hm_lpvt_5544783ae3e1427d6972d9e77268f25d=1585408340; dataHide2=22e65282-2deb-4725-87d4-d68222591f97; FSSBBIl1UgzbN7N80T=4chrQxoLc3y5nwnVLnGvNXIozBkv5ZdzSCaa.G1ybO8u9h3fFOPdWAhz0EODdrtynS1lBxYFM4.VyElwg8PbBxbzsVozgD4fMB6ywNMwjahnHDkmTVpTVxLvtLims.uiZIka90VU2FzBO3RWO1H0RsbqHafXynQ_AcX20Th19FdEULoBexVaHwwYrCIKq5XogACvojsb0MrPvflemAzrkTABn5xjTF9lQmOi41Zj0faCAt2pfS89Hsmtidob.eTeX91zR3fVOPz9QIZGnCtZSvb3ej3iMpyLVH1YTfy6JGxFnAwjQp0JCASiBqi.QK1CSc.iDr3Qy6AN.eVUG.MDdZLavvTm0Od7GThwgCCC4UnClwCNrFfaGu5he9pNLp1yXNhhnFxQzAyL3bbrjD8hb2Jfa",
}

**Jiangxi**

Ok

**Anhui**

安徽也没爬成功

total page 448

In [4]: response.css('div.xxgk_navli')[0].css('a::attr(href)').get()  
Out[4]: 'http://www.ah.gov.cn/zmhd/xwfbhx/8288151.html'

In [5]: response.css('div.xxgk_navli')[0].css('a::attr(title)').get()  
Out[5]: '安徽省 2020 年 3·15 国际消费者权益日活动新闻发布会'

In [6]: response.css('div.xxgk_navli')[0].css('span.syh::text').get()

In [7]: response.css('div.xxgk_navli')[0].css('span.date::text').get()  
Out[7]: '\r\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t2020-03-13\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t'

In [7]: response.css('tbody')[0].css('td')[0].css('::text').getall()  
Out[7]: ['00298627-2/202003-00010']

In [8]: response.css('tbody')[0].css('th')[0].css('::text').getall()  
Out[8]: ['索', '引', '号：\n ']

In [9]: response.css('tbody')[0].css('th')[-2].css('::text').getall()  
Out[9]: ['文', '号：']

response.css('div.wzcon p \*::text').getall()

**Zhejiang**

total page 509

http://www.zj.gov.cn/module/xxgk/search.jsp?infotypeId=&jdid=3096&area=000014349&divid=div1551294&vc_title=&vc_number=&sortfield=,compaltedate:0&currpage=3&vc_filenumber=&vc_all=&texttype=0&fbtime=&texttype=0&fbtime=&vc_all=&vc_filenumber=&vc_title=&vc_number=&currpage=3&sortfield=,compaltedate:0

http://www.zj.gov.cn/module/xxgk/search.jsp?infotypeId=&jdid=3096&area=000014349&divid=div1551294&vc_title=&vc_number=&sortfield=,compaltedate:0&currpage={0}&vc_filenumber=&vc_all=&texttype=0&fbtime=&texttype=0&fbtime=&vc_all=&vc_filenumber=&vc_title=&vc_number=&currpage=3&sortfield=,compaltedate:0

In [5]: response.css('tr')[4:-2][0].css('a::attr(href)').get()  
Out[5]: 'http://www.zj.gov.cn/art/2020/2/14/art_1551345_41917743.html'

In [6]: response.css('tr')[4:-2][0].css('a::attr(title)').get()

In [7]: response.css('tr')[4:-2][0].css('a::attr(mc)').get()  
Out[7]: '浙江省人民政府关于朱林森等职务任免的通知'

In [8]: response.css('tr')[4:-2][0].css('a::attr(wh)').get()  
Out[8]: '浙政干〔2019〕49 号'

In [9]: response.css('tr')[4:-2][0].css('a::attr(rq)').get()  
Out[9]: '2019-12-30'

response.css('div.bt_content p \*::text').getall()

**Fujian**

total page 655

http://www.fujian.gov.cn/was5/web/search?channelid=229105&templet=docs.jsp&sortfield=-pubdate&classsql=chnlid%3E22054*chnlid%3C22084&prepage=10&page={0}

raw = response.text
raw.remove('\n')
raw.replace('\n','')
raw.replace('\r','')
raw = raw.replace('\r','')
raw = raw.replace('\n','')
json.loads(raw)

response.css('div.xl-bk p \*::text').getall()

**Jiangsu**

total page 190

http://www.jiangsu.gov.cn/col/col76841/index.html?uid=297589&pageNum=1&col=1&appid=1&webid=1&path=%2F&columnid=76841&sourceContentType=1&unitid=297589&webname=%E6%B1%9F%E8%8B%8F%E7%9C%81%E4%BA%BA%E6%B0%91%E6%94%BF%E5%BA%9C&permissiontype=0

headers = {
'User-Agent': "Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/60.0",
'Referer': "http://www.jiangsu.gov.cn/col/col76841/index.html?uid=297589&pageNum=3",
"Host": "www.jiangsu.gov.cn",
"Origin":"http://www.jiangsu.gov.cn"
}

http://www.jiangsu.gov.cn/module/web/jpage/dataproxy.jsp?col=1&appid=1&webid=1&path=%2F&columnid=76841&sourceContentType=1&unitid=297589&webname=%E6%B1%9F%E8%8B%8F%E7%9C%81%E4%BA%BA%E6%B0%91%E6%94%BF%E5%BA%9C&permissiontype=0

Selector(text = response.css('div#297589 \*::text').get()).css('record')

n [18]: response.css('::text').getall()[2:]  
Out[18]:
['<li><a title="省政府关于进一步深化高考综合改革的若干意见" target="_blank" href="http://www.jiangsu.gov.cn/art/2020/3/23/art_46143_9019230.html">省政府关于进一步深化高考综合改革的若干意见</a><b>2020-03-23</b></li>',
'<li><a title="省政府办公厅关于印发江苏省突发环境事件应急预案的通知" target="_blank" href="http://www.jiangsu.gov.cn/art/2020/3/19/art_46144_9017328.html">省政府办公厅关于印发江苏省突发环境事件应急预案的通知</a><b>2020-03-19</b></li>',
'<li><a title="省政府办公厅关于印发江苏省太湖蓝藻暴发应急预案的通知" target="_blank" href="http://www.jiangsu.gov.cn/art/2020/3/19/art_46144_9017327.html">省政府办公厅关于印发江苏省太湖蓝藻暴发应急预案的通知</a><b>2020-03-19</b></li>',
'<li><a title="省政府办公厅关于印发省政府 2020 年立法工作计划的通知" target="_blank" href="http://www.jiangsu.gov.cn/art/2020/3/19/art_46144_9017297.html">省政府办公厅关于印发省政府 2020 年立法工作计划的通知</a><b>2020-03-19</b></li>']

In [19]: Selector(text = response.css('::text').getall()[2:][0]).css('a::attr(title)').get()  
Out[19]: '省政府关于进一步深化高考综合改革的若干意见'

In [20]: Selector(text = response.css('::text').getall()[2:][0]).css('a::attr(href)').get()  
Out[20]: 'http://www.jiangsu.gov.cn/art/2020/3/23/art_46143_9019230.html'

In [21]: Selector(text = response.css('::text').getall()[2:][0]).css('b::text').get()  
Out[21]: '2020-03-23'

---

In [45]: Selector(text = response.css('div#297589 _::text').get()).css('_')[7:][0].css('a')  
Out[45]: [<Selector xpath='descendant-or-self::a' data='<a title="省政府关于进一步深化高考综合改革的若干意见" targ...'>]

In [46]: Selector(text = response.css('div#297589 _::text').get()).css('_')[7:][0].css('b')  
Out[46]: [<Selector xpath='descendant-or-self::b' data='<b>2020-03-23</b>'>]

In [47]: Selector(text = response.css('div#297589 _::text').get()).css('_')[7:][1].css('b')  
Out[47]: []

In [48]: Selector(text = response.css('div#297589 _::text').get()).css('_')[7:][0].css('b')  
Out[48]: [<Selector xpath='descendant-or-self::b' data='<b>2020-03-23</b>'>]

In [49]: Selector(text = response.css('div#297589 _::text').get()).css('_')[7:][2].css('b')  
Out[49]: [<Selector xpath='descendant-or-self::b' data='<b>2020-03-23</b>'>]

---

'文\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0 号'

response.css('tbody')
response.css('tbody td')
len(response.css('tbody td'))
response.css('tbody td')[-8].css('::text').get()
response.css('tbody td')[-7].css('::text').get()
response.css('tbody td')[-9].css('::text').get()
response.css('tbody td')[-6].css('::text').get()

response.css('div#zoom p \*::text').getall()

**Henan**

total page 34

https://www.henan.gov.cn/zwgk/gggs/index_32.html 34

https://www.henan.gov.cn/zwgk/fgwj/szfl/index_1.html 5

https://www.henan.gov.cn/zwgk/fgwj/yz/index_1.html 46

https://www.henan.gov.cn/zwgk/fgwj/yzb/index_1.html 82

https://www.henan.gov.cn/zwgk/fgwj/yzr/index_1.html 98

In [4]: response.css('div[class="con-box"] li')[0].css('p::text').get()  
Out[4]: '省政府令第 175 号'

In [5]: response.css('div[class="con-box"] li')[0].css('a::attr(href)').get()  
Out[5]: 'https://www.henan.gov.cn/2016/11-04/237098.html'

In [6]: response.css('div[class="con-box"] li')[0].css('a::attr(tile)').get()

In [7]: response.css('div[class="con-box"] li')[0].css('a::attr(title)').get()

In [8]: response.css('div[class="con-box"] li')[0].css('a').get()  
Out[8]: '<a href="https://www.henan.gov.cn/2016/11-04/237098.html" target="_blank">《河南省公共消防设施管理规定》(省政府令 175 号)</a>'

In [9]: response.css('div[class="con-box"] li')[0].css('a::text').get()  
Out[9]: '《河南省公共消防设施管理规定》(省政府令 175 号)'

In [10]: response.css('div[class="con-box"] li')[0].css('span::text').get()  
Out[10]: '2016-10-11'

response.css('div[class="content"] \*::text').getall()

---

http://wjbb.sft.henan.gov.cn/regulatory/viewQueryAll.do?offset=60&cdid=402881fa2d1738ac012d173a60930017

response.css('div[class=serListCon] a::attr(href)').getall()
response.css('div[class=serListCon] a::attr(title)').getall()
response.css('div[class=serListCon] span::text').getall()

---

In [3]: response.css('div[class="mt15 list-box"] li')[0].css('span::text').get()  
Out[3]: '2006-09-05'

In [4]: response.css('div[class="mt15 list-box"] li')[0].css('a::attr(title)').get()

In [5]: response.css('div[class="mt15 list-box"] li')[0].css('a::attr(href)').get()  
Out[5]: 'https://www.henan.gov.cn/2006/09-01/232817.html'

In [6]: response.css('div[class="mt15 list-box"] li')[0].css('a::text').get()  
Out[6]: '河南省商务厅关于实施酒类流通备案登记管理的公告'

response.css('div[class="content"] \*::text').getall()

**Shandong**

total page 5835

http://www.shandong.gov.cn/module/xxgk/search_custom.jsp?fields=&fieldConfigId=247732&sortfield=compaltedate:0&fbtime=&texttype=&vc_all=&vc_filenumber=&vc_title=&vc_number=&currpage={0}&binlay=&c_issuetime=

In [2]: response.css('div.wip_lists')[0].css('a::attr(href)').get()  
Out[2]: 'http://www.shandong.gov.cn/art/2016/12/21/art_97741_53852.html?xxgkhide=1'

In [3]: response.css('div.wip_lists')[0].css('a::attr(title)').get()

In [4]: response.css('div.wip_lists')[0].css('a::text').get()  
Out[4]: '\n\t\t\t 山东省人民政府办公厅关于印发山东省安全生产巡查工作制度的通知\n\t\t'

In [3]: response.css('div.wip_art_con p')[1].css('::text').get()  
Out[3]: '鲁政字〔2011〕40 号'

response.css('div.wip_art_con p \*::text').getall()

**Hainan**

total page 486

http://www.hainan.gov.cn/u/search/wjk/rs?keywords=&docYear=&docName=&fwzh=&column=undefined&curPage=7&PageSize=15

In [7]: l['page']['list'][0]  
response.text
import json
json.loads(response.txt)
json.loads(response.text)
l = json.loads(response.text)
l['page']['list']
l['page']['list'][0]

Out[7]:
{'channel_name': '市县文件',
'pubDate': '2020-01-10',
'ccode': 'sxgw',
'wcode': 'hainan',
'website_name': '海南省人民政府网',
'c_syh': '00817365-1/2020-44472',
'url': '/hainan/sxgw/202001/8a1de39dadb74187bcfca788448d74dc.shtml',
'channel_id': '0d690a95f6484047ae7f30a4424c9416',
'c_wjbh': '',
'c_ztc': '',
'title': '关于五指山市、临高县、白沙黎族自治县退出贫困县序列的公示',
'c_fbjg': '海南省扶贫开发领导小组办公室',
'manuscript_id': '8a1de39dadb74187bcfca788448d74dc',
'fwrq': '2020-01-10',
'website_id': '18e6ca0ea4434f82ab06eb8dc11d926a'}

response.css('div#zoom p \*::text').getall()

**Central**

total page 2466

http://sousuo.gov.cn/data?t=zhengcelibrary&q=&timetype=timeqb&mintime=&maxtime=&sort=pubtime&sortType=1&searchfield=title&pcodeJiguan=&childtype=&subchildtype=&tsbq=&pubtimeyear=&puborg=&pcodeYear=&pcodeNum=&filetype=&p=2457&n=5&inpro=&bmfl=&dup=&orpro=

import json
d = json.loads(response.text)
d
d['listV0']
d['searchV0']
d['searchVO']
d['searchVO']['extendresult']
d['searchVO']['listvo']
d['searchVO']['gongbao']
d['searchVO']['gongbao']
d['searchVO']['catmap']['gongbao']
d['searchVO']['catmap']['gongbao']['listvo']

{'id': 'gongbao:9045',
'title': '中华人民共和国对外贸易经济合作部令(一九九九年第 3 号)<br> 对外贸易经济合作部《关于外商投资举办投资性公司的暂行规定》的补充<br> 规定',
'pubtime': 949161600000,
'pubtimeStr': '2000.01.30',
'dateType': False,
'summary': '中华人民共和国对外贸易经济合作部令 一九九九年 第 3 号 现将《对外贸易经济合作部的补充规定》予以公布。本规定自公布之日起施行。 部 长 石广生 一九九九年八月二十四日 对外贸易经济合作部 《...',
'url': 'http://www.gov.cn/gongbao/content/2000/content_60559.htm',
'pcode': '3',
'ptime': 935424000000,
'code': '3',
'fcode': '966',
'gname': '2000 年第 3 号',
'source': '外经贸部',
'imgurl': '',
'sourceName': None,
'createtime': None,
'filetype': None,
'childtype': '',
'subchildtype': None,
'puborg': '',
'index': '',
'subjectword': '',
'colname': '国务院公报',
'colfathername': '',
'personal': False,
'theme': False,
'imgWidth': None,
'imgHeight': None,
'textWidth': None,
'themeLinks': [],
'piclinksurl': '',
'fwdw': '',
'wenhao': '',
'zhengtype': '',
'syqt': '',
'fawentime': None,
'fwzh': '',
'fwjg': None,
'wjlx': '',
'shixiao': ''}]

**Liaoning**

news(不好)

http://www.ln.gov.cn/zfxx/rdxx01_105674/index_1.html

total page 25

http://www.ln.gov.cn/zfxx/msrd/index_1.html(不好)

25

http://www.ln.gov.cn/zfxx/tjdt/index_1.html

25

http://www.ln.gov.cn/zfxx/ghjh/bmgh/

another method

http://www.ln.gov.cn/zfxx/zfwj/szfl/index_1.html

9

http://www.ln.gov.cn/zfxx/zfwj/szfbgtwj/zfwj2011_136268/index_1.html

2

http://www.ln.gov.cn/zfxx/zfwj/szfwj/zfwj2011_140407/index.html

1

http://www.ln.gov.cn/zfxx/zfwj/bmwj/

1

In [4]: response.css('table.dataList tr')[1:][0].css('td')[1].css('a::attr(href)').get()  
Out[4]: './zfwj2011_119231/201801/t20180123_3150934.html'

In [5]: response.css('table.dataList tr')[1:][0].css('td')[1].css('a::attr(title)').get()  
Out[5]: '辽宁省人民政府关于修改《辽宁省建设项目安全设施监督管理办法》的决定'

In [6]: response.css('table.dataList tr')[1:][0].css('td')[2].css('::text').get()  
Out[6]: '第 312 号'

In [7]: response.css('table.dataList tr')[1:][0].css('td')[4].css('::text').get()  
Out[7]: '2018-01-23'

response.css('div#main \*::text').getall()

**Xizang**

http://www.xizang.gov.cn/zwgk/xxfb/gsgg_428/

total page 54

In [2]: response.css('ul.zwyw_list li')[0].css('a::attr(href)').get()  
Out[2]: './202004/t20200407_136481.html'

In [3]: response.css('ul.zwyw_list li')[0].css('a::text').get()  
Out[3]: '西藏自治区人民政府驻成都办事处离任审计询价公告'

In [4]: response.css('ul.zwyw_list li')[0].css('span::text').get()  
Out[4]: '2020-04-07'

response.css('table.table')
response.css('table.table tr')
response.css('table.table tr td.th')
response.css('table.table tr td.td')

In [6]: response.css('table.table tr td.th')[2].css('::text').get()  
Out[6]: '文 \xa0\xa0\xa0\xa0 号'

response.css('div.view \*::text').getall()

**Hubei**

'http://www.hubei.gov.cn/zfwj/szfl/index{0}.shtml':10,
'http://www.hubei.gov.cn/zfwj/ezf/index{0}.shtml':47,
'http://www.hubei.gov.cn/zfwj/ezh/index{0}.shtml':12,
'http://www.hubei.gov.cn/zfwj/ezd/index{0}.shtml':1,
'http://www.hubei.gov.cn/zfwj/ezbf/index{0}.shtml':50,
'http://www.hubei.gov.cn/zfwj/qt/index{0}.shtml':8,

headers = {'Host': 'www.hubei.gov.cn',
'Connection': 'keep-alive',
'Cache-Control': 'max-age=0',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (X11; Linux x86*64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/\_;q=0.8,application/signed-exchange;v=b3',
'Referer': 'http://www.hubei.gov.cn/zfwj/szfl/index_9.shtml',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
'Cookie': 'Secure; FSSBBIl1UgzbN7N80S=clrf2UHoMt0DgPB491MS_YjGoovnKcoQJhmG88s2jyYqsL9c9x9qTtP6v7_qEVl3; Secure; \_trs_uv=k92le385_3027_hlrs; \_trs_ua_s_1=k92le385_3027_g0u; Hm_lvt_5544783ae3e1427d6972d9e77268f25d=1585408324,1587031185; dataHide2=f5865260-69d2-47c3-9602-d7faa6439fd6; Hm_lpvt_5544783ae3e1427d6972d9e77268f25d=1587031406; FSSBBIl1UgzbN7N80T=4fBWMV9h77mTovzwH6v3_FSV9vJPTUAMh8ObnRg58Zzxtuj_jxTp7BzdYLTLyBB0VkD0012ZcWolmQ61kViLgcVX65p5b1yq0FbgEHD.ciKU.AByM6dwAWQOYRRM83XnsgznLMyTk9uBq1RCs8ma_DIEFJsuwxqzx4wgfsvm2lj0BtmH5blks.N.dS7kvimGc4H30I8QfCE3sLxGw1b4UtL8XtQzKOMRMsBacs5H96Mw6fE_SHbK0ZCQW08afTvNUEyx.AC3TNr8V11XdL2yVlUA3mOtEPmcXKL6zjzJllsD5.7O5P_QTp1EbxZBzGknhCwQyn3urEoD_nMN_LgIiLsK.0Agwoo3AlHtd3dImJeq8_0imj1N6E0ICxqnqy4b5M5aAwCT3NqjHZD1eWhqbxydr'}

Cookies = {'FSSBBIl1UgzbN7N80S': 'clrf2UHoMt0DgPB491MS_YjGoovnKcoQJhmG88s2jyYqsL9c9x9qTtP6v7_qEVl3',
'\_trs_uv': 'k92le385_3027_hlrs',
'\_trs_ua_s_1': 'k92le385_3027_g0u',
'Hm_lvt_5544783ae3e1427d6972d9e77268f25d': '1585408324,1587031185',
'dataHide2': 'f5865260-69d2-47c3-9602-d7faa6439fd6',
'Hm_lpvt_5544783ae3e1427d6972d9e77268f25d': '1587031406',
'FSSBBIl1UgzbN7N80T': '4fBWMV9h77mTovzwH6v3_FSV9vJPTUAMh8ObnRg58Zzxtuj_jxTp7BzdYLTLyBB0VkD0012ZcWolmQ61kViLgcVX65p5b1yq0FbgEHD.ciKU.AByM6dwAWQOYRRM83XnsgznLMyTk9uBq1RCs8ma_DIEFJsuwxqzx4wgfsvm2lj0BtmH5blks.N.dS7kvimGc4H30I8QfCE3sLxGw1b4UtL8XtQzKOMRMsBacs5H96Mw6fE_SHbK0ZCQW08afTvNUEyx.AC3TNr8V11XdL2yVlUA3mOtEPmcXKL6zjzJllsD5.7O5P_QTp1EbxZBzGknhCwQyn3urEoD_nMN_LgIiLsK.0Agwoo3AlHtd3dImJeq8_0imj1N6E0ICxqnqy4b5M5aAwCT3NqjHZD1eWhqbxydr'}

打开 driver 必须 get 一下主页保证有 referer

In [16]: res.css('div.list_block li')[0].css('a::attr(href)').get()  
Out[16]: './202001/t20200118_2006205.shtml'

In [17]: res.css('div.list_block li')[0].css('a::attr(title)').get()  
Out[17]: '湖北省人民防空工程管理规定'

In [18]: res.css('div.list_block li')[0].css('span::text').get()

Out[18]: '2020-01-18 11:34'

In [24]: res.css('div.metadata_content div.col-xs-12')[0].css('::text').getall()  
Out[24]:
['\n\t\t ',
'索 引 号：',
'011043102/2020-37348\n\t\t ']

In [25]: res.css('div.metadata_content div.col-xs-12')[0].css('::text').get()  
Out[25]: '\n\t\t '

In [26]: res.css('div.metadata_content div.col-xs-12')[0].css('::text').getall()  
Out[26]:
['\n\t\t ',
'索 引 号：',
'011043102/2020-37348\n\t\t ']

In [27]: res.css('div.metadata_content div.col-xs-12')[-1].css('::text').getall()  
Out[27]: ['\n\t\t ', '发布日期：', '2020 年 01 月 18 日\n\t\t ']

'文 号：'

res.css('div.content_block \*::text').getall()
