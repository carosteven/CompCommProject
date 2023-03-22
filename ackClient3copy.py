import random
import socket
import json
import time

## For Python 3

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('localhost', 10000)

# Define list of messages to send
start_message = {'seq': 0, 'data': 'Start'}

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

# Define window size of sender
window_size = 5

# Define function to send messages with intentional 20%  packet loss
def send_message(message):
    message = json.dumps(message)

    # Send data to server
    sock.sendto(message.encode(), server_address)

    # Receive response
    server_ack, server = sock.recvfrom(4096)	
    #print('Received from server: ' + server_ack.decode())

    return server_ack

# Define function to randomly lose 20% of packets
def packets_to_lose(start, end):
    numbers = range(start, end)
    packets_lost = round((end-start)*0.2)

    omit = random.sample(numbers, packets_lost)
    print(f"Packets lost: {omit} ({100*packets_lost/(end-start)}%)")
        
    return sorted(omit)

# Run the client
try:
    # Initialize ack and start index
    server_ack = 0
    start_index = 0
    stop_index = window_size

    # Synchronize sender and receiver
    sock.sendto(json.dumps(start_message).encode(), server_address)

    # Implement Go-Back-N
    while True:
        # Send data, intentionally lose 20% of packets
        omit = packets_to_lose(start_index, stop_index)

        for i in range(start_index, stop_index):
            if i not in omit:
                # Send message if not omitted
                server_ack = int(send_message(messages[i]))

                # Check if ACK is correct, increment start index if so
                if server_ack == messages[i]['seq']:
                    start_index += 1

        # Increment stop index if all packets in window were received
        if start_index == len(messages):
            print(f"Expected ACK: {stop_index}")
            print(f"Received ACK: {server_ack}")
            print("All packets received!")
            break
        elif start_index == stop_index:
            print(f"Expected ACK: {stop_index}")
            print(f"Received ACK: {server_ack}")
            print("Advancing window...\n")
            stop_index += window_size
        else:
            print(f"Expected ACK: {stop_index}")
            print(f"Received ACK: {server_ack}")
            print("Retransmitting from last ACK...\n")
            print("")

        time.sleep(1)

finally:
    # If all packets were received, close the socket
    print('\nClosing socket')
    
sock.close()
