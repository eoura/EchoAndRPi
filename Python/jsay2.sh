#!/bin/sh
python3 /home/pi/Project/Python/weather.py

TMP=/tmp/jsay.wav
/home/pi/aquestalkpi/AquesTalkPi  \
-b -s 82 \
-f ./today.txt -o  $TMP  && \
aplay --quiet $TMP
rm -f $TMP

