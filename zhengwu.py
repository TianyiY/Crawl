# -*- coding: utf-8 -*-
import requests
import json
import pandas as pd
from urllib.parse import urlencode
import urllib.request
import numpy as np
from bs4 import BeautifulSoup
from tqdm import tqdm

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
Status=[]
Categogies=[]
Classification=[]
tid=[]
Dates=[]

# 范锐平1289； 罗强1290； 天府新区4700；  青羊1772； 锦江1773； 金牛1774； 武侯1775；
# 成华1776； 龙泉驿1777； 青白江1778； 新都1779； 温江1780； 都江堰1781； 彭州1782；
# 邛崃1783； 崇州1784； 金堂1785； 双流1786； 郫都1787； 大邑1788； 蒲江1789；
# 新津1790； 高新4498； 简阳1901
person_id=1290

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
        if not (is_chinese(i) or is_alphabet(i)):
            content_str = content_str+i
    return content_str

def get_list(fid):
    url ='http://liuyan.people.com.cn/threads/queryThreadsList'
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
        #print(response.content.decode())
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
            print(id)
            data = {'fid': fid,
                    'lastItem': id}

def save_tid(person_id):
    get_list(person_id)
    np_tid = np.array(tid)
    np.save('np_tid.npy', np_tid)  # 保存为.npy格式

#dataframe=pd.DataFrame(data={'Content':Content, 'answerContent': answerContent, 'answerDateline':answerDateline,
#                        'answerOrganization':answerOrganization, 'dateline':dateline, 'domainName':domainName,
#                        'subject':subject , 'typeName':typeName})
#dataframe.to_csv('output_SQ.csv', encoding='utf_8_sig', index=False)

save_tid(person_id)
tid=np.load('np_tid.npy')
tid=tid.tolist()[:50]

def get_one_page_content(tid):
    parameters={'tid':tid}
    url='http://liuyan.people.com.cn/threads/content?'+urlencode(parameters)
    print(url)
    try:
        web_content = urllib.request.urlopen(url)
        content = web_content.read().decode()
        #print(content)
        return content
    except:
        return 0

def page_content(content):
    try:
        soup = BeautifulSoup(content, "html.parser")
        # print(soup.prettify())
        # print(soup.title)
        # print(soup.head)
        # print(soup.a)
        # print(soup.p)
        #print(soup)
        #print('(((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((')
        text_Q = soup.find_all('div', class_='liuyan_box03 w1200 clearfix')
        #print(text_Q)
        text_A = soup.find_all('div', class_='clearfix liuyan_box05 w1200')
        #print(text_A)
        #print('(((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((')
        dates=(text_Q[0].find_all('h3')[0].find_all('span')[0])
        title0=text_Q[0].find_all('b')[0]
        status=(title0.find_all('em')[0])
        classification=(title0.find_all('em')[1])
        categogies=(title0.find_all('em')[2])
        title=title0.find_all('span')
        #print(title)
        question=text_Q[0].find_all('p')[0]
        #print('(((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((')
        #print(question)
        if len(text_A[0].find_all('p'))>0:
            reply = text_A[0].find_all('p')[0]
        else:
            reply=None
        #print('(((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((')
        #print(reply)
        return title, question, reply, status, classification, categogies, dates
    except:
        return 0

for i in tqdm(tid):
    title, question, reply, status, classification, categogies, dates=(page_content(get_one_page_content(i)))
    #print(title, question, reply)
    title = str(title).replace('[<span class="context-title-text">','')
    title = (title).replace('</span>]', '')
    title=title.strip()
    question = str(question).replace('<p class="zoom content">','')
    question = str(question).replace('</p>', '')
    question = question.strip()
    reply = str(reply).replace('<p class="zoom">','')
    reply = str(reply).replace('<br/>', '')
    reply = str(reply).replace('</p>', '')
    reply = reply.strip()
    status = str(status).replace('<em class="green">', '')
    status = str(status).replace('<em class="red">', '')
    status = str(status).replace('<em class="orange">', '')
    status = str(status).replace('</em>', '')
    status = status.strip()
    classification = str(classification).replace('<em class="domainType">', '')
    classification = str(classification).replace('</em>', '')
    classification = classification.strip()
    categogies = str(categogies).replace('<em class="domainType">', '')
    categogies = str(categogies).replace('</em>', '')
    categogies = categogies.strip()
    dates = str(dates).replace('<span>', '')
    dates = str(dates).replace('</span>', '')
    dates = str(dates).replace('*', '')
    dates=format_str(dates)
    dates = dates.strip()
    TITLE.append(title)
    QUESTION.append(question)
    REPLY.append(reply)
    Status.append(status)
    Classification.append(classification)
    Categogies.append(categogies)
    Dates.append(dates)

dataframe=pd.DataFrame(data={'标题':TITLE, '内容': QUESTION, '回复':REPLY, '状态':Status, '类别':Classification, '性质':Categogies, '时间':Dates})
dataframe.to_csv('zhengwu.csv', encoding='utf_8_sig', index=False)
