import socket
import sys
## For Python 2

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('localhost', 10000)
message = '0'
#'This is the message.  It will be repeated.'
try:
	
    # Send data
		print >>sys.stderr, 'sending "%s"' % message
		sent = sock.sendto(message, server_address)

    # Receive response
		print >>sys.stderr, 'waiting to receive'
		data, server = sock.recvfrom(4096)
		
		print >>sys.stderr, 'I have to send "%s"' % data
		while str(data) != '9':
		
			message = data
			
			sent = sock.sendto(message, server_address)
		    
			data, server = sock.recvfrom(4096)
		
			print >>sys.stderr, 'I have to send "%s"' % data
		
			

finally:
    print >>sys.stderr, 'closing socket'
raw_input()
sock.close()
