import socket
import sys

## For Python 3

# Create a server socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = ('localhost', 10000)
sys.stderr.write('starting up on %s port %s' % server_address)
sock.bind(server_address)

while True:
    # receive packets from the sender
    sys.stderr.write('\nwaiting to receive message')
    data, address = sock.recvfrom(4096)

    sys.stderr.write('received %s bytes from %s' % (len(data), address))
    sys.stderr.write(str(data))
    
    m = ord(data) + 1
    
    print("\ndata, m = ",data,m)
    
    if data:
        sent = sock.sendto(bytes(m), address)
        print("chr(m) = ",chr(m))
        sys.stderr.write('sent %s bytes back to %s' % (sent, address))
