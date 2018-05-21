# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 11:50:46 2018

@author: e.oura
"""

import urllib.request
import json

id = '130010'
url = 'http://weather.livedoor.com/forecast/webservice/json/v1?city=' + str(id)
talk_txt = ''
response = urllib.request.urlopen(url)

content = json.loads(response.read().decode('utf8'))
#print(content)

print(content['title'])
#talk_txt = talk_txt + content['title']

print('今日の天気は'+ content['forecasts'][0]['telop']+'です。\n')
talk_txt = talk_txt + '今日の天気は'+ content['forecasts'][0]['telop']+'です。'
talk_txt = talk_txt.replace('\n','')
talk_txt = talk_txt.replace('【','')
talk_txt = talk_txt.replace('】','')

if content['forecasts'][0]['temperature']['min'] == None:
    print('最低気温は不明です。 ')
    talk_txt = talk_txt + '最低気温は不明です。 '
else:
    print('最低気温は'+ content['forecasts'][0]['temperature']['min']['celsius']+'度です。 ')
    talk_txt = talk_txt + '最低気温は'+ content['forecasts'][0]['temperature']['min']['celsius']+'度です。'

if content['forecasts'][0]['temperature']['max'] == None:
    print('最高気温は不明です。 ')
    talk_txt = talk_txt + '最高気温は不明です。 '
else:
    print('最高気温は'+ content['forecasts'][0]['temperature']['max']['celsius']+'度です。')
    talk_txt = talk_txt + '最高気温は'+ content['forecasts'][0]['temperature']['max']['celsius']+'度です。'
print('\n')

print(content['description']['text'])
talk_txt = talk_txt + content['description']['text']
talk_txt = talk_txt.replace('\n','')
talk_txt = talk_txt.replace('【','')
talk_txt = talk_txt.replace('】','')


print('\n')

print('明日の天気は'+ content['forecasts'][1]['telop']+'です。\n')
#talk_txt = talk_txt + '明日の天気は'+ content['forecasts'][1]['telop']+'です。'

if content['forecasts'][1]['temperature']['min'] == None:
    print('最低気温は不明です。 ')
#    talk_txt = talk_txt + '最低気温は不明です。 '
else:
    print('最低気温は'+ content['forecasts'][1]['temperature']['min']['celsius']+'度です。 ')
#    talk_txt = talk_txt + '最低気温は'+ content['forecasts'][1]['temperature']['min']['celsius']+'度です。'

if content['forecasts'][1]['temperature']['max'] == None:
    print('最高気温は不明です。 ')
#    talk_txt = talk_txt + '最高気温は不明です。 '
else:
    print('最高気温は'+ content['forecasts'][1]['temperature']['max']['celsius']+'度です。')
#    talk_txt = talk_txt + '最高気温は'+ content['forecasts'][1]['temperature']['max']['celsius']+'度です。'

print('\n')

print(talk_txt)

f = open('today.txt', 'w')
f.write(talk_txt)
f.close() 

