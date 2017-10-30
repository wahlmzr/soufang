# -*- coding: utf-8 -*-
"""
Created on Sat Oct 28 01:46:03 2017

@author: Administrator
"""

import requests
from bs4 import BeautifulSoup
import re
import pymysql
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}

start_url = 'http://esf.sh.fang.com/house-a019/i31/'

def get_page_num(start_url):
    #下载网页
    html = requests.get(start_url,headers = headers).text
    #开始soup解析
    soup = BeautifulSoup(html,'lxml')
    #现在class= txt 是对应的位置
    page = soup.find('span',class_= 'txt')
    #先进行正则，形成list后取第一个，再返回int
    pages =  int(re.findall('\d+',page.text)[0])
    
    #获取所有链接的ID和href
    L = []
    for item in soup.find_all("dl",id = re.compile("list_D03_")) :
    #    print (item)

#        id = item['id']
        href = item.a['href']
        L.append(href)

    return (pages ,L)

def house_detail_q_parse(house_detail_q):
    pass

#url是短地址
def web_parse(link):
    url =root_url+ link
    html = requests.get(url,headers = headers).text
    soup =BeautifulSoup(html,'lxml') 
    
    #房子总价
    total = soup.find('div',class_ = 'trl-item sty1').i.text
#    #优质的标签 ，不再提取
#    a = soup.find('div',class_ = 'bqian clearfix')
    
#    q = []
#    for item in a.find_all('span'):
#        q.append(item.text)
#    feature = ' '.join(q)
    
    #基本信息，这是固定的
    detail = soup.find_all('div',class_ = 'trl-item1')

    d = []
    for item in detail:
        for c in item.find_all('div'):
            d.append(c.text.replace('\r\n',''))
    d = d[::-1]
    keys1 = d[::2]
    values1  = d[1::2]
    dic1 = dict(zip(keys1, values1))
    
    #小区
    community = soup.find('a',id =  'agantesfxq_C03_05').text
    #区县
    district  = soup.find('a',id =  'agantesfxq_C03_07').text
    district = district.replace('\r\n','').strip()                
    #街道
    subdistrict  = soup.find('a',id =  'agantesfxq_C03_08').text
    subdistrict = subdistrict.replace('\r\n','').strip() 
#    #对口学校不再取
#    try:
#        #对口学校
#        school  = soup.find('a',id =  'agantesfxq_C03_09').text
#    except :
#        school = ''
#    #中介不再取                  
#    agent  =  soup.find('a',id =  'agantesfxq_C04_02').text              
#    #中介 电话不再取    
#    phone  =  soup.find('span',id = 'mobilecode').text    
#    
    #房源信息，这个是可以变化的            
    house_detail = soup.find('div',class_ = 'cont clearfix qu_bianqu1').find_all('span')

    house_detail_q = []
    for item in house_detail:
        house_detail_q.append(item.text)
    #list比较繁琐，组成了一个字典
    values2 = house_detail_q[1::2]
    keys2 = house_detail_q[::2]
    dic2 = dict(zip(keys2, values2))
    
#    #路径不再取
#    file_dir = link.replace('/chushou/','').replace('.htm','')
    
#    #图片不再取
#    pic_detail = soup.find('div',class_= 'cont-sty1 clearfix').find_all('img')
#
#    pic_detail_q = []
#    for item in pic_detail:
#        alt = item.attrs['alt']
#        link = item.attrs['data-src']
#        pic_detail_q.append([alt,link])
    
    data = {}
    data['url'] = url
    data['total'] = total
#    data['feature'] = feature   
    data['dic1'] = dic1   
    data['community'] = community   
    data['district'] = district   
    data['subdistrict'] = subdistrict   
#    data['school'] = school   
#    data['agent'] = agent   
#    data['phone'] = phone   
    data['dic2'] = dic2  
#    data['file_dir'] = file_dir  
    
    return data

def connect_mysql():
    conn = pymysql.connect('localhost','root','1987','fang',charset = 'utf8')
    cursor = conn.cursor()
    return cursor


def write_mysql(config):
    pass




pages , links = get_page_num(start_url)
print ('一共有%s页'%(pages))


cursor = connect_mysql()

root_url = 'http://esf.sh.fang.com'

for page in range(1,pages+1):
#    print ('开始爬搜索的第%d页'%(page))
    for link in links:
    
        print (root_url+link)
        
        data = web_parse(link)  
      
        url = data['url'] 
        total = data['total'] 
#        feature= data['feature']   
        dic1= data['dic1']  
    
    
    
        if '单价' in dic1.keys():
            avg = re.findall('\d+', dic1['单价'])[0]
        if '建筑面积' in dic1.keys():
            area = re.findall('\d+', dic1['建筑面积'])[0]
        if '朝向' in dic1.keys():
            direct = dic1['朝向']
        if '户型' in dic1.keys():
            house_type = dic1['户型']
    
        
        floor_pos_index = [x[1] for x in dic1.items() if '楼层' in x[0]]
        try:
            floor_pos= floor_pos_index[0]
        except :
            floor_pos = 'Null'
        floor_max_find = [x[0] for x in dic1.items() if '楼层' in x[0]]
        try:
            floor_max_index = floor_max_find[0]
        except :
            floor_max_index='null'
        
        try:
            floor_max_re = re.findall('\d+',floor_max_index)[0]
            floor_max = int(floor_max_re)
        except :
            floor_max = 'Null'
        try :
            decorate = dic1['装修']
        except :
            decorate = 'Null'
        community =   data['community']  
        district =   data['district']
        subdistrict =   data['subdistrict']  
#        school  =  data['school']   
#        agent  =  data['agent']  
#        phone =   data['phone'] 
        dic2 =  data['dic2'] 
    
    
        if '建筑年代' in dic2.keys():
            built_year =int( re.findall('\d+', dic2['建筑年代'])[0])
        
        
        if '有无电梯' in dic2.keys():
            lift = dic2['有无电梯']
        
        if '产权性质' in dic2.keys():
            attr = dic2['产权性质']
    
        if '住宅类别' in dic2.keys():
            house_classify = dic2['住宅类别']
        
        
        if '建筑结构' in dic2.keys():
#            struct = dic2['建筑结构']
        
        if '建筑类别' in dic2.keys():
            attr = dic2['建筑类别']
        
        if '挂牌时间' in dic2.keys():
            create_date = dic2['挂牌时间'][:10]
    
        
#        file_dir=   data['file_dir']   
    
        cursor = connect_mysql()
        sql = """
              insert into house  (href	,
                                    total	,
                                    house_type	,
                                    area	,
                                    avg	,
                                    direct	,
                                    floor_pos	,
                                    floor_max	,
                                    decorate	,
                                    community	,
                                    district	,
                                    subdistrict	,
                                    built_year	,
                                    lift	,
                                    house_classify	,
                                    struct	,
                                    attr	,
                                    create_date	)
              values(
            '%s'	,'%s'	,'%s'	,'%s'	,'%s'	,'%s'	,
            '%s'	,'%s'	,'%s'	,'%s'	,'%s'	, '%s'	,
            '%s'	,'%s'	,'%s'	,'%s'	,'%s'	, '%s'	)"""%(url ,
                  total	,
                  house_type	,
                  area	,
                  avg	,
                  direct	,
                  floor_pos	,
                  str(floor_max)	,
                  decorate	,
                  community	, 
                  district	,
                  subdistrict	,
                  built_year	,
                  lift		,
                  house_classify	,
                  struct	,
                  attr	,
                  create_date)

        cursor.execute(sql)
        cursor.execute('commit')
        
        


        
    



    