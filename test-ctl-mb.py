# -*- coding: utf-8 -*-

'''
这个是用于测试和控制板通信的程序，
使用方法：
1. 停止主程序
2. python ctl-mb.py ttyS1
'''
import serial, json, threading
import time, sys
from random import *
import struct
import crcmod, json
#print len(sys.argv)
'''
[1,20,10,100]
'''
if (len(sys.argv) != 2):
    print 'usage: python ctl-rpi.py ttyUSB0'
    exit(1)

path = '/dev/'+sys.argv[1]
print 'will open ' + path
def parse_ctl(data):
    try:
        pkt = json.loads(data)
        print pkt
    except Exception, e:
        print "this packet is wrong"

ser = serial.Serial(path, 115200, timeout=3)
ser.reset_input_buffer()
ser.reset_output_buffer()
#def ctl_rpi():
x=''
while True:
    x = ser.readline()
    #print "recv: "+":".join("{:02x}".format(ord(c)) for c in x)
        
    if x:
        parse_ctl(x)
        x='' 
