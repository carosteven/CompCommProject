'''
Computer Communications Project 
Server Code

Steven Caro 105205197
Mathew Dunne 105213664
Gian Favero 105215891
'''

import socket
import json

# Create a server socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = ('localhost', 10000)
sock.bind(server_address)

# Create the ack counter
ack = 0

verbose = False

if not verbose:
    print("ACKs sent: \n")

while True:
    # receive packets from the sender
    data, address = sock.recvfrom(4096)
    
    # If some data is received proceed to process it
    if data:
        # Decode the data
        data = data.decode()
        data = json.loads(data)

        # Print the received data and sequence number
        if verbose:
            print(f"Received Data: {data['data']}")
            print(f"Received Sequence Number: {data['seq']}")

        # Check if the sequence number is the expected one
        if data['seq'] == ack + 1:
            ack = data['seq']
            if verbose: print("Sending ACK: " + str(ack) + "\n")
            else:
                print(ack, end=' ')

        # If the sequence number is less than the expected one, reset the ack
        elif data['seq'] == 0:
            ack = 0
            if verbose: print("Initializing ACK...\n")

        # If the sequence number is not the expected one, send the last ack
        else:
            if verbose: 
                print("Unexpected Sequence Number")
                print("Sending ACK: " + str(ack) + "\n")
            else:
                print(ack, end=' ')
        
        # Send the ack to the client
        sock.sendto(str(ack).encode(), address)

        if ack == 15:
            break
