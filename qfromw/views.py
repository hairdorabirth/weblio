#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import render
import requests   # Web からデータを取ってくる時に使う
import bs4        # スクレイピング
import re         # 正規表現によるマッチングを使う
from qfromw.forms import inputForm

his = []


def input_word(request):

    #辞書をつくる
    d = {
        'his': his,
        'input': request.GET.get('word'),
    }
    #word_his()

    #入力した文字　
    tango = str(d.get('input'))
    #print(tango)
    res = requests.get('https://ejje.weblio.jp/content/'+tango)
    soup = bs4.BeautifulSoup(res.text, "html5lib")

    onsei = soup.select('i.fa.fa-volume-up.contentTopAudioIcon source')
    #print('音声', onsei)


    try:
        imi = soup.select('div.summaryM.descriptionWrp td.content-explanation')[0].getText()
        d['explanation'] = imi
        try:
            mp3 = re.findall('https://.*mp3' , str(onsei))
            #print('mp3', mp3)
            d['audio'] = mp3[0]
        except:
            pass
    except:
        e = {
            'error': "その単語は存在しません"
        }
        return render(request, 'input.html',e)
    his.append(d.get('input'))
    #print('履歴',his)
    return render(request, 'input.html',d)
