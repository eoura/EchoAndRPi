import pyaudio
import wave

CHUNK = 1024
FORMAT = pyaudio.paInt16 # int16型
CHANNELS = 1             # mono:1 ステレオ:2
RATE = 48000             # 441.kHz
RECORD_SECONDS = 5       # 5秒録音
WAVE_OUTPUT_FILENAME = "output.wav"

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("* recording")
frames = []
#RECORD_SECONDS = input('Please input recording time>>>')
#RECORD_SECONDS = int(RECORD_SECONDS.replace('\n',''))

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    print('RATE:',RATE)
    print('CHUNK:',CHUNK)
    print('RECORD_SECONDS:',RECORD_SECONDS)
    print('RATE/CHUNK*RECORD_SECONDS:',RATE/CHUNK*RECORD_SECONDS)
    print('int(RATE / CHUNK * RECORD_SECONDS):',int(RATE/CHUNK*RECORD_SECONDS))

    data = stream.read(CHUNK)
    frames.append(data)

print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()
