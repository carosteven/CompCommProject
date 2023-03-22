import random
import socket
import sys
import json
import time

## For Python 3

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('localhost', 10000)
messages = [
    {'seq': 1, 'data': 'Hello, World!'},
    {'seq': 2, 'data': 'This is the second message'},
    {'seq': 3, 'data': 'This is the third message'},
    {'seq': 4, 'data': 'This is the fourth message'},
    {'seq': 5, 'data': 'This is the fifth message'},
    {'seq': 6, 'data': 'This is the sixth message'},
    {'seq': 7, 'data': 'This is the seventh message'},
    {'seq': 8, 'data': 'This is the eighth message'},
    {'seq': 9, 'data': 'This is the ninth message'},
    {'seq': 10, 'data': 'This is the tenth message'}    
]

def send_message(start, end):
    if end > len(messages):
        end = len(messages)

    omit = packets_to_lose(start, end)   

    for message in messages[start:end]:
        if message['seq'] not in omit:
            # Get message from dictionary
            message = json.dumps(message)

            # Send data to server
            sock.sendto(message.encode(), server_address)
            print(message)

            # Receive response
            server_ack, server = sock.recvfrom(4096)	
            print('Received: ' + server_ack.decode())

    return server_ack

def packets_to_lose(start, end):
    numbers = range(start, end)
    packets_lost = round((end-start)*0.2)
    omit = random.sample(numbers, packets_lost)
        
    return sorted(omit)

try:
    server_ack = 0
    start_index = 0
    window_size = 10

    # Implement Go-Back-N
    while True:
    # Send data, intentionally lose packets
        server_ack = int(send_message(start_index, window_size))

        if server_ack != (min(start_index + window_size, len(messages))):
            print('Error: missing packets')
            print(f"Expected: {min(start_index + window_size, len(messages))}")
            print(f"Received: {server_ack}")
            print(f"Going back to last received packet: {server_ack}")

            # Go back to last received packet
            start_index = server_ack
        else:
            break

finally:
    sys.stderr.write('\nclosing socket')
    
sock.close()
