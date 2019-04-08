# -*- coding: utf-8 -*-

#Author: matt ji
#purpose: 接收串口数据，并发送串口数据
#date: 2019/4/8
#usage: put in rc.local python -u tx-rx.py >> log
import serial
import time, datetime
import os
import json, sys
import threading    
import serial, json
import time, sys
ser = None
exitFlag = 0

def ser_recv():
    while True:
        if exitFlag:
            print("thread exit")
            exit(0)
        buffer = ser.readline()
        #buffer = ser.read()
        if buffer:
        #    if buffer[0] == '+':
        #        now = datetime.datetime.now()
        #        print("%s %s" % (now.strftime("%Y-%m-%d %H:%M:%S"), buffer))
            print buffer
            print "recv: "+":".join("{:02x}".format(ord(c)) for c in buffer)
        else:
            print ("no data")
        time.sleep(0.05)
    
def main():
    global ser 
    print len(sys.argv)
    if (len(sys.argv) != 2):
        print 'usage: python rx.py ttyUSB0'
        exit(1)
    path = '/dev/'+sys.argv[1]
    print 'will open ' + path
    ser = serial.Serial(path, 115200, timeout=2)
    t = threading.Thread(name = 'recv', target = ser_recv)
    t.start()
    global exitFlag    
    print "usage: 1: 开门，0: 关门, q:exit"
    while True:
        char = raw_input()
        if (char == "q"):
            print("exit")
            exitFlag = 1
            exit(0)
        elif (char == "1"):
            print("开门")
            ser.write("1")
        elif (char == "0"):
            print("关门")
            ser.write("0")
        else :
            print 'you input '+char + '\n'
            sleep(0.2)

    
    
if __name__ == '__main__':
    main()
