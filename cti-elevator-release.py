# -*- coding: utf-8 -*-
#author: matt ji
#date: 2019/1/8
#purpose: check wifi 4g signal strength, and then switch between them
#         使用vlc来播放不同地址的视频，wifi就播放高清的，4g就播放低分辨率的
#history:
#rtsp://10.42.0.249:9554/webcam
#rtsp://112.74.184.237/webcamtest
#add logging module support，可以打印log到屏幕以及文件
#add ping thread，同时加入ping操作来实时查看网络连通性

from time import sleep
import serial
import time, datetime
import os
import json, sys
import logging
from datetime import datetime
import threading, subprocess
import thread

MODE = "unknown"
SSID = "cti-elevator"
PATH = "/etc/NetworkManager/system-connections/cti-elevator"
PWD = "12345678"
IFACE = "wlp2s0"
#这里可能有gsm和cdma两种可能
CMDM = "nmcli device | grep gsm"
LEVEL = 60
ADDRW = "10.42.0.1"
ADDR4 = "8.8.8.8"

def check_4g_signal():
    #mobile device info
    list=[]
    ret = os.popen("%s" % CMDM).read()
    if ret != "":
        list = ret.split()
        mobile_device=list[0]
        mobile_type=list[1]
        mobile_state=list[2]
        mobile_conn=list[3]
        return list
    return list
    
    
def check_wifi_signal():
    #rescan
    logging.info("scan wifi list, need some time")
    buffer = os.popen("iwlist %s scan" % IFACE)
    buffer = os.popen('nmcli dev wifi | grep %s' % SSID).read()
    ret = 0
    if buffer != "":
        strlist = buffer.split()
        if strlist[0] == '*':
            ret = int(strlist[6])
        else:
            ret = int(strlist[5])
        #for item in strlist:
        #    print item
        logging.info("wifi signal strength %d" % ret)
    return ret
def mode_switch(mode):
    #print("pass")
    global MODE
    if mode == "4g":
        #os.system("nmcli radio wifi off")
        if MODE != "4g":
            logging.info("switch to 4g")
            #os.system("ifconfig wlp2s0 down")
            #如果现在连接的是cti wifi
            if os.system("iwconfig | grep %s" % SSID) == 0:
                logging.info("disconnect %s first" % SSID)
                os.system("nmcli device dis %s" % IFACE)
            #check 4g state
            list = check_4g_signal()
            if len(list) != 0:
                if list[2] == "connected":
                    logging.info("4g is already connected")
                else:
                    ret = os.system("nmcli device con gsm")
                MODE = "4g"
            else:
                logging.warning("no 4g module")
        else:
            logging.info("4g is already connected")
            
    elif mode == "wifi":
        if MODE != "wifi":
            logging.info("switch to wifi")
            #make sure wifi is up
            os.system("ifconfig %s up" % IFACE)                        
            #确认是不是已经连接到cti WiFi            
            if os.system("iwconfig | grep %s" % SSID) == 0:
                logging.info("already connect to cti wifi")
                MODE = "wifi"
            #现在没连接，但是之前连接过
            elif os.path.isfile(PATH):
                logging.info("have connection before, will connect soon")
                ret = os.system("nmcli connection up %s" % SSID)
                if ret == 0:
                    logging.info("connect to cti wifi OK")
                    MODE = "wifi"
                    #连接vlc
                else:
                    logging.warning("connect to cti wifi ERROR")
            #第一次连接
            else:
                ret = os.system("nmcli device wifi connect %s password %s" % (SSID, PWD))
                if ret == 0:
                    logging.info("connect to cti wifi OK")
                    MODE = "wifi"
                    #连接vlc
                else:
                    logging.warning("connect to cti wifi ERROR")                        
        else:
            #print("already connect to cti wifi")
            logging.info("already connect to cti wifi")
      
def check_network():
    #wifi device info
    buf = os.popen("nmcli device").read()
    logging.info(buf)
    buf = os.popen("route -n").read()
    logging.info(buf)

def ping(proc):
    while True:
        for line in iter(proc.stdout.readline, b''):
            logging.info('%s' % line)
def main():
    #log prepare
    logging.basicConfig(filename=datetime.now().strftime('%Y-%m-%d-%I:%M:%S.log'),\
                        format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)
    log = logging.getLogger()
    stdout_handler = logging.StreamHandler(sys.stdout)
    log.addHandler(stdout_handler)                    
    #print("cti-elevator program began")
    logging.info("cti-elevator program began")
    procw = subprocess.Popen(['ping', ADDRW], stdout=subprocess.PIPE, stderr = subprocess.STDOUT)
    proc4 = subprocess.Popen(['ping', ADDR4], stdout=subprocess.PIPE, stderr = subprocess.STDOUT)

    thread.start_new_thread(ping, (procw,))
    thread.start_new_thread(ping, (proc4,))
    
    while True:
        #check current status
        check_network()
        #检查4g信号
        #signal = check_4g_signal()
        #检查wifi信号
        wifi_signal = check_wifi_signal() 
        if wifi_signal > LEVEL:
            #print("wifi signal is good")
            logging.info("wifi signal is good")
            mode_switch("wifi")
        elif wifi_signal < LEVEL and wifi_signal > 0:
            #print("wifi signal is bad")
            logging.warning("wifi signal is bad")
            mode_switch("4g")
        else:
            #print("no wifi signal")
            logging.warning("no wifi signal")
            mode_switch("4g")
        sleep(1)
if __name__ == '__main__':
    main()