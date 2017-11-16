# Copyright (c) 2017 Sascha Strand
# Available open source through the MIT License

import socket
import json

s = socket.socket()
port = 8080

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
    msg = json.loads(c.recv(4096).decode())
    print("\t" + msg['body'])
    c.close()
