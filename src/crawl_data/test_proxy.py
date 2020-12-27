import requests

#请求地址
targetUrl = "http://baidu.com"

#代理服务器
proxyHost = "125.122.199.13"
proxyPort = "9000"

proxyMeta = "http://%(host)s:%(port)s" % {

    "host" : proxyHost,
    "port" : proxyPort,
}

proxyMeta = "http://114.106.72.38:3000"

#pip install -U requests[socks]  socks5代理
# proxyMeta = "socks5://%(host)s:%(port)s" % {

#     "host" : proxyHost,

#     "port" : proxyPort,

# }

proxies = {

    "http"  : proxyMeta,
}

resp = requests.get(targetUrl, proxies=proxies)
print(resp.status_code)
print(resp.text)
