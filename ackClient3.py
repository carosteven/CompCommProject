import socket
import time
import random
import json

UDP_IP = "127.0.0.1"  # localhost
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # create UDP socket

def pickPacketsToLose():
    numbers = list(range(0, 10))
    num1, num2 = random.sample(numbers, 2)
    while num1 == num2:
        num1, num2 = random.sample(numbers, 2)
    return sorted([num1, num2])

def sendPacket(message):
    sock.sendto(json.dumps(message).encode(), (UDP_IP, UDP_PORT))
    print(f"Sent packet {i}")

    # listen for ack
    data, addr = sock.recvfrom(1024)
    data = data.decode()
    data = json.loads(data)
    return data


packetsToLose = pickPacketsToLose()

# main loop
lastAck = -1
for i in range(0, 10):
    message = {"seq": i, "data": f"This is message {i}"}

    if i in packetsToLose:
        print(f"Packet {i} lost (not sent)")

    else:
        # send packet
        response = sendPacket(message)

        # check if ack is correct
        lastAck = int(response['ack'])
        print(f"Received ack {response['ack']}")

print("\n")

# resend lost packets
for i in range(lastAck+1, 10):
    message = {"seq": i, "data": f"This is message {i}"}
    response = sendPacket(message)
    # check if ack is correct
    if int(response['ack']) == lastAck + 1:
        lastAck += 1
    print(f"Received ack {response['ack']}")

if lastAck == 9:
    print("All packets received")