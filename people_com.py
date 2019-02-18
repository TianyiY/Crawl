# -*- coding: utf-8 -*-
import requests
import json
import pandas as pd
from urllib.parse import urlencode
from requests.exceptions import RequestException
import urllib.request
from bs4 import BeautifulSoup

answerContent=[]
answerDateline=[]
answerOrganization=[]
Content=[]
dateline=[]
domainName=[]
subject=[]
typeName=[]
tid=[]
TITLE=[]
QUESTION=[]
REPLY=[]
ASK_TIME=[]
CAT=[]
PROP=[]
REPLY_TIME=[]
REPLY_UNIT=[]

def get_list(fid):
    url = 'http://liuyan.people.com.cn/threads/queryThreadsList'
    headers = {'Accept': 'application/json, text/javascript, */*; q=0.01',
               'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-CN,zh;q=0.9',
               'Connection': 'keep-alive',
               'Cookie': 'wdcid=5f068bc1594d74a0; sso_c=0; sfr=1; ALLYESID4=10149304F3AEC06C; _ma_tk=mo4nbpot0ht8rpny4xxcxj8c51wccmqx; aliyungf_tc=AQAAALaaSB24lwwAS/RydkALDss8uq2d; wdlast=1532321475; wdses=4cdfb526bc0b8e96; JSESSIONID=737C9A310CF80FCA4966A438A122BCA9; rand_code=padaQy0VTd/vAKgCZ/DbNQ==',
               'Host': 'liuyan.people.com.cn',
               'Origin': 'http://liuyan.people.com.cn',
               'Referer': 'http://liuyan.people.com.cn/threads/list?fid='+str(fid),
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3423.2 Safari/537.36'}

    data = {'fid': fid,
            'lastItem': 0}
    while len(json.loads(requests.post(url, headers=headers, data=data).content.decode()).get('responseData')) > 0:
        response = requests.post(url, headers=headers, data=data)
        # print(response.content.decode())
        res = json.loads(response.content.decode())
        for i in range(len(res['responseData'])):
            Content.append(res['responseData'][i].get('content'))
            answerContent.append(res['responseData'][i].get('answerContent'))
            answerDateline.append(res['responseData'][i].get('answerDateline'))
            answerOrganization.append(res['responseData'][i].get('answerOrganization'))
            dateline.append(res['responseData'][i].get('dateline'))
            domainName.append(res['responseData'][i].get('domainName'))
            subject.append(res['responseData'][i].get('subject'))
            typeName.append(res['responseData'][i].get('typeName'))
            id = (res['responseData'][i].get('tid'))
            tid.append(id)
            data = {'fid': fid,
                    'lastItem': id}

#dataframe=pd.DataFrame(data={'Content':Content, 'answerContent': answerContent, 'answerDateline':answerDateline,
#                        'answerOrganization':answerOrganization, 'dateline':dateline, 'domainName':domainName,
#                        'subject':subject , 'typeName':typeName})

#dataframe.to_csv('output_SQ.csv', encoding='utf_8_sig', index=False)

def get_one_page_content(tid):
    parameters={'tid':tid}
    url='http://liuyan.people.com.cn/threads/content?'+urlencode(parameters)
    web_content = urllib.request.urlopen(url)
    content = web_content.read().decode()
    return content

def page_content(content):
    soup = BeautifulSoup(content, "html.parser")
    # print(soup.prettify())
    # print(soup.title)
    # print(soup.head)
    # print(soup.a)
    # print(soup.p)
    text_Q = soup.find_all('div', class_='liuyan_box03 w1200 clearfix')
    text_A = soup.find_all('div', class_='clearfix liuyan_box05 w1200')
    title=text_Q[0].find_all('b')[0]
    ask_time=text_Q[0].find_all('span')[0]
    cat=text_Q[0].find_all('em')[1]
    prop=text_Q[0].find_all('em')[2]
    question=text_Q[0].find_all('p')[0]
    if len(text_A[0].find_all('em'))>0:
        reply_time = text_A[0].find_all('em')[0]
    else:
        reply_time=None
    if len(text_A[0].find_all('p'))>0:
        reply = text_A[0].find_all('p')[0]
    else:
        reply=None
    return title, ask_time, cat, prop, question, reply_time, reply

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

def format_time(content):
    content = str(content)
    content_str = ''
    for i in content:
        if is_number(i):
            content_str = content_str+i
    return content_str

get_list(1789)
for i in tid:
    title, ask_time, cat, prop, question, reply_times, reply=(page_content(get_one_page_content(i)))
    title = format_str(title)[:-3]
    ask_time=format_time(ask_time)[-12:-1]
    cat=format_str(cat)
    prop=format_str(prop)
    question = format_str(question)
    reply_time=format_time(reply_times)[-12:]
    reply_unit=format_str(reply_times)[5:-12]
    reply = format_str(reply)
    TITLE.append(title)
    ASK_TIME.append(ask_time)
    CAT.append(cat)
    PROP.append(prop)
    QUESTION.append(question)
    REPLY_TIME.append(reply_time)
    REPLY_UNIT.append(reply_unit)
    REPLY.append(reply)

dataframe=pd.DataFrame(data={'TITLE':TITLE, 'ASK_TIME':ASK_TIME, 'CAT':CAT, 'PROP':PROP,
                             'QUESTION': QUESTION, 'REPLY_TIME':REPLY_TIME, 'REPLY_UNIT':REPLY_UNIT, 'REPLY':REPLY})

dataframe.to_csv('people.csv', encoding='utf_8_sig', index=False)

