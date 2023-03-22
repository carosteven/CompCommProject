import socket
import sys, json

## For Python 3

# Create a server socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = ('localhost', 10000)
sock.bind(server_address)

# Create the byte counter
ack = 0

while True:
    # receive packets from the sender
    data, address = sock.recvfrom(4096)

    print(str(data.decode()))
    
    if data:
        data = data.decode()
        data = json.loads(data)
        if data['seq'] == ack + 1:
            ack = data['seq']
        elif data['seq'] < ack + 1:
            ack = data['seq']
        
        sock.sendto(str(ack).encode(), address)
        