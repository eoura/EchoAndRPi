from fractions import Fraction
import numpy as np



import scipy.signal as sg
import soundfile as sf

import pyaudio
# import sys
# import time
import wave
import requests
import os
import json



def convert_rate():
# wavファイルのサンプリングレートを変更する
# 48kHz → 16kHzに変換する
#
    fs_target = 16000
    cutoff_hz = 21000.0
    n_lpf = 4096

    sec = 3

    wav, fs_src = sf.read(PATH)
    wav_48kHz = wav[:fs_src * sec]

    frac = Fraction(fs_target, fs_src)  # 16000 / 48000

    up = frac.numerator  # 147
    down = frac.denominator  # 160

    # up sampling
    wav_up = np.zeros(np.alen(wav_48kHz) * up)
    wav_up[::up] = up * wav_48kHz
    fs_up = fs_src * up

    cutoff = cutoff_hz / (fs_up / 2.0)
    lpf = sg.firwin(n_lpf, cutoff)

    # filtering and down sampling
    wav_down = sg.lfilter(lpf, [1], wav_up)[n_lpf // 2::down]

    # write wave file
    sf.write(PATH_DOWN, wav_down, fs_target)

    return 0


def recognize():
# 16kHzに変換したwavファイルをdocomo Developer Support の音声認識APIに渡して
# テキスト変換する
#
    url = "https://api.apigw.smt.docomo.ne.jp/amiVoice/v1/recognize?APIKEY={}".format(APIKEY)
    files = {"a": open(PATH_DOWN, 'rb'), "v":"on"}
    r = requests.post(url, files=files)
#    print('r:',r)
    message = r.json()['text']
    print('recognize_message:', message)
    return message

def dialogue(message="こんにちは"):
# docomo Developer Supportの雑談APIに音声認識したテキストを渡して雑談する。
#
#
    url = "https://api.apigw.smt.docomo.ne.jp/dialogue/v1/dialogue?APIKEY={}".format(APIKEY)
    payload = {
      "utt": message,
      "context": "",
      "nickname": "恵司",
      "nickname_y": "エイジ",
      "sex": "男",
      "bloodtype": "B",
      "birthdateY": "1990",
      "birthdateM": "2",
      "birthdateD": "4",
      "age": "16",
      "constellations": "水瓶座",
      "place": "東京",
      "mode": "dialog",
      "t":20
    }
    r = requests.post(url, data=json.dumps(payload))
    print (r.json()['utt'])
    return r.json()['utt']

def talk(message="こんにちは", card=1, device=0):
# 雑談APIからの戻りのテキストを音声に変換
# AquesTaliPi を使用。-b:抑揚をなくす -s 80 :喋るスピード default:100
# 変換した音声をaplay で鳴らす。

    print('talk_in_message:',message)
#    os.system(  '/home/pi/aquestalkpi/AquesTalkPi " ' + message.encode('utf-8') + ' " | aplay -Dhw:{},{}').format(card, device)
    comand_txt = '/home/pi/aquestalkpi/AquesTalkPi -b -s 83 "'+ message + '" | aplay -Dhw:'+ str(card) + ',' + str(device)
    print ('comand_txt:'+comand_txt)
    os.system(comand_txt)

if __name__ == '__main__':
    chunk = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    PATH = '/var/tmp/tmp.wav'
    PATH_DOWN = '/var/tmp/tmp_down.wav'
    with open("APIKEY.txt","r") as f:
        APIKEY =f.read()
    CARD = 1 #OUTPUTの指定
    DEVICE = 0 #OUTPUTの指定
    #サンプリングレート、マイク性能に依存(このマイクは48kHz対応)
    RATE = 48000
    #録音時間
#    RECORD_SECONDS = input('Please input recoding time>>>')
    RECORD_SECONDS = 3

    #pyaudio
    p = pyaudio.PyAudio()

    #マイク0番を設定
    input_device_index = 0
    #マイクからデータ取得
    stream = p.open(format = FORMAT,
                    channels = CHANNELS,
                    rate = RATE,
                    input = True,
                    frames_per_buffer = chunk)
    all = []
    for i in range(0, int(RATE / chunk * RECORD_SECONDS) ):
        data = stream.read(chunk)
        all.append(data)
    stream.stop_stream()
    stream.close()

#    data = ''.join(all)
    out = wave.open(PATH,'wb')
    out.setnchannels(1) #mono
    out.setsampwidth(2) #16bits
    out.setframerate(RATE)

#*ここで16kHzを指定して書き出してもスロー再生したような間延びが発生するのでNG
#    out.setframerate(16000) 
    out.writeframes(b''.join(all))
    out.close()
    p.terminate()
    #サンプリングレート変換48kHz → 16kHzに変換（APIが16kHzのみ対応）
    ret = convert_rate()
    #録音したメッセージを文字認識させる
    message = recognize()
    #docomo Developer Supportの雑談APIに渡す
    talk_message = dialogue(message)
    #雑談APIの戻りを喋らせる
    talk(talk_message, CARD, DEVICE)


