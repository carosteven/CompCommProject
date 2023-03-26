'''
Computer Communications Project 
Client Code

Steven Caro 105205197
Mathew Dunne 105213664
Gian Favero 105215891
'''

import random
import socket
import json
import time

## For Python 3

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('localhost', 10000)

# Define list of messages to send
messages = [
    {'seq': 0, 'data': 'Start'},
    {'seq': 1, 'data': 'Hello, World!'},
    {'seq': 2, 'data': 'This is the second message'},
    {'seq': 3, 'data': 'This is the third message'},
    {'seq': 4, 'data': 'This is the fourth message'},
    {'seq': 5, 'data': 'This is the fifth message'},
    {'seq': 6, 'data': 'This is the sixth message'},
    {'seq': 7, 'data': 'This is the seventh message'},
    {'seq': 8, 'data': 'This is the eighth message'},
    {'seq': 9, 'data': 'This is the ninth message'},
    {'seq': 10, 'data': 'This is the tenth message'},
    {'seq': 11, 'data': 'This is the eleventh message'},
    {'seq': 12, 'data': 'This is the twelfth message'},
    {'seq': 13, 'data': 'This is the thirteenth message'},
    {'seq': 14, 'data': 'This is the fourteenth message'},
    {'seq': 15, 'data': 'This is the fifteenth message'}    
]

# Define function to send messages
def send_message(message):
    message = json.dumps(message)

    # Send data to server
    sock.sendto(message.encode(), server_address)

    # Receive response
    server_ack, server = sock.recvfrom(4096)	

    return server_ack

# Define function to randomly lose 20% of packets
def packets_to_lose(start, end):
    numbers = range(start, end)
    packets_lost = round((end-start)*0.2)
    
    if packets_lost/(len(messages)) < 0.2:
        packets_lost += 1

    omit = random.sample(numbers, packets_lost)
        
    return omit, packets_lost

# Run the client
try:
    # Define window size of sender
    window_size = 15

    # Initialize ack and start index
    server_ack = 0
    start_index = 1
    current_index = 1
    stop_index = window_size

    # Create timeout buffer and threshold
    timers = []
    timeout = 0.5

    # Comment style 
    verbose = True

    # Synchronize sender and receiver
    if verbose: print(f"Sending Data: {messages[0]['data']}")
    if verbose: print(f"Sending Sequence Number: {messages[0]['seq']}")
    sock.sendto(json.dumps(messages[0]).encode(), server_address)
    server_ack, server = sock.recvfrom(4096)
    if verbose: print(f"Received ACK: {int(server_ack)}\n")

    # Find index of lost packets
    omit, packets_lost = packets_to_lose(start_index, len(messages))
    print(f"Packet(s) {omit} lost. Loss rate: ({100*packets_lost/(len(messages))}%)\n")

    print("Starting transmission:\n")

    # Implement Go-Back-N
    while start_index <= len(messages) - 1:
        if current_index not in omit:
            if verbose: print(f"Sending Data: {messages[current_index]['data']}")
            if verbose: print(f"Sending Sequence Number: {messages[current_index]['seq']}")
            server_ack = int(send_message(messages[current_index]))
            if verbose: print(f"Received ACK: {server_ack}\n") 
            else:
                print(current_index, end=' ')
        else:
            omit.remove(current_index)
        
        timers.append(time.time())

        # Check if ACK is correct, increment indexes if so
        if server_ack == start_index:
            start_index += 1
            stop_index = min(stop_index + 1, len(messages)-1)
            timers.pop(0)

        # Increment current index
        current_index += 1
        
        # Check if all packets have been sent before timeout
        if start_index > stop_index:
            break
        elif current_index > stop_index:
            while True:
                if time.time() - timers[0] > timeout:
                    if verbose: 
                        print("Reached end of Window: Timeout")
                        print(f"Expected ACK: {stop_index}")
                        print(f"Received ACK: {server_ack}")
                        print("Retransmitting from last ACK...\n")
                    current_index = start_index
                    timers = []
                    break

        time.sleep(0.5)

    if verbose: print("All packets received!")

finally:
    # If all packets were received, close the socket
    if verbose: print('\nClosing socket')
    
sock.close()