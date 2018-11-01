import socket
import sys
import json

#ctl_dict = {'mode':'navi', 'state':'run', 'linearVelocity':0, 'angular':0, 'ultrasonic':0} 
ctl_dict = {"Vx": 10, "Vz": 20}
# Create a UDS socket
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = '/home/rpdzkj/code/cti-tr/message'
print >>sys.stderr, 'connecting to %s' % server_address
try:
    sock.connect(server_address)
except socket.error, msg:
    print >>sys.stderr, msg
    sys.exit(1)

try:
    
    # Send data
    message = json.dumps(ctl_dict)
    print >>sys.stderr, 'sending "%s"' % message
    sock.sendall(message+'\n')

    amount_received = 0
    amount_expected = len(message)
    
    while True:
#    while amount_received < amount_expected:
        data = sock.recv(1000)
        if data:
            amount_received += len(data)
            print >>sys.stderr, 'received "%s"' % data
        else:
            print >>sys.stderr, 'no more data'
            break

finally:
    print >>sys.stderr, 'closing socket'
    sock.close()
