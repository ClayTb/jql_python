# -*- coding: utf-8 -*-
#author: matt ji
#date: 20190409
#purpose: 主要用来测试呼梯
#云端发送呼梯指令，梯控发送ack，云端计时，再除以二，就得到时间
#严格来讲，需要梯控将命令发给单片机，单片机回复ack，梯控再回复ack，云端这时候计时为止
#需要使用python mqtt，可以直接用命令mosquitto_pub发送 用mosquitto_sub接收
#推送topic："/cti/ele-cmd"  订阅topic "/cti/elevator-l"
#这个版本是正式在机器人上跑的，另外一个local版本是跑在梯控里的
#需要连接梯控ip 192.168.1.150

import threading
from time import sleep
import os
import subprocess
import datetime, json
import select

SUB = "mosquitto_sub -t /cti/elevator-l"
exitFlag = 0

def parse(msg):
    #print datetime.datetime.now()
    #print msg
    pkt = json.loads(msg)
    
    
    
    
def mqtt_sub():
    global exitFlag
    start = 0
    end = 0
    msg = ""

    proc = subprocess.Popen(['mosquitto_sub', '-h', '192.168.1.150','-t', '/cti/elevator-l'], stdout=subprocess.PIPE, stderr = subprocess.STDOUT)
    poll_obj = select.poll()
    poll_obj.register(proc.stdout, select.POLLIN)
    while True:
        poll_result = poll_obj.poll(0)
        if poll_result:
            output = proc.stdout.readline()
            #if output == '' and proc.poll() is not None:
            #    break;
            if output:
                #print "recv msg"
                #print output.strip()
                if(output.startswith("{")):
                    start = 1
                if(output.startswith("}")):
                    end = 1
                    start = 0
                if(start == 1):
                    msg += output            
                if(end == 1):
                    msg += output
                    end = 0
                    parse(msg)
                    msg = ""
        if exitFlag:
            print("thread exit")
            proc.kill()
            exit(0)
        #sleep(0.01)
    #for line in iter(proc.stdout.readline, b''):
    #    print line
    

def callele(floor):
    print datetime.datetime.now()
    value = '{"ID":"07551", "cmd":"call", "floor":"' + str(floor) + '"}'
    print "send call msg"
    proc = subprocess.Popen(['mosquitto_pub', '-h', '192.168.1.150','-t', '/cti/ele-cmd', '-m', value], stdout=subprocess.PIPE, stderr = subprocess.STDOUT)

def close():
    print datetime.datetime.now()
    value = '{"ID":"07551", "cmd":"close", "duration":"1"}'
    print "send close msg"
    proc = subprocess.Popen(['mosquitto_pub', '-h', '192.168.1.150','-t', '/cti/ele-cmd', '-m', value], stdout=subprocess.PIPE, stderr = subprocess.STDOUT)

def open():
    value = '{"ID":"07551", "cmd":"open", "duration":"30"}'
    print "send open msg"
    proc = subprocess.Popen(['mosquitto_pub', '-h', '192.168.1.150','-t', '/cti/ele-cmd', '-m', value], stdout=subprocess.PIPE, stderr = subprocess.STDOUT)

def cancelopen():
    value = '{"ID":"07551", "cmd":"cancelopen", "duration":"30"}'
    print "send cancel open msg"
    proc = subprocess.Popen(['mosquitto_pub', '-h', '192.168.1.150','-t', '/cti/ele-cmd', '-m', value], stdout=subprocess.PIPE, stderr = subprocess.STDOUT)

def cancelclose():
    print datetime.datetime.now()
    value = '{"ID":"07551", "cmd":"cancelclose", "duration":"1"}'
    print "send cancel close msg"
    proc = subprocess.Popen(['mosquitto_pub', '-h', '192.168.1.150','-t', '/cti/ele-cmd', '-m', value], stdout=subprocess.PIPE, stderr = subprocess.STDOUT)
 
def main():
    global exitFlag
    t = threading.Thread(name = 'mqttSub', target = mqtt_sub)
    t.start()
    
    print "usage: 1. 呼梯 2. 开门 3. 关门 4. 取消开门 5.取消关门 q: 退出"
    while True:
        char = raw_input()
        if (char == "q"):
            print("exit")
            exitFlag = 1
            exit(0)
        elif (char == "3"):
            print("发送关门指令")
            close()

        elif (char.startswith('1')):
            print("发送呼梯指令")
            x,floor = map(int, char.split())
            callele(floor)
        elif (char == "2"):
            print("开门")
            open()
        elif (char == "4"):
            print("取消开门")
            cancelopen()
        elif (char == "5"):
            print("取消关门")
            cancelclose()    
        else :
            print 'you input '+char + '\n'
            sleep(0.2)



if __name__ == '__main__':
    main()
