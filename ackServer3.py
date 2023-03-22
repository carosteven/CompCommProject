import socket

UDP_IP = "127.0.0.1"  # localhost
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # create UDP socket
sock.bind((UDP_IP, UDP_PORT))  # bind socket to IP address and port

while True:
    data, addr = sock.recvfrom(1024)  # receive data (up to 1024 bytes)
    print("Received message:", data.decode())  # print the received message
