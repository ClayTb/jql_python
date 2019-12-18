1. uds*是unix domain socket的测试程序
2. serial-read/write是读写串口例子
3. 4g.py 
  #自动发送脚本给4g模块
  #检测信号质量
4. navi.py是模拟机器人发命令给梯控， rostopic  
5. getlog.py是ssh进去看完文件名，然后scp把文件拉出来  
6. rx-tx.py 一个线程专门收数据，另外可以捕获键盘输入，q两个线程都退出  
7. subprocess-test: 是两个线程，一个线程使用subprocess来监听mosquitto的topic，并且使用select poll来实现非阻塞读  
8. tx-file.py:  一边通过串口接收数据，一边通过串口发送文件  
scpupdate: 批量上传文件scp  
