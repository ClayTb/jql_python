# -*- coding: utf-8 -*-

'''
2. 主要模拟主控发送数据给控制板
'''
import serial, json
import time, sys
from random import *

HEADER=0xFE
if (len(sys.argv) != 2):
    print 'usage: python rpi-ctl.py ttyUSB0'
    exit(1)
MODE={"uwb":1, "app":2, "navi":3}
rcp = [HEADER, MODE['app'], 0 , 0, 0, 0]
path = '/dev/'+sys.argv[1]
print 'will open ' + path
ser = serial.Serial(path, 115200, timeout=3)
while True:
#线速度
    rcp[2] = randint(1,100)
#角速度
    rcp[3] = randint(1,100)
    #print ":".join("{:02x}".format(ord(c)) for c in data)
    #print rcp
    try: 
        ser.write(rcp)
    except Exception, e:
        print e
        pass
    else:
        pass
    time.sleep(1)
