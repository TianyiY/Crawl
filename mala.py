# -*- coding: utf-8 -*-
import re
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import trange
import numpy as np
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False

web_urls=[]
text_titles=[]
text_contents=[]
text_looks=[]
text_replies=[]
text_dates=[]

def is_chinese(uchar):
    """判断一个unicode是否是汉字"""
    if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
        return True
    else:
        return False

def is_number(uchar):
    """判断一个unicode是否是数字"""
    if uchar >= u'\u0030' and uchar <= u'\u0039':
        return True
    else:
        return False

def is_alphabet(uchar):
    """判断一个unicode是否是英文字母"""
    if (uchar >= u'\u0041' and uchar <= u'\u005a') or (uchar >= u'\u0061' and uchar <= u'\u007a'):
        return True
    else:
        return False

def format_chinese(content):
    content = str(content)
    content_str = ''
    for i in content:
        if is_chinese(i):
            content_str = content_str+i
    return content_str

def format_num(content):
    content = str(content)
    content_str = ''
    for i in content:
        if is_number(i):
            content_str = content_str+i
    return (content_str)

def extract_webs():
    for j in trange(500):
        url = 'https://www.mala.cn/forum-5-' + str(j+1) + '.html'
        headers = {
            'ACCEPT': 'text/html, application/xhtml+xml, application/xml; q=0.9, image/webp, image/apng, */*;q=0.8',
            'ACCEPT-ENCODING': 'gzip, deflate, br',
            'ACCEPT-LANGUAGE': 'zh-CN, zh; q=0.9',
            'CACHE-CONTROL': 'max - age = 0',
            'CONNECTION': 'keep - alive',
            'USER-AGENT': 'Mozilla/5.0(WindowsNT 6.3; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
        response = requests.get(url=url, headers=headers)
        text = response.text
        #print(text)
        txt = ''
        soup = BeautifulSoup(text, "html.parser")
        text = (soup.find_all('div', class_='bm_c'))
        for i in range(len(text)):
            txt += str(text[i])
        pattern = re.compile(r'.*?<tbody id="normalthread_(\d{8})">.*?')
        id = re.findall(pattern, txt)
        for i in id:
            web_url = 'https://www.mala.cn/thread-' + str(i) + '-1-' + str(j) + '.html'
            #print(web_url)
            web_urls.append(web_url)

def save_urls():
    extract_webs()
    np_web_urls=np.array(web_urls)
    np.save('np_web_urls.npy' ,np_web_urls) # 保存为.npy格式

#save_urls()
web_urls=np.load('np_web_urls.npy')
web_urls=web_urls.tolist()[:20]
#print(web_urls)

def extract_contents(urls):
    headers = {
        'ACCEPT': 'text/html, application/xhtml+xml, application/xml; q=0.9, image/webp, image/apng, */*;q=0.8',
        'ACCEPT-ENCODING': 'gzip, deflate, br',
        'ACCEPT-LANGUAGE': 'zh-CN, zh; q=0.9',
        'CACHE-CONTROL': 'max - age = 0',
        'CONNECTION': 'keep - alive',
        'USER-AGENT': 'Mozilla/5.0(WindowsNT 6.3; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
    for url in tqdm(urls):
        response = requests.get(url=url, headers=headers)
        text = response.text
        soup = BeautifulSoup(text, "html.parser")
        print(url)
        #print(soup)
        text_head=str(soup.find_all('div', class_='authi')[1])
        FrontPos = text_head.index('发表于')
        AfterPos = text_head.index('</em>')
        text_date=(text_head[FrontPos+4:AfterPos])
        text_title = soup.find_all('h1', class_="ts")
        if len(soup.find_all('td', class_='t_f'))>0:
            text_content = soup.find_all('td', class_='t_f')[0]
        else:
            text_content = soup.find_all('td', class_='t_f')
        if len(soup.find_all('span', class_='xi1'))==2:
            text_look = soup.find_all('span', class_='xi1')[0]
            text_reply = soup.find_all('span', class_='xi1')[1]
        else:
            text_look = None
            text_reply = None
        text_title = format_chinese(text_title)
        text_content = format_chinese(text_content)
        #if int(format_num(text_look)[1:])>=0:
        #    text_look = int(format_num(text_look)[1:])
        #else:
        #    text_look=None
        #if int(format_num(text_reply)[1:]) >= 0:
        #    text_reply = int(format_num(text_reply)[1:])
        #else:
        #    text_reply=None
        text_titles.append(text_title)
        text_contents.append(text_content)
        text_looks.append(text_look)
        text_replies.append(text_reply)
        text_dates.append(text_date)

extract_contents(web_urls)
dataframe=pd.DataFrame(data={'url':web_urls, '标题': text_titles, '内容':text_contents, '时间':text_dates,}) #'text_looks':text_looks, 'text_replies':text_replies
dataframe.to_csv('mala.csv', encoding='utf_8_sig', index=False)