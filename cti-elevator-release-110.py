# -*- coding: utf-8 -*-
#author: matt ji
#date: 2019/1/8
#purpose: check wifi 4g signal strength, and then switch between them
#         使用vlc来播放不同地址的视频，wifi就播放高清的，4g就播放低分辨率的
#rtsp://10.42.0.249:9554/webcam
#rtsp://112.74.184.237/webcamtest
'''
1. 测试环境 
    1.1 梯控使用rk3288模拟，本身使用4g与云端通信，发射ap供机器人进入电梯后连接
    1.2 机器人使用移动pc模拟，使用4g与云端通信，进入电梯后连接梯控wifi与梯控直接通信
2. 测试过程
    2.1 首先机器人在外面使用4g，可以和云端正常通信
    2.2 按下按钮，等待电梯
    2.3 进入电梯，自动连接梯控wifi，与梯控正常通信 PS：此时外网通信也正常，4g依然有连接
    2.4 离开电梯，断开梯控wifi，4g通信继续维持，与外网正常通信
3. 测试结果
    3.1 通信过程流畅
    3.2 从ping包的结果看有少量外网丢包和内网丢包，< 1%
    
'''
from time import sleep
import serial
import time, datetime
import os
import json, sys

MODE = "unknown"
SSID = "cti-elevator"
PATH = "/etc/NetworkManager/system-connections/cti-elevator"
PWD = "12345678"
IFACE = "wlp2s0"
CMDM = "nmcli device | grep gsm"
LEVEL = 60
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
    print("scan wifi list, need some time")
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
        print("wifi signal strength %d" % ret)
    return ret
def mode_switch(mode):
    #print("pass")
    global MODE
    if mode == "4g":
        #os.system("nmcli radio wifi off")
        if MODE != "4g":
            print("switch to 4g")
            #os.system("ifconfig wlp2s0 down")
            #如果现在连接的是cti wifi
            if os.system("iwconfig | grep %s" % SSID) == 0:
                print("disconnect %s first" % SSID)
                os.system("nmcli device dis %s" % IFACE)
            #check 4g state
            list = check_4g_signal()
            if len(list) != 0:
                if list[2] == "connected":
                    print("4g is already connected")
                else:
                    ret = os.system("nmcli device con cdma")
                MODE = "4g"
            else:
                print("no 4g module")
            
    elif mode == "wifi":
        if MODE != "wifi":
            print("switch to wifi")
            #make sure wifi is up
            os.system("ifconfig %s up" % IFACE)                        
            #确认是不是已经连接到cti WiFi            
            if os.system("iwconfig | grep %s" % SSID) == 0:
                print("already connect to cti wifi")
                MODE = "wifi"
            #现在没连接，但是之前连接过
            elif os.path.isfile(PATH):
                print("have connection before, will connect soon")
                ret = os.system("nmcli connection up %s" % SSID)
                if ret == 0:
                    print("connect to cti wifi OK")
                    MODE = "wifi"
                    #连接vlc
                else:
                    print("connect to cti wifi ERROR")
            #第一次连接
            else:
                ret = os.system("nmcli device wifi connect %s password %s" % (SSID, PWD))
                if ret == 0:
                    print("connect to cti wifi OK")
                    MODE = "wifi"
                    #连接vlc
                else:
                    print("connect to cti wifi ERROR")                        
        else:
            print("already connect to cti wifi")
      
def check_network():
    #wifi device info
    ret = os.system("nmcli device")
    ret = os.system("route -n")

def main():
    print("cti-elevator program began")
    while True:
        #check current status
        check_network()
        #检查4g信号
        #signal = check_4g_signal()
        #检查wifi信号
        wifi_signal = check_wifi_signal() 
        if wifi_signal > LEVEL:
            #print("wifi signal is good")
            mode_switch("wifi")
        elif wifi_signal < LEVEL and wifi_signal > 0:
            print("wifi signal is bad")
            mode_switch("4g")
        else:
            print("no wifi signal")
            mode_switch("4g")
        sleep(1)
if __name__ == '__main__':
    main()