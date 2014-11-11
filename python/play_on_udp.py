#!/usr/bin/env python
import socket
import ip_tools

trans = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

broadcast = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
broadcast.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
broadcast.bind(('', 9001))

ips = socket.gethostbyname_ex(socket.gethostname())[2]
conn = ("0.0.0.0",0)
msg = ""

while True:
    msg, conn = broadcast.recvfrom(64)
    if msg == "sfx_scan":
        print "Recieved scan from "+str(conn)+", communicating via "+str(ip_tools.closest_ip(conn[0], ips))
        break
    
trans.connect(addr)
trans.send("acknowledged")

while msg != "close_connection":
    msg, addr = broadcast.recvfrom(64)
    if addr == conn:
        if msg == "sfx_play":
            print "playing"

print "Closing connection"
trans.close()
    
