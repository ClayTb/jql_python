#Author: matt ji
#purpose: check 4g wireless signal strength
#date: 2019/1/3
import serial
import time, datetime
import os
import json, sys

#ser = serial.Serial("/dev/ttyUSB0", 115200, timeout=3)
#ser = serial.Serial(sys.argv[1], 9600)
print("check 4g wireless strength\n")
ser = serial.Serial("/dev/ttyUSB2", 9600, timeout=3)
while True:
    ser.write('AT+CSQ\r\n')
    #ser.write("AT\r\n")
    #print("write(AT+CSQ)")
    buffer = ser.readline()
    buffer = ser.readline()
    if buffer:
        if buffer[0] == '+':
            now = datetime.datetime.now()
            print("%s %s" % (now.strftime("%Y-%m-%d %H:%M:%S"), buffer))
        #print "recv: "+":".join("{:02x}".format(ord(c)) for c in buffer)
    else:
        print ("no data")
    time.sleep(1)
