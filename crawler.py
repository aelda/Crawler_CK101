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

url = input ("input the noval url at CK101 website: ")

if not os.path.exists('./noval') :
    os.mkdir('noval')

driver = webdriver.Chrome() # chrome driver
driver.get(url) 

url = url[:-8]
filename = ''
page = 1;
requestUrl(url,page)
total_page = soup.find(class_='last').text

while page < total_page + 1:
    requestUrl(url,page)
    filename = 'Page' + str(page)
    f = open('./noval/' + filename + '.txt','w')
    f.write(soup.title.string)
    lines = soup.select('.postList #pbody .mes .postmessage') # array of content
    index = 0
    lens = len(lines)
    for line in lines :
        f.write(line.text)
        index = index + 1
        # progressbar
        sys.stdout.write('\r')
        sys.stdout.write('[%-50s] %d%%' % ('='*int(50/lens*index),index/lens*100))   
        sys.stdout.flush()
    # click to next page    
    driver.find_element_by_xpath("//a[contains(text(),'下一頁')]").click()  
    page = page + 1
    sys.stdout.write('\n'+ soup.title.string+ ' saved \n')
    f.close()
    time.sleep(2)
driver.quit()

def requestUrl(url,page):
    # everytime open the url , must use urllib to request the website 
    headers = ('Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1')
    req = urllib.request.Request(url + str(page)+'-1.html')  # for 403 HTTP Forbidden, some website forbid crawler
    req.add_header("User-Agent",headers)
    files = urllib.request.urlopen(req)
    soup = BeautifulSoup(files , 'html5lib')

