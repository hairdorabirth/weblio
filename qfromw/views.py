#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import render
import requests   # Web からデータを取ってくる時に使う
import bs4        # スクレイピング
import re         # 正規表現によるマッチングを使う

his = []    #検索履歴に表示する単語
his_imi = []#検索履歴に表示する単語の意味

def input_word(request):

    #辞書をつくる#
    d = {
        'input': request.GET.get('word'),
    }
    #フォームから入力した単語を変数に保存#
    tango = str(d.get('input'))

    #入力された単語が無ければ例外処理を行う#
    try:

        #Weblio上で入力された単語のページへ飛ぶ#
        res = requests.get('https://ejje.weblio.jp/content/'+tango)

        #bs4でHTMLをスクレイピング#
        soup = bs4.BeautifulSoup(res.text, "html5lib")

        #その単語の音声データの部分を抽出#
        onsei = soup.select('i.fa.fa-volume-up.contentTopAudioIcon source')

        #主な〇〇を抽出#
        omona = soup.select('div.summaryM.descriptionWrp b.squareCircle.description')[0].getText()
        #その単語の意味を抽出・保存#
        imi = soup.select('div.summaryM.descriptionWrp td.content-explanation')[0].getText()
        #print(imi)
        d['mainXX'] = omona

        #正規表現で意味を分割、リストに保存#
        imi_list = re.split('[;、]',imi)
        d['explanation'] = imi_list

        #音声データが登録されていない単語も存在するので、別にtry-exceptを行う#
        try:
            mp3 = re.findall('https://.*mp3' , str(onsei))
            #print('mp3', mp3)
            d['audio'] = mp3[0]
        except:
            d['nomp3'] = 'この単語には音声データが存在しません'

        try:
            #フォームから入力された単語を変数に保存#
            word =d.get('input')
            #inputがNoneの時にexcept処理をするためのダミー#
            len(word)

            #履歴の単語名を保存#
            his.append(word)
            his_imi.append(imi)

            #順序を記憶したまま重複を削除#
            sender = sorted(set(his),key=his.index)
            sender_imi = sorted(set(his_imi),key=his_imi.index)

            #重複した単語をリスト末尾に移動#
            for i in range(len(sender)):
                if sender[i] == word:
                    dedupe = sender[:]
                    dedupe.append(dedupe[i])
                    dedupe.pop(i)
                    dedupe_imi = sender_imi[:]
                    dedupe_imi.append(dedupe_imi[i])
                    dedupe_imi.pop(i)
                    #print('sender',dedupe)
                    sender = dedupe[:]
                    sender_imi = dedupe_imi[:]
            tmp = sender[:]
            tmp_imi = sender_imi[:]
            #最新検索ワードが上に表示されるようにソートしなおす#
            tmp.reverse()
            tmp_imi.reverse()

            #ボタンが押されたら#
            if request.method == 'POST':
                if 'asc' in request.POST:
                    pass
                if 'des' in request.POST:
                    tmp.reverse()
                    tmp_imi.reverse()
                if 'clear' in request.POST:
                    tmp.clear()
                    his.clear()
                    tmp_imi.clear()
                    his_imi.clear()
            #単語名とその意味を同時にまとめたリストの作成
            history = zip(tmp, tmp_imi)
            d['his'] = history

        except:
            #何も入力が無い時、input==Noneなので、リストに追加されるのを防ぐための例外処理#
            print('何も入力が無いのでスルー')

    except:
        e = {
            'error': "その単語は存在しません"
        }
        print('[his_error]',his)
        return render(request, 'input.html',e)
    print('[his]',his)

    return render(request, 'input.html',d)
