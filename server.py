# Copyright (c) 2017 Sascha Strand
# Available open source through the MIT License

import socket
import select
from msg_processing import process_message, broadcast

WELCOME_PORT = 8080
MAX_MSG_SIZE = 4096 #bytes 

#-----------------------------------------------#
#                Set up server                  #
#-----------------------------------------------#

all_sockets = []
all_channels = []

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
				msg_json = active_socket.recv(MAX_MSG_SIZE).decode()
				process_message(msg_json, all_sockets, [s, active_socket])
				
			except Exception as e:
				# broadcast("User {} has left the channel\n".format(addr), all_sockets, [s, active_socket])
				print("exception: {}".format(e))

s.close()
