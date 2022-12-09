import socket
import select
import netmsg
import sys
import os
import time

STARTSTATE = 1
LOBBYSTATE = 2
RUNNINGSTATE = 3
GAMEOVERSTATE = 4
ENDSTATE = 5
GAME_MSG = "game"
ANSWER_MSG = "answer"
        
def serverLobbyState(server_socket, maxPlayers, client_list, currentPlayers, playersJoined, playerScores,answerResult,answersRecevied):
	socket_mapping = {}
	outState = LOBBYSTATE
	rList,  [], [] = select.select(client_list, [], [])
	for socket in rList:
		
		if socket == server_socket:
			
			client_socket, client_address = server_socket.accept()
			
			status = netmsg.receive_message(client_socket)
			print(status)
			
			if len(currentPlayers) == maxPlayers:
				netmsg.send_to_one(client_socket, "SVR TXT Sorry, server full!")
				netmsg.send_to_one(client_socket, "DC")
				client_socket.close()
			else:
				netmsg.send_to_one(client_socket, "SVR TXT Please Enter Player Name: ")
				
				name = netmsg.receive_message(client_socket)
				
				if name is False:
					continue

				if name:
					if name in currentPlayers.values():
						
						netmsg.send_to_one(client_socket, "SVR TXT Name already taken. Please choose a different one and join again!")
						
						client_socket.close()
					else:
						currentPlayers[client_socket] = name
						socket_mapping[client_socket] = client_address
						playerScores[name] = 0
						answerResult[name] = False
						answersRecevied[name] = False
						playersJoined += 1
						client_list.append(client_socket)
						print("Participant connected: " + str(client_address) +" [ " + currentPlayers[client_socket] + " ]" )
						if playersJoined < maxPlayers:
							
							netmsg.send_to_one(client_socket, "SVR TXT Welcome to the lobby " + name + "!\nPlease wait for host to start the game...")
							
							message = "SVR TXT Players(" + str(playersJoined) + "/" + str(maxPlayers) + "): "
							for pname in currentPlayers.values():
								print(pname)
								message = message + pname + " "
							netmsg.send_to_all(server_socket, message, client_list)

						if playersJoined == maxPlayers:
							netmsg.send_to_all(server_socket, "SVR TXT \nParticipant(s) joined:", client_list)
							for i in currentPlayers:
								netmsg.send_to_all(server_socket,">> " + currentPlayers[i], client_list)
							netmsg.send_to_all(server_socket, "SVR TXT \nThe quiz will begin in 30 seconds. Quickly go through the instructions\n", client_list)
							print("\n wtf")
							outState = RUNNINGSTATE
							
							return outState, server_socket, client_list, currentPlayers, playersJoined, playerScores, socket_mapping, answersRecevied, answerResult 
	return outState, server_socket, client_list, currentPlayers, playersJoined, playerScores, socket_mapping, answersRecevied, answerResult

def serverRunningState(server_socket, client_list, player_dic, score_dic, answerResult_dic ,answerRecevied_dic, roundWinInfo_dic , socket_mapping, maxScore,route_msg):

	outState = RUNNINGSTATE
	isGameOver = False
	allAnswersReceived = True
	Arcv = answerRecevied_dic
	Ares = answerResult_dic
	roundWinInfo = roundWinInfo_dic
	OutScores = score_dic
	outRouteMsg = route_msg
	for recv in Arcv.values():
		if recv == False:
			allAnswersReceived = False
	print(roundWinInfo["round won"])
	print(roundWinInfo["msg"])
	if allAnswersReceived:
				
		if roundWinInfo["round won"] == "true":
			print("won")
			netmsg.send_to_all(server_socket, roundWinInfo["msg"], client_list)
		else:
			print("!won")
			netmsg.send_to_all(server_socket, "SVR TXT No winner this round, moving onto next round in 5 seconds:", client_list)

		for recv in Arcv.keys():
			Arcv[recv] = False
			Ares[recv] = False
			
		allAnswersReceived = False
		roundWinInfo["round won"] = "false"
		roundWinInfo["new round"] = "true"
		time.sleep(5)
		return outState, server_socket, client_list, OutScores, Ares ,Arcv, roundWinInfo

	if roundWinInfo["new round"] == "true":
	
		print("Start round")
		roundWinInfo["new round"] = "false"
		netmsg.send_to_all(server_socket, "SVR GM NXT Please enter the length of the shortest path:", client_list)
	else:
		
		rList,  [], [] = select.select(client_list, [], [])

		for socket in rList:
			
			if socket != server_socket:
				msg = netmsg.receive_message(socket)
				code1 = msg.split(" ")[0]
				if code1 == "answer":
					distance_answer = msg.split(" ")[1]
					print("split")
					#address = socket_mapping[socket]
					name = player_dic[socket]
					Arcv[name] = True
					if distance_answer == route_msg:
						print("running10")
						Ares[name] = True
						if roundWinInfo["round won"] == "false":
							print("running11")
							print(OutScores[name])
							OutScores[name] += 1
							print(OutScores[name])

							roundWinInfo["round won"] = "true"
							roundWinInfo["name"] = name
							print("running12")
							msg = "SVR TXT " + name + " answered correctly first! Their score is: " + str(OutScores[name]) + "/" + str(maxScore)
							print(msg)
							roundWinInfo["msg"] = msg
							print("running13")
							if OutScores[name] >= maxScore:
								outState = GAMEOVERSTATE
						
					answerRecevied = "SVR TXT " + name + " submitted answer, waiting for all answers to be submitted"
					netmsg.send_to_all(server_socket, answerRecevied, client_list)
	
				
	return outState, server_socket, client_list, OutScores, Ares ,Arcv, roundWinInfo
	


def runServerStateMachine(p, s):
	os.system('cls' if os.name == 'nt' else 'clear')
		
	score = s
	isRunning = True
	state = LOBBYSTATE

	server_socket = netmsg.openHostSocket(p, 1111)
	clientList = [server_socket]
	players = {}
	scores = {}
	socket_mapping = {}
	answerResult = {}
	answersRecevied = {}
	roundInfo = {"round won" : "false","name" : "", "msg" : "", "new round" : "true"}
	player_count = 0
	isRoundWinner = False
	routeAnswer_msg = ""
	while isRunning:
		if state == LOBBYSTATE:
			state,server_socket,clientList,players,player_count,scores,socket_mapping,answersRecevied,answerResult = serverLobbyState(server_socket,p,clientList,players,player_count,scores,answersRecevied,answerResult)
		elif state == RUNNINGSTATE:
			
			state,server_socket,clientList,scores,answerResult,answersRecevied,roundInfo = serverRunningState(server_socket,clientList,players,scores,answerResult,answersRecevied,roundInfo,socket_mapping,s, "11")
		elif state == ENDSTATE:
			for sock in clientList:
				netmsg.send_to_all(server_socket, "Disconnect", clientList)
				print("close")
				sock.close()
			isRunning = False
	
		#os.system('cls' if os.name == 'nt' else 'clear')

	
	
