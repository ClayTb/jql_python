import socket
import sys
import os

server_address = './uds_socket'

# Make sure the socket does not already exist
try:
#这里先去删除这个文件
    os.unlink(server_address)
except OSError:
    if os.path.exists(server_address):
        raise

# Create a UDS socket
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

# Bind the socket to the port
print >>sys.stderr, 'starting up on %s' % server_address
sock.bind(server_address)

# Listen for incoming connections
# 这里是同一时间只能有一个连接
sock.listen(1)

while True:
    # Wait for a connection
    print >>sys.stderr, 'waiting for a connection'
# 这里去接收连接
    connection, client_address = sock.accept()
    try:
        print >>sys.stderr, 'connection from', client_address

        # Receive the data in small chunks and retransmit it
        while True:
		#这里收数据，看能不能改成每次收一行 
		#这里依然面临粘包的问题，这里可以使用split来分包，详细见有道笔记
		#但是导航模块也会有这样的问题，也挺难解决的。
		#这里默认是阻塞读，没有问题，反正在另一个线程里
            data = connection.recv(16)
            print >>sys.stderr, 'received "%s"' % data
            if data:
                print >>sys.stderr, 'sending data back to the client'
                #connection.sendall(data)
            else:
                print >>sys.stderr, 'no more data from', client_address
                break

    finally:
        # Clean up the connection
		#这里去关闭连接
        print >>sys.stderr, 'close the socket'
        connection.close()

state = ['forward','back','left','right','stop']
av_dict = {'voicenum':0, 'imageNum':0}
mode = ['uwb','app','navi']
#四个模块，总共6组数据
#控制板需要返回什么值吗？跟随模式下控制板需要发送数据给rpi吗？比如线速度 角速度 行走速度，
#rpi需要发送数据给控制板吗？
#超声波距离 uwb数据 imu
crfd = {'mode':mode[0], 'usd':0, 'uwb':{}, 'imu':{}}
#rpi发给ctl的就是mode 线速度 角速度 
#mode 分为 跟随模式uwb 编程模式app 导航模式navi
rcfd = {'mode':mode[0], 'lv':'0', 'av':'0'}
#rpi发给app帧， 此时状态 以及 网络状况
rafd = {'mode':mode[0],  \
'net':[{'name':'wifi','ssid':'', 'pw':'', 'status':'down', 'ip':''}, {'name':'AP','status':'', 'ip':''}]}
#arfd app发给rpi
arfd = {'mode':mode[0], 'lv':0, 'av':0, 'img':0, 'voc':0, 'cmd':''}
#rnfd rpi发送给navi的数据
rnfd = {'mode':mode[0],'usd':0, 'uwb':{}, 'imu':{}}
#nrfd navi发送给rpi的数据
nrfd = {'lv':0, 'av':0}

#这里是树莓派和运动控制的通信
#先从运动控制处通过串口得到数据，这个类似于蓝牙通信里去读串口数据一样。也是readline
#拿到数据之后要转发给导航
#z这里也要找一下运动控制的板子，发送AT，返回CONTROL。因为有很多个usb转串口ttyUSB，
for vnode in os.listdir("/dev/"):
    if vnode.startswith("ttyUSB"):
        print "test "+vnode
	#这里要修改一下，是要返回CONTROL而不是OK。蓝牙是返回OK
        ser = fm(vnode)
        if ser:
            break
	return ser_ctl
if (ser == None):
    print "not found control module"
    exit(1)
	
def control_to_rpi():
    while True:
	    try:
        buffer = ser.readline()
        #print "buffer " + buffer
        #buffer = ser.read(100)
        if buffer:
            #print buffer
            fdict = json.loads(buffer)
            #ser.write(buffer)
            #ser.write(buff_test)
            #print fdict
            #len = len(fdict)
            print fdict['lv'], fdict['av'], fdict['voc'], fdict['img'],  \
                    fdict['cmd'], fdict['mode']
			#这里需要注意的是会有一个APP控制到uwb跟随模式的切换
			#手环会发送一个指令到node，node会发送给控制板，控制板也要发送给rpi。
            pcf()         
            buffer = ''
        else:
            print "No data"
    except json.JSONDecodeError:
        print "Error: try to parse an incomplete message"
        time.sleep(0.001)
    
#这里需要设置一个timer，定时去发送帧到控制，导航，app
#如果这是uwb跟随模式，如果app有连接，那就发送数据给app，如果没有连接，就不发送
#如何判断有无连接，即使没有连接发送，再次连接上，也不会有问题。
#接口命名规则，比如app_ble，意思是app接口，这个接口是蓝牙通信，可能下次是app_ap，这就是AP模式下接口，
#app_wifi：和app是wifi通信
def rpi_to_control:
    cnt = 0
    while True:
	#1. 发送数据给app
	#这里计数，是100ms发送一次 导航和nav是10ms一次
	if cnt == 10
	    cnt = 0
	data = json.dumps(rafd)
	app_ble.write(data)
	#2. 发送数据给导航
	data = json.dumps(rnfd)
	#这里通过socket送出
	cnt = nav_skt.sendall(data)
	#3. 发送数据给控制板 也就是 线速度 角速度
	data = json.dumps(rcfd)
	cnt = ctl_ser.write(data)
	#每隔100ms发送一次
		time.sleep(100)
#pcf: parse control frame
#cafd: control to app frame dict,这是控制板发送过来数据 
#rcfd: raspberry pi to control frame dict: rpi发送给控制板的
#rafd：树莓派发送给app的帧
#arfd：app to rpi frame dict: app发送给树莓派的数据转换成dict格式了 
#rnfd: rpi to navigate module frame dict
def pcf():
	for key in cafd.keys():
		for case in switch(key):
			if case('mode'):
			    if cfd['mode'] = 'uwb':
				    rafd['mode'] = 'uwb'
					#control_dict['mode'] = fdict['mdoe']
				break
			if case('usdis'):
				rafd['usdis'] = cfd['usdis']
				break
			if case('uwb'):
				rnfd['uwb'] = cfd['uwb']
				break
			if case():
				print "some new key, should not happen"
				logging.warning('pcf some new key %s', key)

'''				
开机
1. 打开蓝牙串口 打开控制板串口 发送AT，分别返回OK CONTROL
2. 和app通信，返回目前的状态 rafd，开机默认应该是跟随模式uwb
3. app发送wifi设置，rpi接收到，设置完之后，rpi会把信息传送回去
4. app切换到遥控模式，会传输lv av，这时 rpi就会发送对应数据给ctl，
5. ctl 一开机默认是跟随模式，也会不断发送数据给rpi，但是这时候传上来的传感器数据 rpi不会传给 navi，
因为这时候是uwb模式。
6. 到编程模式的时候， ctl还是传输 同样的传感器数据上来
'''

