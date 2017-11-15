# Copyright (c) 2017 Sascha Strand
# Available open source through the MIT License

# Notes from: http://www.geeksforgeeks.org/socket-programming-python/

import socket

s = socket.socket()
port = 12356

# No address specified so any device could connect
s.bind(('', port))

# max of five clients at a time
s.listen(5)
print("Socket listening at port {}.".format(port))

# The server sends and receives messages on a new socket for each connection
while True:
    c, addr = s.accept()
    print("\tGot connection from {}".format(addr))
    c.send(b'\tHello from the server.')
    print(c.recv(1024).decode('utf-8'))
    c.close()
