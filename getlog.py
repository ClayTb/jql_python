# -*- coding: utf-8 -*-
import os, sys

#sshpass -p ctibr01 scp -P 16101  cti@frp.ctirobot.com:tikong/2019-04-04-11:07:07.log .
#sshpass -p ctibr01 ssh -P 16101  cti@frp.ctirobot.com

def main():
    if (len(sys.argv) < 2):
        print "usage: getlog.py num log"
        exit(1)
    elif(len(sys.argv) == 3):
        if(sys.argv[1] == "1"):
            pw = "ctibr01"
            port = "16101"
        elif(sys.argv[1] == "2"):
            pw = "ctibr02"
            port = "16102"
        elif(sys.argv[1] == "3"):
            pw = "ctibr03"
            port = "16103"
        path = "cti@frp.ctirobot.com:tikong/" + sys.argv[2]
        cmd = "sshpass -p "+pw+" scp -P " + port + " "+ path+ " /mnt/hgfs/F/louyu/log/"
        print cmd
        os.system(cmd)
    elif(len(sys.argv) == 2):
        if(sys.argv[1] == "1"):
            pw = "ctibr01"
            port = "16101"
        elif(sys.argv[1] == "2"):
            pw = "ctibr02"
            port = "16102"
        elif(sys.argv[1] == "3"):
            pw = "ctibr03"
            port = "16103"
        cmd = "sshpass -p " + pw +" ssh -p " + port + " cti@frp.ctirobot.com"
        print cmd
        os.system(cmd)
    
if __name__ == '__main__':
    main()
