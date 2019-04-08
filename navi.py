# -*- coding: utf-8 -*-

import threading
from time import sleep
import os

string = 'rostopic pub -1 /robot_state cti_msgs/BuildingRobotState "state: 0 \ntarget_floor: 0 \ncurrent_floor: 0 \ndestination:\n  position: {x: 0.0, y: 0.0, z: 0.0}\n  orientation: {x: 0.0, y: 0.0, z: 0.0, w: 0.0}"'
string2 = 'rostopic pub -1 /elevator_cmd cti_msgs/ElevatorCmd "cmd: 1 \nelevator_id: \'0000100610006\' \ntarget_floor: 0 \ncurrent_floor: 0"'
string1 = 'rostopic pub -1 /elevator_cmd cti_msgs/ElevatorCmd "cmd: 0 \nelevator_id: \'0000100610006\' \ntarget_floor: %d \ncurrent_floor: %d"'
string3 =  'rostopic pub -1 /elevator_cmd cti_msgs/ElevatorCmd "cmd: 2 \nelevator_id: \'0000100610006\' \ntarget_floor: 0 \ncurrent_floor: 0"'          

exitFlag = 0
def robot_state():
    while True:
        #if (exitFlag == 1):
        #print exitFlag
        if exitFlag:
            print("thread exit")
            exit(0)
        print "send heart msg"
        os.system(string)
        sleep(1)
  
def closedoor():
    print("close door")
    os.system(string2)

def huti(f, t):
    print("call elevator")
    os.system(string1 % (t,f))  

def missionCancel():
    print("mission cancel")
    os.system(string3)

def main():
    t = threading.Thread(name = 'robotstate', target = robot_state)
    t.start()

    global exitFlag    
    print "usage: 1. 呼梯(1 1 3) 2. 关门 3. 取消任务 q: 退出"
    while True:
        char = raw_input()
        if (char == "q"):
            print("exit")
            exitFlag = 1
            exit(0)
        elif (char == "2"):
            print("发送关门指令")
            closedoor()
        elif (char.startswith('1')):
            print("发送呼梯指令")
            x,y,z = map(int, char.split())
            huti(y,z)
        elif (char == "3"):
            print("取消任务")
            missionCancel()
        else :
            print 'you input '+char + '\n'
            sleep(0.2)

if __name__ == '__main__':
    main()



