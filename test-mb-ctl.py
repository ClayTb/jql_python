# -*- coding: utf-8 -*-

'''
1. 这是一个测试程序，实际产品中不运行
2. 主要模拟主控发送数据给控制板
3. 需要安装sudo pip install crcmod
'''
import serial, json
import time, sys, crcmod, struct
from random import *
crc16 = crcmod.mkCrcFun(0x18005, rev=True, initCrc=0xFFFF, xorOut=0x0000)
HEADER=0xFE
#print len(sys.argv)
if (len(sys.argv) != 2):
    print 'usage: python rpi-ctl.py ttyUSB0'
    exit(1)
#mode = ['uwb', 'app', 'navi']
#rcfd = {'mode':mode[0], 'lv':'0', 'av':'0'}
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
    data1 = struct.pack('!BBhhhh', HEADER, rcp[1], rcp[2], rcp[3], rcp[4], rcp[5])
    crc = crc16(data1)
    data = struct.pack('!BBhhhhH', HEADER, rcp[1], rcp[2], rcp[3], rcp[4], rcp[5], crc) 
    #print ":".join("{:02x}".format(ord(c)) for c in data)
    #print rcp
    try: 
        ser.write(data)
    except Exception, e:
        print e
        pass
    else:
        pass
    print rcp
    ser.write(data)
    time.sleep(1)
