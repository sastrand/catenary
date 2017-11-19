# Copyright (c) 2017 Sascha Strand
# Available open source through the MIT License

import socket
from select import select
# from msg_processing import process_message, broadcast, print_all_users
from msg_processing import *
from pandas import DataFrame

WELCOME_PORT = 8080
MAX_MSG_SIZE = 4096 #bytes 
DEFAULT_CHANNELS = {
	'main':[],
}
USER = {
	'ip_address':[],
	'username':[],
	'socket_obj':[],
}

#-----------------------------------------------#
#                Set up server                  #
#-----------------------------------------------#

all_sockets = []
all_channels = DataFrame(DEFAULT_CHANNELS)
all_users = []

print(all_channels)

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
	active_sockets,_,_ = select(all_sockets, [], [])
	for active_socket in active_sockets:
		if active_socket == s:
			# New connection
			c, addr = s.accept()
			this_user = {
				'ip_address': addr,
				'username': "unknow",
				'socket_obj': c
			}
			all_users.append(this_user)
			all_sockets.append(c)
			print("\tGot connection from {}".format(addr))
		else:
			try:
				# Incoming message
				msg_json = active_socket.recv(MAX_MSG_SIZE).decode()
				process_message(msg_json, all_sockets, [s, active_socket])
				print_all_users(all_users)
				
			except Exception as e:
				broadcast("User {} has left the channel\n".format(addr), all_sockets, [s, active_socket])
				print("exception: {}".format(e))
				all_sockets.remove(active_socket)
				active_socket.close()


s.close()
