# Copyright (c) 2017 Sascha Strand
# Available open source through the MIT License

import socket
from select import select
from msg_processing import *

WELCOME_PORT = 8080
MAX_MSG_SIZE = 4096 #bytes 
DEFAULT_CHANNELS = {
	# 'main':['poobear'],
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
all_channels = DEFAULT_CHANNELS
all_users = []

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
				'username': "unknown",
				'socket_obj': c
			}
			all_users.append(this_user)
			all_sockets.append(c)
			print("\tGot connection from {}".format(addr))
		else:
			try:
				# Incoming message
				msg = loads(active_socket.recv(MAX_MSG_SIZE).decode())
				# if msg['to'] == 'JOINWORKSPACE':
				# 	if msg[]


				if msg['to'] == "JOINCHANNEL":
					# print("<><> Active Socket info: {}".format(active_socket))
					# if all_users[]
					if msg['body'] in all_channels:
						all_channels[msg['body']].append(msg['from'])
						print_channel_members(all_channels)
					else:
						all_channels.update({msg['body']: [msg['from']]})
						print_channel_members(all_channels)

					print("User: " + msg['from'])
				else:
					process_message(msg, all_sockets, [s, active_socket])
				
			except Exception as e:
				broadcast("User {} has left the channel\n".format(addr), all_sockets, [s, active_socket])
				all_sockets.remove(active_socket)
				active_socket.close()
				exception_record = "An exception of type {0} occurred. \nArguments:{1!r}"
				exception_print = exception_record.format(type(e).__name__, e.args)
				print(exception_print)


s.close()
