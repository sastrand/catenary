import socket
import random
import string
import json
import sys
import select

ID_LENGTH = 6
SERVER_HOSTNAME = "localhost"
PORT = 8080
SELF_ID = "[You] "

def id_generator():
	return ''.join(random.choice(string.ascii_letters + string.digits) for i in range(ID_LENGTH))

def prompt_flush(ps1):
	sys.stdout.write("[" + ps1 + "] ")
	sys.stdout.flush()

#-----------------------------------------------#
#               Set up connection               #
#-----------------------------------------------#

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
	s.connect((SERVER_HOSTNAME, PORT))
	print("\n+--------------------------------+")
	print("|       Welcome to Catenary      |")
	print("+--------------------------------+")
except:
	print("There was a problem connecting to the server.")
	exit()

user_id = input("Please enter a user id\n")
if not user_id:
	user_id = id_generator()
print("Welcome {}".format(user_id))

channel = input("What channel would you like to join?\n")
if not channel:
	channel = "main"

msg = {}
msg['to'] = "JOINCHANNEL"
msg['from'] = user_id
msg['body'] = channel

s.send(json.dumps(msg).encode())

prompt_flush(user_id)

#-----------------------------------------------#
#                  Run client                   #
#-----------------------------------------------#

while True:
	while msg['body'] != ":::\n":
		all_sockets = [sys.stdin, s]

		active_sockets,_,_ = select.select(all_sockets, [], [])

		for active_socket in active_sockets:
			if active_socket == s:
			# messages from server
				data = active_socket.recv(4096).decode()
				if data:
					sys.stdout.write(data)
					prompt_flush(user_id)
				else:
					print("The server has closed your connection.")
					exit()
			else:
			# message to the server
				msg['body'] = sys.stdin.readline()
				if msg['body'] != ":::\n":
					msg['to'] = channel
					msg['from'] = user_id
					s.send(json.dumps(msg).encode())
					prompt_flush(user_id)
	msg['body'] = ''
	msg['from'] = user_id
	sys.stdout.write("command: ")
	sys.stdout.flush()
	command = sys.stdin.readline()
	if command in ["list\n", "l\n"]:
		msg['to'] = "LISTCHANNELS"
	if command in ["join\n", "j\n"]:
		ret = input("channel: ")
		if ret != '': channel = ret
		msg['to'] = "JOINCHANNEL"
		msg['body'] = channel
	if command in ["quit\n", "q\n"]:
		msg['to'] = "LEAVEWORKSPACE"
		s.send(json.dumps(msg).encode())
		prompt_flush(user_id)
		s.close()
		print("goodbye")
		exit()
	if command in ["users\n", "u\n"]:
		msg['to'] = "LISTUSERS"
		msg['body'] = channel
	if command in ["closer server\n", "cs\n"]:
		msg['to'] = "CLOSESERVER"
		msg['body'] = "password"
	if command in ["direct message\n", "dm\n"]:
		msg['to'] = "DIRECTMESSAGE"
		recipient = input("recipient: ")
		content = input("conents: ")
		msg['body'] = recipient + ":::" + content
	s.send(json.dumps(msg).encode())
	prompt_flush(user_id)

