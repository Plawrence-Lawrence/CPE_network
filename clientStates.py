import socket
import select
import sys
import netmsg
import time

MSG_LEN = 10
DISCONNECT_MSG = "DC"
GAME_MSG = "GM"
SERVER_MSG = "SVR"
TEXT_MSG = "TXT"
GAMEOVER_MSG = "GO"
WIN_MSG = "WIN"
NXTROUND_MSG = "NXT"
NAMERQST_MSG = "NM"
def clientStateMachine(IP, PORT):

	MSG_LEN = 5

	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	if IP == "":
		IP = socket.gethostname()
		PORT = 1111

	try:
		client.connect((socket.gethostname(), 1111))
	except:
		print("CAN'T CONNECT TO SERVER!")
		sys.exit()
	client.setblocking(False)
	netmsg.send_to_one(client, "Connected: ")
	print("Connected to server. Loading lobby...")
	
	isPlaying = True
	while isPlaying:
		sockets_list = [client]
		read_sockets,[], [] = select.select(sockets_list,[],[])
		for currentSocket in read_sockets:
			if currentSocket == client:
				encoded_message = netmsg.receive_message(currentSocket)
				code = encoded_message.split(" ")
				
				if code[0] == DISCONNECT_MSG:
					isPlaying = False
					m1 = encoded_message.replace(code[0],'')
					print(m1)
					time.sleep(1)
					client.close()
				elif code[0] == SERVER_MSG:
						if code[1] == GAME_MSG:
							m1 = encoded_message.replace(code[0],'')
							m2 = m1.replace(code[1],'')
							m3 = m2.replace(code[2],'')
							
							if code[2] == NXTROUND_MSG:
								pathDist = input("			>", )
								msg = "answer " + pathDist
								netmsg.send_to_one(client, msg)
						elif code[1] == TEXT_MSG:
							m1 = encoded_message.replace(code[0],'')
							m2 = m1.replace(code[1],'')
							print(m2)
						elif code[1] == NAMERQST_MSG:
							m1 = encoded_message.replace(code[0],'')
							m2 = m1.replace(code[1],'')
							print(m2)
							
							name = ""
							while name == "":
								name = (input("      > "))
							
							netmsg.send_to_one(client, name)





   