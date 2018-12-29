#!usr/bin/python
# -*- coding: utf-8 -*-
# encoding=utf8
import re
import urllib.request
from tqdm import tqdm
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
import tkinter
import tkinter.messagebox
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False

# empty list for storage
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

# attention: city_code为所查询城市编码, 重点城市city_code:
city_dict={'北京':'010000', '上海':'020000', '深圳':'040000', '广州':'030200', '武汉':'180200', '西安':'200200', '杭州':'080200',
           '南京':'070200', '成都':'090200', '重庆':'060000', '大连':'230300', '东莞':'030800', '沈阳':'230200', '苏州':'070300',
           '昆明':'250200', '长沙':'190200', '合肥':'150200', '宁波':'080300', '郑州':'170200', '天津':'050000', '青岛':'120300',
           '济南':'120200', '哈尔滨':'220200', '长春':'240200', '福州':'110200'}
job_dict={'工程':'%25E5%25B7%25A5%25E7%25A8%258B', '新能源':'%25E6%2596%25B0%25E8%2583%25BD%25E6%25BA%2590',
          '人工智能':'%25E4%25BA%25BA%25E5%25B7%25A5%25E6%2599%25BA%25E8%2583%25BD', '生物制药':'%25E7%2594%259F%25E7%2589%25A9%25E5%2588%25B6%25E8%258D%25AF',
          '大数据':'%25E5%25A4%25A7%25E6%2595%25B0%25E6%258D%25AE', '医疗':'%25E5%258C%25BB%25E7%2596%2597'}
def get_one_page_content(city, job_categotry, page=1):
    global paras
    city=str(city)
    job_categotry = str(job_categotry)
    page = str(page)
    paras={'city':city, 'job_categotry':job_categotry}
    city_code=str(city_dict[city])
    job_code=str(job_dict[job_categotry])
    url='https://search.51job.com/list/'+city_code+',000000,0000,00,9,99,'+job_code+',2,'+page+'.html'
    web_content=urllib.request.urlopen(url)
    content=web_content.read().decode('gbk')
    return content

def reg_content(content):
    reg_pattern=re.compile(r'class="t1 ">.*? <a target="_blank" title="(.*?)".*? '
                           r'<span class="t2"><a target="_blank" title="(.*?)".*?'
                           r'<span class="t3">(.*?)</span>.*?'
                           r'<span class="t4">(.*?)</span>.*? '
                           r'<span class="t5">(.*?)</span>', re.S)
    items = re.findall(reg_pattern, content)
    return items

def get_one_page_processed_info(reged_content):
    for item in reged_content:
        job_title = item[0].strip()
        job_titles.append(job_title)
        company_name = item[1].strip()
        company_names.append(company_name)
        company_location = item[2].strip()
        company_location_index = company_location.find('-')
        if company_location_index >= 0:
            cities.append(company_location[0:company_location_index])
            districts.append(company_location[company_location_index + 1:])
        else:
            cities.append(company_location)
            districts.append(None)
        salary_range = item[3].strip()
        salary_ranges.append(salary_range)

def page_job_count(content):
    soup = BeautifulSoup(content, "html.parser")
    text_job = soup.find_all('div', class_='rt')
    text_job=str(text_job[0])
    job_num = int(re.sub("\D", "", text_job))
    text_page=soup.find_all('span', class_='td')
    text_page = str(text_page[0])
    page_num = int(re.sub("\D", "", text_page))
    return job_num, page_num

def get_batch_info(city, job_categotry):
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

def write_to_file(job_titles, company_names, cities, districts, min_salaries, max_salaries, avg_salaries):
    print('writing to file')
    time.sleep(5)
    dataframe=pd.DataFrame({'job_titles':job_titles, 'company_names':company_names, 'cities':cities, 'districts':districts,
                            'salaries_avg':avg_salaries, 'salaries_min':min_salaries, 'salaries_max':max_salaries})
    filename = 'qcwy'+'_'+paras['city'] + '_' + paras['job_categotry'] + '.csv'
    dataframe.to_csv(filename, encoding='utf_8_sig', index=False, sep=',')
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

def write_result_to_file(position_num, min_sal_level, max_sal_level, avg_sal_level, median_sal_level, st_dev):
    print('writing calculation result to file')
    time.sleep(5)
    dataframe=pd.DataFrame({'position_numbers':position_num, 'minimum_salary_level': min_sal_level, 'maximum_salary_level':max_sal_level,
                            'average_salary':avg_sal_level, 'medium_salary':median_sal_level, 'standard deviation':st_dev},
                           index=[0])
    filename='qcwy'+'_'+paras['city']+'_'+paras['job_categotry']+'_'+'计算结果'+'.csv'
    dataframe.to_csv(filename, encoding='utf_8_sig', index=False)
    print('complete writing, you can figure it out in current directory')
    print('********************************************************************************')

A_S=[]
def visulization(average_salaries, min_sal_level, max_sal_level, avg_sal_level, st_dev):
    print('showing distribution')
    time.sleep(2)
    maxi=avg_sal_level+3*st_dev
    mini=avg_sal_level-3*st_dev
    for i in average_salaries:
        if i>=mini and i<=maxi:
            A_S.append(i)
    tkinter.messagebox.showinfo('{}{}职位空缺数量'.format(location_A, position), len(A_S))
    tkinter.messagebox.showinfo('{}{}薪酬分布标准差'.format(location_A, position), np.std(np.array(A_S)))
    plt.hist(A_S, bins=50, color='g')
    #plt.axvline(min_sal_level, ls=':', color='r')
    #plt.axvline(max_sal_level, ls=':', color='r')
    plt.axvline(avg_sal_level, ls='-', color='k')
    #plt.axvline(avg_sal_level - st_dev, ls='-.', color='k')
    #plt.axvline(avg_sal_level + st_dev, ls='-.', color='k')
    plt_name='前程无忧'+'_'+paras['city']+'_'+paras['job_categotry']+'_'+'薪酬分布'
    plt.title(plt_name)
    plt.show()

location_A='深圳'
position='大数据'
get_batch_info(location_A, position)
process_salary_info(salary_ranges)
write_to_file(job_titles, company_names, cities, districts, min_salaries, max_salaries, avg_salaries)
position_num, min_sal_level, max_sal_level, avg_sal_level, median_sal_level, st_dev=calculation(avg_salaries, min_salaries, max_salaries)
#write_result_to_file(position_num, min_sal_level, max_sal_level, avg_sal_level, median_sal_level, st_dev)
visulization(average_salaries, min_sal_level, max_sal_level, avg_sal_level, st_dev)





