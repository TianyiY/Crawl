import requests
headers={'user-agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'}
res=requests.get('https://finance.yahoo.com/quote/%5EIXIC?p=^IXIC', headers=headers)
print res.text