import pyaudio
import sys
import time
import wave

if __name__ == '__main__':
    chunk = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    #サンプリングレート、マイク性能に依存
#    RATE = 44100
    RATE = 48000
     #録音時間
    RECORD_SECONDS = input('Please input recoding time>>>')
    RECORD_SECONDS = int(RECORD_SECONDS)
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
    for i in range(0, int(RATE / chunk * RECORD_SECONDS)):
        data = stream.read(chunk)
        all.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()
#    data = ''.join(all)
    out = wave.open('mono.wav','wb')
    out.setnchannels(1) #mono
    out.setsampwidth(2) #16bits
    out.setframerate(RATE)
    out.writeframes(b''.join(data))
    out.close()
