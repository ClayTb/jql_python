# -*- coding: utf-8 -*-

'''
这个是用于测试和控制板通信的程序，
使用方法：
1. 停止主程序
2. python ctl-mb.py ttyS1
'''
import serial 
import time, sys

if (len(sys.argv) != 2):
    print 'usage: python ctl-rpi.py ttyUSB0'
    exit(1)

path = '/dev/'+sys.argv[1]
print 'will open ' + path


ser = serial.Serial(path, 115200, timeout=3)
ser.reset_input_buffer()
ser.reset_output_buffer()
#def ctl_rpi():
x=''
while True:
    x = ser.readline()
    #x = ser.read()
    #print "recv: "+":".join("{:02x}".format(ord(c)) for c in x)
        
    if x:
        print x
        x='' 
