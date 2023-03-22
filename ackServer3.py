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
    
    if data:
        data = data.decode()
        data = json.loads(data)

        print(f"Received Data: {data['data']}")
        print(f"Received Sequence Number: {data['seq']}")

        if data['seq'] == ack + 1:
            ack = data['seq']
            print("Sending ACK: " + str(ack) + "\n")

        elif data['seq'] < ack + 1:
            ack = data['seq']
            print("Sending ACK: " + str(ack) + "\n")

        else:
            print("Unexpected Sequence Number")
            print("Sending ACK: " + str(ack) + "\n")
        
        sock.sendto(str(ack).encode(), address)
