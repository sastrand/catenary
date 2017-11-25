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
				print("An error has occured in broadcast_to_workspace.\n\n{}".format(e))

def broadcast_to_channel (msg, recipients, channels, ommitted):
	body = "\r[" + msg['from'] + "] " + msg['body']
	for user in recipients:
		if user in channels[msg['to']] and recipients[user] != ommitted:
			try:
				recipients[user].send(body.encode())
			except Exception as e:
				print("An error has occured in broadcast_to_channel.\n\n{}".format(e))

def send_to_user (msg, recipient):
	try:
		recipient.send(msg.encode())
	except Exception as e:
		print("An error has occured in send_to_user.\n\n{} ".format(e))

def list_channels (all_channels, recipient):
	try:
		send_to_user("\r+--------------------------------+"\
		"\n|          All Channels          |"\
		"\n+--------------------------------+\n\r", recipient)
		for channel in all_channels:
			send_to_user("\r" + str(channel) + "\n\r", recipient)
	except Exception as e:
		print("An error has occured in list_channels.\n\n{}".format(e))

def client_disconnect (all_sockets, ommitted, all_channels, all_users, socket_out):
	try:
		for user in all_users:
			if all_users[user] == socket_out:
				leave_workspace(all_channels, all_users, user)
				msg = "User {} has left the channel.\n".format(user)
				broadcast_to_workspace(msg, all_sockets, ommitted)
				break
	except Exception as e:
		print("An error has occured in client_disconnect.\n\n{}".format(e))

def leave_workspace (all_channels, all_users, leaving_user):
	try:
		del all_users[leaving_user]
		leave_channels(all_channels, leaving_user)
	except Exception as e:
		print("An error has occured in list_channels.\n\n{}".format(e))

def list_users (all_channels, all_users, channel, recipient):
	try:
		channel_str = "#" + channel[:31]
		send_to_user("\r+--------------------------------+"\
		"\n|" + channel_str.center(32) + "|"\
		"\n+--------------------------------+\n\r", recipient)
		for user in all_channels[channel]:
			send_to_user("\r {:12s}{:16s}\n".format(user[:11], str(all_users[user].getpeername())), recipient)
	except Exception as e:
		print("An error has occured in list_channels.\n\n{}".format(e))	

def join_channel (all_channels, all_users, user, channel):
	try:
		if channel in all_channels and user not in all_channels[channel]:
			# user joins existing channel
			leave_channels(all_channels, user)
			all_channels[channel].append(user)
		else:
			# existing user creates channel
			leave_channels(all_channels, user)
			all_channels.update({channel: [user]})
	except Exception as e:
		print("An error has occured in join_channel.\n\n{}".format(e))

def leave_channels (all_channels, user):
	try:
		for channel in all_channels:
			if user in all_channels[channel]:
				all_channels[channel].remove(user)
	except Exception as e:
		print("An error has occured in leave_channel.\n\n{}".format(e))

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
			print(" {:16s}{:16s}".format(channel[:15], user[:16]))
