# Copyright (c) 2017 Sascha Strand
# Available open source through the MIT license

from json import loads
from select import select

def broadcast_to_workspace (body, recipients, ommitted):
	for socket in recipients:
		if socket not in ommitted:
			try:
				socket.send(body.encode())
			except Exception as e:
				socket.close()
				recipients.remove(socket)
				print("A client has been disconnected due to an error: {}".format(e))

def broadcast_to_channel (msg, recipients, channels, ommitted):
	body = "\r[" + msg['from'] + "] " + msg['body']
	for user in recipients:
		if user in channels[msg['to']] and recipients[user] != ommitted:
			try:
				recipients[user].send(body.encode())
			except Exception as e:
				recipients[user].close()
				# recipients.remove(user) #make sure pass-by-value works or abstract out globals
				print("A client has been disconnected due to an error: {}".format(e))

def send_to_user (msg, recipient):
	try:
		recipient.send(msg.encode())
	except Exception as e:
		recipient.close()
		# recipients.remove(user) #make sure pass-by-value works or abstract out globals
		print("A client has been disconnected due to an error: {}".format(e))

def list_channels (all_channels, recipient):
	try:
		send_to_user("\r+--------------------------------+"\
		"\n|          All Channels          |"\
		"\n+--------------------------------+\n\r", recipient)
		for channel in all_channels:
			send_to_user("\r" + str(channel) + "\n\r", recipient)
	except Exception as e:
		recipient.close()
		# recipients.remove(user) #make sure pass-by-value works or abstract out globals
		print("A client has been disconnected due to an error: {}".format(e))

def leave_channel(all_channels, user, channel):
	pass
	## Implement leave_channel
	## 

def print_all_users(all_users):
	print("\n+--------------------------------+")
	print("|        All Users With IP       |")
	print("+--------------------------------+")
	for user in all_users:
		print(" {:12s}{:16s}".format(user[:11], str(all_users[user].getpeername())))

def print_channel_members(all_channels):
	print("\n+--------------------------------+")
	print("|       Channel Membership       |")
	print("+--------------------------------+")
	for channel in all_channels:
		# print(channel)
		for user in all_channels[channel]:
			# print("   " + channel + ": " + user)
			print(" {:16s}{:16s}".format(channel[:15], user[:16]))
