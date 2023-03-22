TODO:

- Client and server running on local host
- Client sends 10 packets with sequence number and data to server
- Server acknowledges each received packet
- Client intentionally loses/holds 2 segments (loss rate of 0.2)
- Go Back N protocol is used to successfully deliver all 10 packets