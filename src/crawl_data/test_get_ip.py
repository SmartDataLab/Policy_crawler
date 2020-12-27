import requests
import json

url = "https://api.xiaoxiangdaili.com/ip/get?appKey=571491556088238080&appSecret=6VZhoE4G&cnt=1&method=http&releaseAuto=false&wt=json"

resp = requests.get(url)
print(resp.status_code,type(resp.status_code))
if resp.status_code == 200:
    x = json.loads(resp.text)
    s = 'http://%s:%s' %(x['data'][0]['ip'],x['data'][0]['port'])
    print(s)
    
