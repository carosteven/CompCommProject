import socket
import sys
import pickle

## For Python 3

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('localhost', 10000)
message = '0'
try:
    # Send data
	sys.stderr.write('sending "%s"' % message)
	sock.sendto(message.encode(), server_address)

    # Receive response
	sys.stderr.write('\nwaiting to receive ack')
	data, server = sock.recvfrom(4096)
	
	sys.stderr.write('I have to send "%s"' % data)
	while str(data) != '9':
		message = data
		sent = sock.sendto(bytes(message), server_address)
		data, server = sock.recvfrom(4096)
		sys.stderr.write('I have to send "%s"' % data)
		
finally:
    sys.stderr.write('\nclosing socket')
    
sock.close()
