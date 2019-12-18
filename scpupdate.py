# -*- coding: utf-8 -*-

#Author: matt ji
#purpose: scp批量更新文件
#date: 2019/11/28
#usage: python scpupdate.py 16987 ...
import os, sys

#sshpass -p ctibr01 scp -P 16101  cti@frp.ctirobot.com:tikong/2019-04-04-11:07:07.log .
#sshpass -p ctibr01 ssh -p 16101  cti@frp.ctirobot.com
#sshpass -p tikong-mb scp -P 16990 

def main():
    if (len(sys.argv) < 2):
        print "usage: python scpupdate.py 16987 ..."
        exit(1)
    for index in range(len(sys.argv)-1):
    	cmd = "sshpass -p tikong-mb scp -P " + sys.argv[index+1] +" dongxi tikong@frp.ctirobot.com:"
        print cmd
        os.system(cmd)
    
if __name__ == '__main__':
    main()