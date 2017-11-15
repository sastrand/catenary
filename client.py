import socket

s = socket.socket()
port = 12356

#host = socket.gethostname()

s.connect(('localhost', port))
print(s.recv(1024).decode('utf-8'))
s.send(b'\tHello from the client.')
s.close
