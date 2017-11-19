# Copyright (c) 2017 Sascha Strand
# Available open source through the MIT license

from json import loads
from select import select

def process_message(msg, all_sockets, ommitted_broadcast):
	body = "\r[" + msg['from'] + "] " + msg['body']
	broadcast(body, all_sockets, ommitted_broadcast)

def broadcast (body, recipients, ommitted):
	for socket in recipients:
		if socket not in ommitted:
			try:
				socket.send(body.encode())
			except Exception as e:
				socket.close()
				recipients.remove(socket)
				print("A client has been disconnected due to an error: {}".format(e))

def print_all_users(all_users):
	print("\n+--------------------------------+")
	print("|         All Users By IP        |")
	print("+--------------------------------+")
	for user in all_users:
		print(user['ip_address'])
		print(user['socket_obj'])
	print("")

def print_channel_members(all_channels):
	print("\n+--------------------------------+")
	print("|       Channel Membership       |")
	print("+--------------------------------+")
	for channel in all_channels:
		# print(channel)
		for user in all_channels[channel]:
			# print("   " + channel + ": " + user)
			print(" {:16s}{:16s}".format(channel[:15], user[:16]))
