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

    #入力した文字　
    tango = str(d.get('input'))
    #print(tango)
    res = requests.get('https://ejje.weblio.jp/content/'+tango)
    soup = bs4.BeautifulSoup(res.text, "html5lib")

    onsei = soup.select('i.fa.fa-volume-up.contentTopAudioIcon source')
    print('音声', onsei)
    mp3 = re.findall('https://.*mp3' , str(onsei))
    print('mp3', mp3)

    try:
        imi = soup.select('div.summaryM.descriptionWrp td.content-explanation')[0].getText()

        d['explanation'] = imi
    except:
        e = {
            'error': "その単語は存在しません"
        }
        return render(request, 'input.html',e)

    return render(request, 'input.html',d)
