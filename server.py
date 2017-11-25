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
DEFAULT_USERS = {
	# 'poobear': <socket object>,
}

#-----------------------------------------------#
#                Set up server                  #
#-----------------------------------------------#

all_sockets = []
all_channels = DEFAULT_CHANNELS
all_users = DEFAULT_USERS

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# No address specified so a device with any IP address can connect 
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
			all_sockets.append(c)
			print("\tGot connection from {}".format(addr))
		else:
			try:
				# Incoming message
				msg = loads(active_socket.recv(MAX_MSG_SIZE).decode())
				if msg['to'] == "JOINCHANNEL":
					if msg['from'] not in all_users:
						# new user added to user list
						all_users.update({msg['from']:active_socket})
						print_all_users(all_users)
					join_channel(all_channels, all_users, msg['from'], msg['body'])
					print_channel_members(all_channels)
				elif msg['to'] == "LISTCHANNELS":
					list_channels(all_channels, all_users[msg['from']])
				elif msg['to'] == "LEAVECHANNEL":
					pass
				elif msg['to'] == "LISTUSERS":
					list_users(all_channels, all_users, msg['body'], all_users[msg['from']])
				else:
					broadcast_to_channel(msg, all_users, all_channels, active_socket)
				
			except Exception as e:
				broadcast_to_workspace("User {} has left the channel\n".format(addr), all_sockets, [s, active_socket])
				all_sockets.remove(active_socket)
				active_socket.close()
				# exception_record = "An exception of type {0} occurred. \nArguments:{1!r}"
				# exception_print = exception_record.format(type(e).__name__, e.args)
				# print(exception_print)


s.close()
