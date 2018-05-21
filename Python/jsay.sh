#!/bin/sh
python3 /home/pi/Project/Python/weather.py

TMP=/tmp/jsay.wav
open_jtalk \
-m /usr/share/hts-voice/mei/mei_normal.htsvoice \
-x /var/lib/mecab/dic/open-jtalk/naist-jdic \
-ow $TMP ./today.txt && \
aplay --quiet $TMP
rm -f $TMP

