#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import csv
import re
import string
import urllib.request
from bs4 import BeautifulSoup

# 入力出力チェック
argvs = sys.argv
argc = len(argvs)

if (argc != 2):
        print ('please type "python %s url.txt"'%argvs[0])
        sys.exit()

"""
文章を区切って、文にする
入力：クローリングした文章
出力：文
"""

def splitSentence(input):
        input = input.translate(str.maketrans(",","、")) # 句点と区切り点の変換

        # 句読点を区切り点に変換
        symbols = ['w','W','ｗ','W','.','。','?','？','!','！']
        for symbol in symbols:
                if symbol in input:
                        input = input.translate(str.maketrans(symbol,","))

        # 改行を区切りとする文への対策
        div_flag = False
        div_ti = 100
        new_text = ""
        for i,v in enumerate(input):

                if v == ',':
                        div_flag = True
        
                if i == div_ti:        
                        if div_flag == False:
                                new_text = input.replace('<br/>', ',')
                        else:
                                new_text = input.replace('<br/>', '')
                        break
            
                        div_flag = False
                        
        return new_text


if __name__ == "__main__" :
        #0. ファイル読み書き準備
        input_f = open(argvs[1], 'r')

        output_f = open('data.csv', 'w')
        writer = csv.writer(output_f, lineterminator='\n')

        for i,row in enumerate(input_f):
                url = row.strip()
        
                #1-1. Webページ取得
                response = urllib.request.urlopen(url)
                data = response.read()
                soup = BeautifulSoup(data.decode('utf-8', 'ignore'),"lxml")
                outputs = []
                output = []
                review_list= soup.find(id="revwdtl")

                #1-2. レビューURL 
                output.append(url)
        
                #1-3. ユーザーデータ
                userurl_data = review_list.find("a", href=True)
                userurl = "http://movies.yahoo.co.jp"+userurl_data['href']
                output.append(userurl)

                #1-4. 総合評価データ
                star_data = review_list.find("i", class_="star-actived")
                star = re.findall(r'[0-9]+',str(star_data))
                output.append(star)

                #1-5. レビュー本文
                review_data = review_list.find("p")
                texts=""
                review=""
        
                for j in review_data:
                        text = str(j).strip()                                
                        texts += text
                                
                review = splitSentence(texts)
                output.append(review)

                #1-6. 詳細評価
                chart_data = review_list.find("canvas")
                chart = chart_data['data-chart-val-user'].split(",")
                output.append(chart)

                #1-7. イメージワード
                word = []
                word_data = review_list.find_all("span", class_="bgcolor-layer")
                for j in word_data:
                        word.append(j.get_text())
                output.append(word)

                #1-8. 1件レビュー情報の追加
                print(i+1)
                writer.writerow(output)
        
        input_f.close()
        output_f.close()
