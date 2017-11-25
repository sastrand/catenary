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
				print("A client has been disconnected due to an error in broadcast_to_workspace: {}".format(e))

def broadcast_to_channel (msg, recipients, channels, ommitted):
	body = "\r[" + msg['from'] + "] " + msg['body']
	for user in recipients:
		if user in channels[msg['to']] and recipients[user] != ommitted:
			try:
				# print("<><> to: " + user + "  at channel: " + msg['to'])
				recipients[user].send(body.encode())
			except Exception as e:
				recipients[user].close()
				# recipients.remove(user) #make sure pass-by-value works or abstract out globals
				print("A client has been disconnected due to an error in broadcast_to_channel: {}".format(e))

def send_to_user (msg, recipient):
	try:
		recipient.send(msg.encode())
	except Exception as e:
		recipient.close()
		# recipients.remove(user) #make sure pass-by-value works or abstract out globals
		print("A client has been disconnected due to an error in send_to_user: {} ".format(e))

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
		print("A client has been disconnected due to an error in list_channels: {}".format(e))

def join_channel (all_channels, all_users, user, channel):
	if channel in all_channels and user not in all_channels[channel]:
		# user joins existing channel
		leave_channels(all_channels, user)
		all_channels[channel].append(user)
	else:
		# existing user creates channel
		leave_channels(all_channels, user)
		all_channels.update({channel: [user]})

def leave_channels (all_channels, user):
	try:
		for channel in all_channels:
			if user in all_channels[channel]:
				all_channels[channel].remove(user)
	except Exception as e:
		recipient.close()
		# recipients.remove(user) #make sure pass-by-value works or abstract out globals
		print("A client has been disconnected due to an error in leave_channel: {}".format(e))

def print_all_users (all_users):
	print("\n+--------------------------------+")
	print("|        All Users With IP       |")
	print("+--------------------------------+")
	for user in all_users:
		print(" {:12s}{:16s}".format(user[:11], str(all_users[user].getpeername())))

def print_channel_members (all_channels):
	print("\n+--------------------------------+")
	print("|       Channel Membership       |")
	print("+--------------------------------+")
	for channel in all_channels:
		# print(channel)
		for user in all_channels[channel]:
			# print("   " + channel + ": " + user)
			print(" {:16s}{:16s}".format(channel[:15], user[:16]))
