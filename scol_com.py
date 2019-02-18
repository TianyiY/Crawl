# -*- coding: utf-8 -*-
import requests
import json
import re
import pandas as pd
from urllib.parse import urlencode
import urllib.request
from bs4 import BeautifulSoup

ask_cats=[]
ask_props=[]
ask_titles=[]
ask_times=[]
ask_contents=[]
answer_units=[]
answer_times=[]
answer_contents=[]
web_urls=[]

def extract_webs(fid):
    for j in range(1, 10+1):
        tid=[]
        url='https://ly.scol.com.cn/main/thredlist?fid='+str(fid)+ '&display=1&page='+ str(j)
        headers = {
            'ACCEPT': 'text/html, application/xhtml+xml, application/xml; q=0.9, image/webp, image/apng, */*;q=0.8',
            'ACCEPT-ENCODING': 'gzip, deflate, br',
            'ACCEPT-LANGUAGE': 'zh-CN, zh; q=0.9',
            'CACHE-CONTROL': 'max - age = 0',
            'CONNECTION': 'keep - alive',
            'USER-AGENT': 'Mozilla/5.0(WindowsNT 6.3; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
        response = requests.get(url=url, headers=headers)
        text = response.text
        soup = BeautifulSoup(text, "html.parser")
        text = soup.find_all('div', class_='con_lylist w1000 auto')
        text=text[0].find_all('a')
        i=0
        while i < len(text)/4:
            text_num=str(text[2+4*i])
            id=int(text_num.index('tid='))
            tid.append(text_num[id+4:id+11])
            i+=1
        for i in tid:
            web_url = 'https://ly.scol.com.cn/thread?tid='+str(i)
            web_urls.append(web_url)

def get_one_page_content(url):
    web_content = urllib.request.urlopen(url)
    content = web_content.read().decode()
    return content

def page_content(content):
    soup = BeautifulSoup(content, "html.parser")
    text_Q = soup.find_all('div', class_='c1')
    ask_title=text_Q[0].find_all('em')
    ask_time=text_Q[0].find_all('i')[0]
    ask_content=text_Q[0].find_all('p')
    text_A = soup.find_all('div', class_='c3')
    if len(text_A)>0:
        answer_content = text_A[0].find_all('p')
        answer_time=text_A[0].find_all('i')
        answer_unit=text_A[0].find_all('em')
    else:
        answer_content=None
        answer_time=None
        answer_unit=None
    return ask_title, ask_time, ask_content, answer_unit, answer_time, answer_content

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

def format_str(content):
    content = str(content)
    content_str = ''
    for i in content:
        if is_chinese(i) or is_number(i):
            content_str = content_str+i
    return content_str

def format_chinese(content):
    content = str(content)
    content_str = ''
    for i in content:
        if is_chinese(i):
            content_str = content_str+i
    return content_str

def format_time(content):
    content = str(content)
    content_str = ''
    for i in content:
        if is_number(i):
            content_str = content_str+i
    return content_str

extract_webs(1789)

for i in web_urls:
    ask_title, ask_time, ask_content, answer_unit, answer_time, answer_content=(page_content(get_one_page_content(i)))
    ask_title = format_chinese(ask_title)
    ask_id = str(ask_time).index('*')
    ask_time = str(ask_time)[ask_id + 3:ask_id + 3 + 16]
    ask_content = format_str(ask_content)
    answer_unit = format_chinese(answer_unit)
    if (answer_time)!=None:
        answer_id = str(answer_time).index('回复时间')
        answer_time = str(answer_time)[answer_id + 5: answer_id + 5 + 16]
    else:
        answer_time=None
    answer_content = format_str(answer_content)
    ask_cats.append(ask_title[:2])
    ask_props.append(ask_title[2:4])
    ask_titles.append(ask_title[4:])
    ask_times.append(ask_time)
    ask_contents.append(ask_content)
    answer_units.append(answer_unit)
    answer_times.append(answer_time)
    answer_contents.append(answer_content)

dataframe=pd.DataFrame(data={'ask_cats':ask_cats, 'ask_props':ask_props, 'ask_titles':ask_titles, 'ask_times':ask_times, 'ask_contents':ask_contents,
                             'answer_units': answer_units, 'answer_times':answer_times, 'answer_contents':answer_contents})

dataframe.to_csv('scol.csv', encoding='utf_8_sig', index=False)

