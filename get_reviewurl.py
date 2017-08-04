#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import csv
import urllib.request
from bs4 import BeautifulSoup

argvs = sys.argv
argc = len(argvs)

if (argc != 4):
    print('please type "python %s url total_review outputfile"'%argvs[0])
    print('sample:"python %s https://movies.yahoo.co.jp/movie/ハーモニー/351840/review/  100 url.txt"'%argvs[0])
    sys.exit()

review_page = (int(argvs[2])/10)+1

#0.ファイルへ書き込み準備
f = open(argvs[3], 'w')

for i in range(int(review_page)):
    #1.Webページ取得
    url=argvs[1]+'?page='+str(i+1)
    response = urllib.request.urlopen(url)
    data = response.read()
    soup = BeautifulSoup(data.decode('utf-8', 'ignore'))
    
    #2.該当箇所の抽出
    review_list= soup.find(id="revwlst")
    for a in review_list.find_all("a", href=True):
        output = "http://movies.yahoo.co.jp"+a['href']+"\n"
        f.write(output)
    print(i+1)

f.close()
    
