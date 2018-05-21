# モジュールをインポート
import RPi.GPIO as GPIO
import time
 
# daemon化に必要
#from daemon import daemon
#from daemon.pidlockfile import PIDLockFile
 
# GPIOのピン番号を定義
GPIO18 = 19
 
# 周波数を定義
Hz = 60
 
#=================
# CPUの温度を取得
#=================
#def get_CPU_Temperature():
#    temp = "0"
# 
#    f = open("/sys/class/thermal/thermal_zone0/temp", "r")
#    for t in f:
#        temp=t[:2] + "." + t[2:5]
#    f.close()
 
#    return float(temp)
 
#=========
# PWM実行
#=========
#def exec_pwm():
    #--------------------------------------
    # GPIOを物理的なピン番号で指定する場合
    #--------------------------------------
    ## GPIOピン番号の定義方法
    #GPIO.setmode(GPIO.BOARD)
    ## 出力モードで初期化
    #GPIO.setup(12, GPIO.OUT)
    ## PWM初期化
    #p = GPIO.PWM(12, Hz)
 
    #------------------------
    # GPIO番号で指定する場合
    #------------------------
    # GPIOピン番号の定義方法
GPIO.setmode(GPIO.BCM)
    # 出力モードで初期化
GPIO.setup(GPIO18, GPIO.OUT)
    # PWM初期化
p = GPIO.PWM(GPIO18, Hz)

try:
        # 100%の出力で、1秒間動かす
        # 最初の出力が小さすぎて、ファンが回らない場合の対策
    Duty = 100
    p.start(Duty)
    time.sleep(1)
 
    while True:
            # CPUの温度を取得
        temp = "0"
 
        f = open("/sys/class/thermal/thermal_zone0/temp", "r")
        for t in f:
            temp=t[:2] + "." + t[2:5]
#            f.close()
            
 #           CPU_Temp = get_CPU_Temperature()
        CPU_Temp = temp
 
            # CPUの温度によって出力を変更
            #-------------------------
            #       ～20.0℃ -->  25%
            # 20.0℃～25.0℃ -->  50%
            # 25.0℃～30.0℃ -->  75%
            # 30.0℃～       --> 100%
            #-------------------------
        if CPU_Temp < 30.0:
            Duty = 25
        elif CPU_Temp < 40.0:
            Duty = 50
        elif CPU_Temp < 45.0:
            Duty = 75
        else:
            Duty = 100
 
            # 出力を変更して、30秒間待機
        p.ChangeDutyCycle(Duty)
        time.sleep(30)
 
except Exception as e:
        # 例外処理
    print( "[例外発生] PWM_FanCooler_d.py を終了します。")
    print("Exception : " + str(e))
    print("     Type : " + str(type(e)))
    print("     Args : " + str(e.args))
    print("  Message : " + e.message)
finally:
        # PWMを終了
    p.stop()
 
        # GPIO開放
    GPIO.cleanup()
 
#if __name__ == "__main__":
 #   # PIDファイルの書き込みに失敗してデーモンが動かない事があるので、少し時間をずらす
#    time.sleep(1)
# 
 #   # /etc/init.d/PWM_FanCooler.sh のPIDファイルとは別名にする
 #   with daemon.DaemonContext(pidfile=PIDLockFile('/var/run/PWM_FanCooler_d.pid')):
  #      exec_pwm()

