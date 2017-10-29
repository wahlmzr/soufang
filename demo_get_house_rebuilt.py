# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 22:10:32 2017

@author: Administrator
"""

import requests
from bs4 import BeautifulSoup

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0"}

#def get_urls(url):
#    html=requests.get(url,headers=headers).text
#    table=BeautifulSoup(html,'lxml').find('div',attrs={'class':'houseList'}).find_all('div',id='Div1')
#    urls=[]
#    for item in table:
#        urls.append(item.find('div',attrs={'class':'img rel floatl'}).find('a').get('href'))
#    return urls
#
#if __name__=='__main__':
#    for i in range(1,2):
#        url = 'http://esf.sh.fang.com/house-a019/i3%s'%(str(i))
#        print (url)
#        urls = get_urls(url)


i = 1
url = 'http://esf.sh.fang.com/house-a019/i3%s'%(str(i))
html = requests.get(url,headers=headers).text

#dl
soup =BeautifulSoup(html,'lxml')

import re
for item in soup.find_all("dl",id = re.compile("list_D03_")) :
#    print (item)
    print ('--------------')
    id = item['id']
    href = item.a['href']
    print (id , href)
    

href = '/chushou/3_306950858.htm'
root_url = 'http://esf.sh.fang.com'
html = requests.get(root_url+href,headers = headers).text
f = open('demo_detail.html','w',encoding = 'utf8')
f.write(html)
f.close()            


soup =BeautifulSoup(html,'lxml')
#总价
total = soup.find('div',class_ = 'trl-item sty1').i.text

# 标签
a = soup.find('div',class_ = 'bqian clearfix')
    
q = []
for item in a.find_all('span'):
    q.append(item.text)


#基本信息
detail = soup.find_all('div',class_ = 'trl-item1')

d = []
for item in detail:
    for c in item.find_all('div'):
        d.append(c.text.replace('\r\n',''))
values1 = d[::2]
keys1 = d[1::2]
dic1 = dict(zip(keys1, values1))

#小区
community = soup.find('a',id =  'agantesfxq_C03_05').text
#区县
district  = soup.find('a',id =  'agantesfxq_C03_07').text
#街道
subdistrict  = soup.find('a',id =  'agantesfxq_C03_08').text
#对口学校
school  = soup.find('a',id =  'agantesfxq_C03_09').text
#中介                  
agent  =  soup.find('a',id =  'agantesfxq_C04_02').text              
#中介 电话
phone  =  soup.find('span',id = 'mobilecode').text    

#房源信息                 
house_detail = soup.find('div',class_ = 'cont clearfix qu_bianqu1').find_all('span')

house_detail_q = []
for item in house_detail:
    house_detail_q.append(item.text)
values2 = house_detail_q[1::2]
keys2 = house_detail_q[::2]
dic2 = dict(zip(keys2, values2))

#图片
pic_detail = soup.find('div',class_= 'cont-sty1 clearfix').find_all('img')

pic_detail_q = []
for item in pic_detail:
    alt = item.attrs['alt']
    link = item.attrs['data-src']
    pic_detail_q.append([alt,link])

pic_url = 'http://img3n.soufunimg.com/viewimage/agents/2013_11/25/M02/01/67/wKgFk1KSxlCIdF2OAANgi8H1Q08AACMPgDdmTAAA2Cj814/600x450c.jpg'
html = requests.get(pic_url,headers=headers)
with open('picture.jpg', 'wb') as file:
    file.write(html.content)
    file.close()

    

    
    
    
    
    
    
    
    
    
    
    
        