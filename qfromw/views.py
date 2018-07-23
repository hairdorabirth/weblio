#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import render
import requests   # Web からデータを取ってくる時に使う
import bs4        # スクレイピング
import re         # 正規表現によるマッチングを使う
from qfromw.forms import inputForm

def input_word(request):

    #辞書をつくる
    d = {
        'input': request.GET.get('word'),
    }

    tango = str(d.get('input'))
    print(tango)
    res = requests.get('https://ejje.weblio.jp/content/'+tango)
    soup = bs4.BeautifulSoup(res.text, "html5lib")

    try:
        imi = soup.select('div.summaryM.descriptionWrp td.content-explanation')[0].getText()
        d['explanation'] = imi
    except:
        e = {
            'error': "その単語は存在しません"
        }
        return render(request, 'input.html',e)
    return render(request, 'input.html',d)

def appmain(request):

    form = inputForm()
    #if request.method == 'POST':


    word = 'What'
    res = requests.get('https://ejje.weblio.jp/content/'+word)
    soup = bs4.BeautifulSoup(res.text, "html5lib")

    try:
        explanation = soup.select('div.summaryM.descriptionWrp td.content-explanation')[0].getText()
        #print(explanation)
    except:
        print('そのページは存在しない')
    # この Wiki エントリのタイトルの文字列を変数 title に代入
    #title = soup.select("#firstHeading")[0].getText()


    # この Wiki エントリのトップにある説明文だけ取り出して変数 description に代入
    #description = soup.select('div.mw-content-ltr p')[0].getText()
    # ( ) 内に答えにつながる言葉があるエントリが多いので，( ) は取り除いてしまう．最短マッチが重要
    #description2 = re.sub(r"（.*?）|(.*?)", ' ', description)

    # 答えに当たる部分を ◯ で置き換える．文字数が同じなのはヒントのため
    #description3 = description2.replace(title, '◯' * len(title))

    # 答えが置き換わったときだけクイズにする
    #if description2 != description3:
    #    break

    # demo/main.hml に値を渡す
    return render(request, 'demo/main.html', {
        'answer' : word,
        'descr' : explanation,
    })
