# Copyright (c) 2017 Sascha Strand
# Available open source through the MIT License

# To do: user can leave channel by prompt and leaves all_users list at close
# To do: user can leave channel on disconnect (see recipients.remove comments)
# To do: user can list all rooms
# To do: .private messaging
# To do: .enhanced security
# To do: .file transfer
# To do: order all users by IP
# To do: order Channel membership

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
					if not msg['from'] in all_users:
						all_users.update({msg['from']:active_socket})
						print_all_users(all_users)
					if msg['body'] in all_channels:
						all_channels[msg['body']].append(msg['from'])
						print_channel_members(all_channels)
					else:
						all_channels.update({msg['body']: [msg['from']]})
						print_channel_members(all_channels)
				elif msg['to'] == "LISTCHANNELS":
					list_channels(all_channels, all_users[msg['from']])
				elif msg['to'] == "LEAVECHANNEL":
					print("here2")
					leave_channel(all_channels, all_users[msg['from']], all_users[msg['body']])
					print("User {} left channel {}".format(msg['from'], msg['body']))
					print_channel_members(all_channels)
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
