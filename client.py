import socket
import random
import string
import json
import sys
import select

ID_LENGTH = 6
SERVER_HOSTNAME = 'localhost'
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

user_id = id_generator()

msg = {}
msg['to'] = "server_initial"
msg['from'] = user_id
msg['body'] = "hello from user {}.".format(user_id)

try:
	s.connect((SERVER_HOSTNAME, PORT))
except:
	print("There was a problem connecting. The server may not be running.")
	exit()

sys.stdout.write("Welcome\n")
prompt_flush(user_id)

#-----------------------------------------------#
#                  Run client                   #
#-----------------------------------------------#

while True:
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
			msg['to'] = "server"
			msg['from'] = user_id
			msg['body'] = sys.stdin.readline()
			s.send(json.dumps(msg).encode())
			prompt_flush(user_id)
