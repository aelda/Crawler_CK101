# -*- coding: utf8 -*-
import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
import re
import sys
import os
import urllib.request
import ssl
from functools import wraps
def sslwrap(func):
    @wraps(func)
    def bar(*args, **kw):
        kw['ssl_version'] = ssl.PROTOCOL_TLSv1
        return func(*args, **kw)
    return bar

ssl.wrap_socket = sslwrap(ssl.wrap_socket)

'''
url = 'https://ithome.com.tw/'
resp = requests.get(url)
soup = BeautifulSoup(resp.text,'html.parser')
dcard_title = soup.find_all('p',class_ = {'title'})
f = open('result.txt','w')
f.write('iThome\n')
for index , title in enumerate(dcard_title[:10]):
    f.write("{}. {} \n".format(index + 1, title.text))
f.close()
'''
# 403 Http problem 
headers = ('Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1')

url = input ("input the noval website url : ")

driver = webdriver.Chrome() # chrome driver
driver.get(url) 

url = url[:-8]
filename = ''
page = 1;
total_page = 17
while page < total_page + 1:
    # everytime open the url , must use urllib to request the website 
    req = urllib.request.Request(url + str(page)+'-1.html')  # for 403 HTTP Forbidden, some website forbid crawler
    req.add_header("User-Agent",headers)
    files =urllib.request.urlopen(req)

    soup = BeautifulSoup(files , 'html5lib')
    # create the dir
    if page == 1 :
        dir_name = 'noval'
        if not os.path.exists('./' + dir_name) :
            os.mkdir(dir_name)

    filename = 'Page' + str(page)
    f = open('./'+ dir_name +'/' + filename + '.txt','w')
    f.write(soup.title.string)
    lines = soup.select('.postList #pbody .mes .postmessage') # array of content
    index = 0
    lens = len(lines)
    for line in lines :
        f.write(line.text)
        index = index + 1
        sys.stdout.write('\r')
        sys.stdout.write('[%-50s] %d%%' % ('='*int(50/lens*index),index/lens*100))  # progressbar 
        sys.stdout.flush()
    driver.find_element_by_xpath("//a[contains(text(),'下一頁')]").click()  # click to next page
    page = page + 1
    sys.stdout.write('\n'+ soup.title.string+ ' saved \n')
    f.close()
    time.sleep(2)
driver.quit()




