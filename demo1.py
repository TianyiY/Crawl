import requests
res=requests.get("https://world.taobao.com/search/search.htm?_ksTS=1496788690090_29&spm=a215z.1510359.a214x9l.2&search_type=0&_input_charset=utf-8&navigator=all&json=on&q=iphone6%E6%89%8B%E6%9C%BA%E5%A3%B3&cna=vgJmEco6gVYCAYEPQP5jhJHU&callback=__jsonp_cb&abtest=_AB-LR517-LR854-LR895-PR517-PR854-PR895")
print res.text