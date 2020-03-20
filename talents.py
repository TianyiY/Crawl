#!usr/bin/python
# -*- coding: utf-8 -*-
# encoding=utf8
import re
import urllib.request
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
import tkinter
import tkinter.messagebox
import jieba
import jieba.analyse as analyse
import jieba.posseg
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False

job_titles=[]
company_names=[]
salary_ranges=[]
cities=[]
districts=[]
min_salaries=[]
max_salaries=[]
avg_salaries=[]
average_salaries=[]
minimum_salaries=[]
maximum_salaries=[]
job_info=[]
keywords=[]
months=[]
days=[]
work_locations=[]
experiences=[]
degrees=[]
head_counts=[]

def is_chinese(word):
    for ch in word:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False

def is_number(word):
    for ch in word:
        if ch >= u'\u0030' and ch <= u'\u0039':
            return True
    return False

def is_alphabet(word):
    for ch in word:
        if (ch >= u'\u0041' and ch <= u'\u005a') or (ch >= u'\u0061' and ch <= u'\u007a'):
            return True
    return False

def trans_chinese(content):
    content_str = ''
    for i in content:
        if is_chinese(i):
            content_str = content_str+i
    return content_str

def trans_chinese_and_number(content):
    content_str = ''
    for i in content:
        if is_chinese(i) or is_number(i):
            content_str = content_str+i
    return content_str

# attention: city_code为所查询城市编码, 重点城市city_code:
city_dict={'北京':'010000', '上海':'020000', '深圳':'040000', '广州':'030200', '武汉':'180200', '西安':'200200', '杭州':'080200',
           '南京':'070200', '成都':'090200', '重庆':'060000', '大连':'230300', '东莞':'030800', '沈阳':'230200', '苏州':'070300',
           '昆明':'250200', '长沙':'190200', '合肥':'150200', '宁波':'080300', '郑州':'170200', '天津':'050000', '青岛':'120300',
           '济南':'120200', '哈尔滨':'220200', '长春':'240200', '福州':'110200'}

def get_one_page_content(city, job_categotry='%2520', page=1):
    global paras
    city=str(city)
    page = str(page)
    paras={'city':city}
    city_code=str(city_dict[city])
    if job_categotry!='%2520':
        job_categotry = urllib.parse.quote(job_categotry)
    url='https://search.51job.com/list/'+city_code+',000000,0000,00,9,99,'+job_categotry+',2,'+page+'.html'
    #print(url)
    web_content=urllib.request.urlopen(url)
    content=web_content.read().decode('gbk','ignore')
    return content

def reg_content(content):
    #print(content)
    reg_pattern=re.compile(r'class="t1 ">.*? <a target="_blank" title="(.*?)".*? '
                           r'href="(.*?)".*? '
                           r'<span class="t2"><a target="_blank" title="(.*?)".*?'
                           r'href="(.*?)".*? '
                           r'<span class="t3">(.*?)</span>.*?'
                           r'<span class="t4">(.*?)</span>.*? '
                           r'<span class="t5">(.*?)</span>'
                           , re.S)
    items = re.findall(reg_pattern, content)
    return items

def get_one_page_processed_info(reged_content):
    for item in reged_content:
        url = (item[1])
        web_content = requests.get(url).content.decode('gbk', 'ignore')
        soup = BeautifulSoup(web_content, 'html.parser')
        pp0 = soup.findAll(name='p', attrs={'class': 'msg ltype'})
        if (len(pp0))>0:
            job_title = item[0].strip()
            #print (job_title)
            job_titles.append(job_title)
            url = (item[1])
            web_content = requests.get(url).content.decode('gbk', 'ignore')
            soup = BeautifulSoup(web_content, 'html.parser')
            pp0 = soup.findAll(name='p', attrs={'class': 'msg ltype'})
            pp00=(str(pp0[0]).split('|'))
            #print((pp00[0]))
            work_locations.append(trans_chinese(pp00[0].strip()))
            #print((pp00[1]))
            experiences.append(pp00[1].strip().replace(' ',''))
            #print((pp00[2]))
            if '招' not in (pp00[2].strip().replace(' ', '')):
                degrees.append(pp00[2].strip().replace(' ', ''))
            else:
                degrees.append(None)
            #print((pp00[3]))
            if '招' in (pp00[3].strip().replace(' ','')):
                head_counts.append(pp00[3].strip())
            else:
                head_counts.append(pp00[2].strip())
            pp = soup.findAll(name='div', attrs={'class': 'bmsg job_msg inbox'})
            if len(pp) > 0:
                pp = re.sub(u"\\<.*?\\>", "", str(pp[0]))
                job_info.append(str(pp.strip().strip('微信分享').strip("\n").replace(' ', '')))
            else:
                job_info.append(None)
            #print (str(pp.strip().strip('微信分享').strip("\n").replace(' ', '')))
            company_name = item[2].strip()
            #print (company_name)
            company_names.append(company_name)
            company_location = item[4].strip()
            #print (company_location)
            company_location_index = company_location.find('-')
            if company_location_index >= 0:
                cities.append(company_location[0:company_location_index])
                districts.append(company_location[company_location_index + 1:])
            else:
                cities.append(company_location)
                districts.append(None)
            #print (company_location[company_location_index + 1:])
            #print (company_location[0:company_location_index])
            salary_range = item[5].strip()
            salary_ranges.append(salary_range)
            date=item[6].strip()
            months.append(date[:2])
            days.append(date[-2:])
            #print ('**********************************************')
            #print(time.strptime(date, "%m-%d"))

def page_job_count(content):
    soup = BeautifulSoup(content, "html.parser")
    text_job = soup.find_all('div', class_='rt')
    text_job=str(text_job[0])
    job_num = int(re.sub("\D", "", text_job))
    text_page=soup.find_all('span', class_='td')
    text_page = str(text_page[0])
    page_num = int(re.sub("\D", "", text_page))
    return job_num, page_num

def get_batch_info(city, job_categotry='%2520'):
    print('collecting data from internet')
    time.sleep(2)
    content=get_one_page_content(city, job_categotry)
    job_num, page_num=page_job_count(content)
    for i in tqdm(range(1, page_num+1)):
        content_=get_one_page_content(city, job_categotry, i)
        reged_content_=reg_content(content_)
        get_one_page_processed_info(reged_content_)
    print('complete extracting')
    print('********************************************************************************')

def process_salary_info(salary_ranges):
    print('cleaning salary data')
    time.sleep(5)
    for item in salary_ranges:
        sal_index = item.find('-')
        if item == '':
            min_salaries.append(None)
            max_salaries.append(None)
            avg_salaries.append(None)
        elif sal_index < 0:
            if item.find('.')>=0:
                text_num = re.findall(r'\d+\.?\d', item)
            else:
                text_num = re.findall(r'\d', item)
            num=(float(str(text_num[0])))
            multiplier = 1.
            multiplier_ = 1.
            if item.find('千') >= 0:
                multiplier = 1000.
            if item.find('万') >= 0:
                multiplier = 10000.
            if item.find('天') >= 0:
                multiplier_ = 30.
            if item.find('日') >= 0:
                multiplier_ = 30.
            if item.find('年') >= 0:
                multiplier_ = 1 / 12.
            num_=num*multiplier*multiplier_
            min_salaries.append(num_)
            max_salaries.append(num_)
            avg_salaries.append(num_)
        else:
            a = float(item[0:sal_index])
            b = float(item[sal_index + 1:-3])
            temp_min=min(a, b)
            temp_max=max(a, b)
            temp_avg = 0.5 * (temp_min + temp_max)
            multiplier=1.
            multiplier_=1.
            if item[-1] == '年':
                multiplier = 1. / 12.
            if item[-1] == '月':
                multiplier = 1.
            if item[-1] == '日':
                multiplier = 30.
            if item[-1] == '天':
                multiplier = 30.
            if item[-3] == '万':
                multiplier_ = 10000.
            if item[-3] == '千':
                multiplier_ = 1000.
            if item[-3] == '元':
                multiplier_ = 1.
            temp_min_ = temp_min * multiplier * multiplier_
            temp_max_ = temp_max * multiplier * multiplier_
            temp_avg_ = temp_avg * multiplier * multiplier_
            min_salaries.append(temp_min_)
            max_salaries.append(temp_max_)
            avg_salaries.append(temp_avg_)
    print('salary data is ready')
    print('********************************************************************************')

def tran_list_to_df(job_titles, company_names, cities, districts, min_salaries, max_salaries, average_salaries, job_info,
                    months, days, work_locations, experiences, degrees, head_counts):
    print('transforming list to dataframe')
    time.sleep(5)
    job_titles = (pd.DataFrame({'job_titles': job_titles}, dtype='object'))
    company_names = (pd.DataFrame({'company_names': company_names}, dtype='object'))
    cities = (pd.DataFrame({'cities': cities}, dtype='object'))
    districts = (pd.DataFrame({'districts': districts}, dtype='object'))
    min_salaries = (pd.DataFrame({'salaries_min': min_salaries}, dtype='float'))
    max_salaries = (pd.DataFrame({'salaries_max': max_salaries}, dtype='float'))
    average_salaries = (pd.DataFrame({'salaries_average': average_salaries}, dtype='float'))
    job_info=(pd.DataFrame({'descriptions': job_info}, dtype='object'))
    months = (pd.DataFrame({'month': months}, dtype='int'))
    days = (pd.DataFrame({'day': days}, dtype='int'))
    work_locations = (pd.DataFrame({'work_locations': work_locations}, dtype='object'))
    experiences = (pd.DataFrame({'experiences': experiences}, dtype='object'))
    degrees = (pd.DataFrame({'degrees': degrees}, dtype='object'))
    head_counts = (pd.DataFrame({'head_counts': head_counts}, dtype='object'))
    return pd.concat([job_titles, company_names, cities, districts, min_salaries, max_salaries, average_salaries,
                      work_locations, experiences, degrees, head_counts, job_info, months, days], axis=1)

def label_keyword(df, keyword):
    for i in range(len(df['descriptions'])):
        if str(keyword) in (str(df['descriptions'][i])):
            keywords.append(1)
        else:
            keywords.append(0)
    df['keyword_label'] = keywords
    return df

def word_frequency_statistics(job_info):
    words = ("".join(job_info))
    words = jieba.cut(words)
    counts = {}
    for word in words:
        counts[word] = counts.get(word, 0) + 1
    items = list(counts.items())
    items.sort(key=lambda x: x[1], reverse=True)
    for i in range(100):
        word, count = items[i]
        if (is_chinese(str(word)) or is_number(str(word)) or is_alphabet(str(word))) and (len(str(word))>=2):
            print(word, count)

def write_to_file(df, pos):
    print('writing to file')
    time.sleep(5)
    filename = '前程无忧'+'_'+paras['city'] + '_' + pos + '_'+'数据导出'+'.csv'
    df.to_csv(filename, encoding='utf_8_sig', index=False, sep=',')
    print('complete writing, you can figure it out in current directory')
    print('********************************************************************************')

def calculation(avg_salaries, min_salaries, max_salaries):
    print('calculating...')
    time.sleep(5)
    position_num=len(avg_salaries)
    for avg_sal in avg_salaries:
        if (avg_sal!=None and avg_sal>=2000):
            average_salaries.append(avg_sal)
    for min_sal in min_salaries:
        if (min_sal != None and min_sal>=2000):
            minimum_salaries.append(min_sal)
    for max_sal in max_salaries:
        if (max_sal!=None and max_sal>=2000):
            maximum_salaries.append(max_sal)
    min_sal_level=np.min(minimum_salaries)
    max_sal_level=np.max(maximum_salaries)
    avg_sal_level=np.mean(average_salaries)
    median_sal_level=np.median(average_salaries)
    #range_level=max_sal_level-min_sal_level
    st_dev=np.std(average_salaries)
    print('complete calculating')
    print('********************************************************************************')
    return position_num, min_sal_level, max_sal_level, avg_sal_level, median_sal_level, st_dev

def write_result_to_file(position_num, min_sal_level, max_sal_level, avg_sal_level, median_sal_level, st_dev, pos):
    print('writing calculation result to file')
    time.sleep(5)
    dataframe=pd.DataFrame({'position_numbers':position_num, 'minimum_salary_level': min_sal_level, 'maximum_salary_level':max_sal_level,
                            'average_salary':avg_sal_level, 'medium_salary':median_sal_level, 'standard deviation':st_dev}, index=[0])
    filename='前程无忧'+'_'+paras['city']+'_'+pos+'_'+'薪酬计算结果'+'.csv'
    dataframe.to_csv(filename, encoding='utf_8_sig', index=False)
    print('complete writing, you can figure it out in current directory')
    print('********************************************************************************')

A_S=[]
def visulization(avg_salaries, avg_sal_level, st_dev, pos):
    print('showing distribution')
    time.sleep(2)
    maxi=avg_sal_level+3*st_dev
    mini=avg_sal_level-3*st_dev
    for i in avg_salaries:
        if str(i).isdigit():
            if int(i)>=mini and int(i)<=maxi:
                A_S.append(int(i))
    tkinter.messagebox.showinfo('{}{}职位空缺数量'.format(location_A, '所有'), len(A_S))
    tkinter.messagebox.showinfo('{}{}职位薪酬均值'.format(location_A, '所有'), np.mean(np.array(A_S)))
    plt.hist(A_S, bins=50, color='g')
    #plt.axvline(min_sal_level, ls=':', color='r')
    #plt.axvline(max_sal_level, ls=':', color='r')
    plt.axvline(avg_sal_level, ls='-', color='k')
    #plt.axvline(avg_sal_level - st_dev, ls='-.', color='k')
    #plt.axvline(avg_sal_level + st_dev, ls='-.', color='k')
    plt_name='前程无忧'+'_'+paras['city']+'_'+pos+'_'+'薪酬分布'
    plt.title(plt_name)
    plt.show()

location_A='成都'
#position='区块链'
get_batch_info(location_A, '区块链')#position
process_salary_info(salary_ranges)
df=tran_list_to_df(job_titles, company_names, cities, districts, min_salaries, max_salaries, avg_salaries, job_info, months, days, work_locations, experiences, degrees, head_counts)
#df=label_keyword(df, '大数据')
word_frequency_statistics(job_info)
write_to_file(df, '职位') #position
position_num, min_sal_level, max_sal_level, avg_sal_level, median_sal_level, st_dev=calculation(avg_salaries, min_salaries, max_salaries)
write_result_to_file(position_num, min_sal_level, max_sal_level, avg_sal_level, median_sal_level, st_dev, '职位') #position
#visulization(avg_salaries, avg_sal_level, st_dev, position)



