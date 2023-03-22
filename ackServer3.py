import socket
import json

## For Python 3

# Create a server socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = ('localhost', 10000)
sock.bind(server_address)

# Create the ack counter
ack = 0

while True:
    # receive packets from the sender
    data, address = sock.recvfrom(4096)
    
    # If some data is received proceed to process it
    if data:
        # Decode the data
        data = data.decode()
        data = json.loads(data)

        # Print the received data and sequence number
        print(f"Received Data: {data['data']}")
        print(f"Received Sequence Number: {data['seq']}")

        # Check if the sequence number is the expected one
        if data['seq'] == ack + 1:
            ack = data['seq']
            print("Sending ACK: " + str(ack) + "\n")

        # If the sequence number is less than the expected one, reset the ack
        elif data['seq'] == 0:
            ack = 0
            print("Initializing ACK...\n")

        # If the sequence number is not the expected one, send the last ack
        else:
            print("Unexpected Sequence Number")
            print("Sending ACK: " + str(ack) + "\n")
        
        # Send the ack to the client
        sock.sendto(str(ack).encode(), address)
