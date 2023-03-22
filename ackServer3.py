import socket
import json

UDP_IP = "127.0.0.1"  # localhost
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # create UDP socket
sock.bind((UDP_IP, UDP_PORT))  # bind socket to IP address and port

lastCorrectPacket = -1

while True:
    data, addr = sock.recvfrom(1024)  # receive data (up to 1024 bytes)
    data = data.decode()
    data = json.loads(data)
    print("Received:", data['data'])  # print the received message

    # send ack back to sender
    if data['seq'] == lastCorrectPacket + 1:
        lastCorrectPacket += 1

    ack = {"ack": lastCorrectPacket}
    sock.sendto(json.dumps(ack).encode(), addr)
    print("Sent ack", ack['ack'])

    if lastCorrectPacket == 9:
        print("All packets received")
        break
