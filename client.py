import socket
import random
import string
import json

ID_LENGTH = 6

def id_generator():
	return ''.join(random.choice(string.ascii_letters + string.digits) for i in range(ID_LENGTH))

s = socket.socket()
port = 8080

client_id = id_generator()

msg = {}
msg['to'] = "server_initial"
msg['from'] = client_id
msg['body'] = "hello from client {}.".format(client_id)


host = socket.gethostname()

s.connect(('localhost', port))
print(s.recv(1024).decode('utf-8'))
s.send(json.dumps(msg).encode())
s.close
