# Copyright (c) 2017 Sascha Strand
# Available open source through the MIT License

import socket
import json
import select

WELCOME_PORT = 8080
MAX_MSG_SIZE = 4096 #bytes 

def broadcast (body, recipients, ommitted):
	for socket in recipients:
		if socket not in ommitted:
			try:
				socket.send(body.encode())
			except Exception as e:
				socket.close()
				recipients.remove(socket)
				print("A client has been disconnected due to an error: {}".format(e))

#-----------------------------------------------#
#                Set up server                  #
#-----------------------------------------------#

all_sockets = []

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# No address specified so device with an IP address can connect
s.bind(('', WELCOME_PORT))

# max of five clients at a time
s.listen(5)
print("Server listening at port {}.".format(WELCOME_PORT))

all_sockets.append(s)

#-----------------------------------------------#
#                  Run server                   #
#-----------------------------------------------#

while True:
	active_sockets,_,_ = select.select(all_sockets, [], [])
	for active_socket in active_sockets:
		if active_socket == s:
			# New connection
			c, addr = s.accept()
			all_sockets.append(c)
			print("\tGot connection from {}".format(addr))
		else:
			try:
				# Incoming message
				msg = json.loads(active_socket.recv(MAX_MSG_SIZE).decode())
				body = "\r[" + msg['from'] + "] " + msg['body']
				broadcast(body, all_sockets, [s, active_socket])
			except Exception as e:
				# broadcast("User {} has left the channel\n".format(addr), all_sockets, [s, active_socket])
				print("exception: {}".format(e))

s.close()
