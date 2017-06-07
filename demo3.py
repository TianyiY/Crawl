import requests
res=requests.get("https://world.taobao.com/search/json.htm?navigator=all&cat=50040657&_ksTS=1496794829523_29&_input_charset=utf-8&json=on&callback=__jsonp_cb&cna=vgJmEco6gVYCAYEPQP5jhJHU&abtest=_AB-LR517-LR854-LR895-PR517-PR854-PR895&nid=&type=&uniqpid=")
print res.text
print '============================'
import json
import re
m=re.search('if\(window.__jsonp_cb\)\{__jsonp_cb\((.*?)\)\}', res.text)     # what we need is included in (.*?)
print m.group(1)   # 1 refer to (.*?)
print '============================'
jd=json.loads(m.group(1))
print jd
print '============================'

with open('a.json', 'w') as f:
    f.write(json.dumps(jd))

for item in jd['itemList']:    # a.json preview
    print item['nick'], item['price']
print '============================'

import pandas
df=pandas.DataFrame(jd['itemList'])
print df


