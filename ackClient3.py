import socket
import sys
import json

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

try:
    server_ack = 0

    # Send data, intentionally lose 6th and 9th packets
    for message in messages:
        message = json.dumps(message)
        sock.sendto(message.encode(), server_address)

        # Receive response
        server_ack, server = sock.recvfrom(4096)	

        print('Received: ' + str(server_ack.decode()))
		
finally:
    sys.stderr.write('\nclosing socket')
    
sock.close()
