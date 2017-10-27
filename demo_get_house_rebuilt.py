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
f = open('demo.html','w',encoding='utf-8')
f.write(html)
f.close()

#dl
soup =BeautifulSoup(html,'lxml')

import re
for item in soup.find_all("dl",id = re.compile("list_D03_")) :
    print (item)
    print ('--------------')
