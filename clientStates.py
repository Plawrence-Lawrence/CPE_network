import socket
import select
import sys
import netmsg


MSG_LEN = 10
DISCONNECT_MSG = "DC"
GAME_MSG = "GM"
SERVER_MSG = "SVR"
TEXT_MSG = "TXT"
GAMEOVER_MSG = "GO"
WIN_MSG = "WIN"
NXTROUND_MSG = "NXT"
def clientStateMachine(IP, PORT):

	MSG_LEN = 5

	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	if IP == "":
		IP = socket.gethostname()
		PORT = 1111

	print(IP)
	print(PORT)
	try:
		client.connect((socket.gethostname(), 1111))
	except:
		print("CAN'T CONNECT TO SERVER!")
		sys.exit()
	print("test")
	client.setblocking(False)
	netmsg.send_to_one(client, "Connected: ")
	name = (input("Enter Name: "))
	netmsg.send_to_one(client, name)
	
	isPlaying = True
	while isPlaying:
		sockets_list = [client]
		read_sockets,write_socket, error_socket = select.select(sockets_list,[],[])
		for currentSocket in read_sockets:
			if currentSocket == client:
				encoded_message = netmsg.receive_message(currentSocket)
				code1 = encoded_message.split(" ")[0]
				if code1 == DISCONNECT_MSG:
					isPlaying = False
					client.close()
				elif code1 == SERVER_MSG:
						code2 = encoded_message.split(" ")[1]
						if code2 == GAME_MSG:
							code3 = encoded_message.split(" ")[2]
							encoded_message.replace(code1, '')
							encoded_message.replace(code2, '')
							encoded_message.replace(code3, '')
							print(encoded_message)
							if code3 == NXTROUND_MSG:
								pathDist = input("			>", )
								msg = "answer " + pathDist
								netmsg.send_to_one(client, msg)

						if code2 == TEXT_MSG:
							print(encoded_message)
				elif code1 == GAMEOVER_MSG:
					isPlaying = False
					client.close()


			else:
				message = sys.stdin.readline()
				netmsg.send_to_one(client, message)

	


	'''try:
		msg_len = client_socket.recv(MSG_LEN).decode('utf-8')

		if not len(msg_len):
			return False

		message_length = int(msg_len.decode('utf-8').strip())
		return {'Length': msg_len, 'data': client_socket.recv(message_length)}

	except:
		return False'''


'''
while True:
	sockets_list = [sys.stdin, client]
	read_sockets,write_socket, error_socket = select.select(sockets_list,[],[])
	for socket in read_sockets:
		if socket == client:
			encoded_message = receive_message(socket)
			if not encoded_message :
				print("DISCONNECTED")
				sys.exit()
			else:
				message = encoded_message['data'].decode('utf-8')
				print(message)

		else:
			message = sys.stdin.readline()
			send_to_one(client, message)'''


#server.close()

STARTSTATE = 1
LOBBYSTATE = 2
RUNNINGSTATE = 2


   