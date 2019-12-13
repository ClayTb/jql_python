#Author: matt ji
#purpose: check 4g wireless signal strength
#date: 2019/1/3
#usage: python ./4g.py
import serial
import time
from datetime import datetime
import os
import json, sys
import os, threading
import logging

#ser = serial.Serial("/dev/ttyUSB0", 115200, timeout=3)
#ser = serial.Serial(sys.argv[1], 9600)
exitFlag = 0

def check():
    global exitFlag
    logging.basicConfig(filename=datetime.now().strftime('%Y-%m-%d-%I:%M:%S.log'),level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    print("check 4g wireless strength")
    os.system('service ModemManager stop')
    dbmDict = {'2':'-109','3':'-107','4':'-105','5':'-103','6':'-101','7':'-99','8':'-97','9':'-95','10':'-93','11':'-91','12':'-89','13':'-87','14':'-85','15':'-83','16':'-81','17':'-79','18':'-77','19':'-75','20':'-73','21':'-71','22':'-69','23':'-67','24':'-65','25':'-63','26':'-61','27':'-59','28':'-57','29':'-55','30':'-53'}
    ser = serial.Serial(port="/dev/ttyUSB0", baudrate=115200, exclusive= True,timeout=3)
    while True:
        if exitFlag:
            print("thread exit")
            exit(0)
  
        ser.write('AT+CSQ\r\n')
		#ser.write("AT\r\n")
		#print("write(AT+CSQ)")
	    #+CSQ: 18,99
		#buffer = ser.readline()
        buffer = ser.readline()
		#buffer = ser.read()
        if buffer:
            if buffer[0] == '+':
                list = buffer.split(':')
                list2 = list[1].split(',')
                list3 = list2[0].split()
		        #print list3
                str = list3[0]
                if int(str) < 10:
                    condition = "Marginal"
                elif int(str) < 15:
                    condition = "OK"
                elif int(str) < 19:
                    condition = "Good"
                elif int(str) < 31:
                    condition = "Excellent"
                print("%s get signal strength %sdbm %s" % (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), dbmDict[str], condition))
                #logger.info(datetime.now())
                logger.info("%s get signal strength %sdbm %s" % (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), dbmDict[str], condition))
		    #print "recv: "+":".join("{:02x}".format(ord(c)) for c in buffer)
        else:
            print ("no data")
        time.sleep(1)

def main():
    global exitFlag
    t = threading.Thread(name = 'check', target = check)
    t.start()
    while True:
        char = raw_input()
        if (char == "q"):
            print("exit")
            exitFlag = 1
            os.system('service ModemManager start')
            exit(0)
        else :
            print "q:exit"
            time.sleep(0.2)

if __name__ == '__main__':
    main()



