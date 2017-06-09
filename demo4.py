import requests
from bs4 import BeautifulSoup
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
res=requests.get("http://www.xinshipu.com/zuofa/685313", headers=headers)
soup=BeautifulSoup(res.text, 'lxml')

mil=soup.select('.re-up')[0]
print mil.select('.font18.no-overflow')[0].text
print mil.select('.font16.ml10.col')[0].text
print mil.select('.font16.ml10.col')[1].text
print mil.select('.cg2.mt12 span:nth-of-type(1)')[0].text, mil.select('.cg2.mt12 span:nth-of-type(2)')[0].text
print mil.select('.cg2.mt12 span:nth-of-type(3)')[0].text, mil.select('.cg2.mt12 span:nth-of-type(4)')[0].text
print mil.select('.cg2.mt12 span:nth-of-type(5)')[0].text, mil.select('.cg2.mt12 span:nth-of-type(6)')[0].text