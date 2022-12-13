#Author: Pearson Lawrence
#Finished: 12/11/2022
#This program runs the core game loop of the quickroute game. The server mainly does all of the game logic, sending it all to the clients and only expecting simple answers in return
#This program will create a lobby from a host, and then allow players to join said lobby. Once the lobby fills up then the game begins!
#The server creates a graph and sends the information to the players, having them find the shortest path in a premade routing graph that generates random
#path lengths, it uses Dijkstra algorithm to find the length of the shortest path and stores it.
#Once the clients have their answers they send it to the server, where the server checks their answer against the correct answer from the algorithm
#The first player to answer correctly wins a round and then a new round is created. Once someone has won the maximum number of rounds the game ends and closes all connections
import socket
import select
import netmsg
import os
import time
import shortestPathUtils
import random

#------------State variables-----------#
#--See state machine for explenations--#
STARTSTATE = 1
LOBBYSTATE = 2
RUNNINGSTATE = 3
GAMEOVERSTATE = 4
ENDSTATE = 5
#-------------------------------------#

ANSWER_MSG = "answer"

#serverLobbyState: Acts as the game lobby, where the host waits for players to connect.	
				# This state listens for connections and accepts them while setting up player info needed to socket
				# Once the max number of players connect then the state will switch to running which runs game loop
				# If an error occurs, such as client suddenly disconnecting, or failing to send/receive data then the state will 
				# Change to game over
#This function does
#1.) Gets a list of sockets that have info
#2.) Accepts connections from sockets
#3.) Request name from new socket
#4.) Takes name and setsup player to socket
#5.) Sends lobby info (players) to players connected
#5.) Repeats until match has reached max players
#6.) Sends message telling clients the match is starting
#7.) Sends to running state
#Note: If error (players disconnect suddenly, some messaging error) lobby will close and game with exit
def serverLobbyState(server_socket, maxPlayers, client_list, currentPlayers, socket_mapping, playersJoined, playerScores,answersRecevied):
	try: #Try to get connections
		outState = LOBBYSTATE #By default return lobby state to re-loop
		rList,  [], [] = select.select(client_list, [], []) #This selects sockets with i/o at OS level and gets the sockets with current i/o storing in list

		#For each socket that has information (rlist)
		for socket in rList:

			if socket == server_socket: #if current socket is the server
				client_socket, client_address = server_socket.accept() #Accepts connection on server socket, and stores the clients socket and address (IP:PORT)
																	   
				try: #Try to receive message from client socket (First syn)
					status = netmsg.receive_message(client_socket) #Simulating a three way handshake: receiving the first syn
																   #Receives a message storing the status if the playe is attempting connection
				except: #If it couldnt return error true
					print("Could not receive msg ")
					return outState, server_socket, client_list, currentPlayers, playersJoined, playerScores, socket_mapping, answersRecevied, True

				print(status)
				
				if len(currentPlayers) == maxPlayers: #If there are already the max amount of players
					netmsg.send_to_one(client_socket, "DC Sorry, server full! ") #Tell the newly connected client that the server is full and it should disconnect (First syn-ack)
					client_socket.close() #Close connection to client
				else: #If the lobby is not full
					netmsg.send_to_one(client_socket, "SVR NM Please Enter Player Name: ") #Tekk the newly connected client that you want its name (First syn-ack)
					
					name = netmsg.receive_message(client_socket) #Receive the requested name from the client (Second Syn)
					
					#If for some reason we couldnt receie name, continue
					if name is False:
						continue

					#If we have the name
					if name:
						if name in currentPlayers.values(): #If someone already has the name that the client sent then disconnect

							#End of three way handshake, tells client to disconnect and rejoin because name already taken
							netmsg.send_to_one(client_socket, "DC Name already taken. Please choose a different one and join again!\nDisconnecting... ")
							client_socket.close() #closes connection

						else: #If name is not already taken
							#----------Setup Player------------#
							currentPlayers[client_socket] = name #Assigns name to current socket in player dictionary
							socket_mapping[name] = client_socket #Assigns name to socket in socket mapping dictionary
							playerScores[name] = 0				 #Assigns score related to name of player to 0 at start in score dictionary
							answersRecevied[name] = False		 #Assigns weather the answer associated with player name has been received (True/False) to False by default in answerReceived dictionary
							playersJoined += 1					 #Increment players connected to lobby
							client_list.append(client_socket)	 #Add new client socket to the client list
							
							#print out the client information
							print("Participant connected: " + str(client_address) +" [ " + currentPlayers[client_socket] + " ]" )

							
							#Welcome the new client to the lobby using unicasting
							netmsg.send_to_one(client_socket, "SVR TXT Welcome to the lobby " + name + "!\nPlease wait for host to start the game... ")
								
							
							#Create a message that stores how many players have joined in comparision to the max player count
							message = "SVR TXT Players(" + str(playersJoined) + "/" + str(maxPlayers) + "): "
						
							#Loop through all the names of the sockets and add the names to the message created above
							for pname in currentPlayers.values():
								print(pname)
								message += pname + " "
							
							netmsg.send_to_all(server_socket, message, client_list) 

							#If the lobby has reached full capacity then start the game
							if playersJoined == maxPlayers:
								
								#Multicast and tell all sockets that the match is about to start
								netmsg.send_to_all(server_socket, "SVR TXT \nThe match starts in 10 seconds. \nFind the shortest distance between two nodes in a routing graph. \nAnswer first to win!\n ", client_list)

								#All players joined so change to main game loop running state
								outState = RUNNINGSTATE
								time.sleep(10) #Start match in 10 seconds after waiting
								
								return outState, server_socket, client_list, currentPlayers, playersJoined, playerScores, socket_mapping, answersRecevied, False #Return no error

	except: #If A client disconnects suddenly or a message is failed to be received, an error is thrown
		print("An error occured, client disconnected suddenly or failed to send/receive information")
		outState = GAMEOVERSTATE #Change state to game over to close connections that have been made
		return outState, server_socket, client_list, currentPlayers, playersJoined, playerScores, socket_mapping, answersRecevied, True #Return error occured
		
	return outState, server_socket, client_list, currentPlayers, playersJoined, playerScores, socket_mapping, answersRecevied, False #Return no error. This is the loop information

#serverRunningState: is the core game loop. Where the server does not act as a player
				   # This state prompts users with simulated routing graphs and the distance between two nodes on said graph
				   # Prompts by sending messages over the server, then waiting to receive messages (answers) from the clients back in the client list
				   # Keeps track of answers, if the round has been won (someone answered correctly first), if new round should start, and if game has been won and is over
				   # If error occurs, such as client suddenly disconnecting, or failing to send/receive data, then state will change to game over
def serverRunningState(server_socket, client_list, player_dic, score_dic,answerRecevied_dic, roundWinInfo_dic, maxScore,route_msg):
	outState = RUNNINGSTATE #Default out state for looping purposes
	
	try: #Try to run game loop
		allAnswersReceived = True #Setup all Answered received variable for this loop. 
								  #Defaulted to true for for loop purpose
		#For each value of answeresReceived_dic (dictionary containing if a player has answered)						  
		for recv in answerRecevied_dic.values():
			if recv == False:					#If any value is false then all answers have not been received
				allAnswersReceived = False
		
		if allAnswersReceived: #If all players have answered
			
			#go into the roundWinInfo_dic and check to see if the game is over
			if roundWinInfo_dic["game over"] == "true":
				#If it is over then tell everyone who won the last round using multicasting
				netmsg.send_to_all(server_socket,  roundWinInfo_dic["msg"], client_list)
				#Delay the game over screen from printing to allow for people to read final message
				time.sleep(1)
				outState = GAMEOVERSTATE #Change out state to game over and return out without error
				return outState, server_socket, client_list, score_dic,answerRecevied_dic, roundWinInfo_dic, route_msg, False

			#If the round has been won but the game is not over
			if roundWinInfo_dic["round won"] == "true":
				#Tell everyone who won the last round by sending the win info message through multicasting
				omsg = roundWinInfo_dic["msg"] + "\nStarting new round in 5 seconds... "
				netmsg.send_to_all(server_socket, omsg, client_list)
			else: #If there was no winner last round (No one submitted correct answer)
				#Multicast and tell everyone no one was correct and tell them to prepare for next round
				netmsg.send_to_all(server_socket, "SVR TXT No winner this round, moving onto next round in 5 seconds: ", client_list)

			#Reset the answers received and results for next round for each player
			for recv in answerRecevied_dic.keys():
				answerRecevied_dic[recv] = False
			
			roundWinInfo_dic["round won"] = "false" #Resets round won
			roundWinInfo_dic["new round"] = "true"	#Tells the round info to start a new round
			time.sleep(5) #Waits five seconds to give players time to prepare and then returns out to start next loop
			return outState, server_socket, client_list, score_dic,answerRecevied_dic, roundWinInfo_dic, route_msg, False
		
		if roundWinInfo_dic["new round"] == "true": # If it is a new round
			
			print("Start round")
			roundWinInfo_dic["new round"] = "false" # Set new round to false so it doesnt resend this information 
			rand = random.randrange(1,4) 
			startNode, endNode, graph, answer = shortestPathUtils.genGraph(rand) #Generate a premade graph between 1 and 4
																			     #This function selects a premade routing graph, and propagates the paths with random values
																				 #It then uses Dijkstra's algorithm to find the shortest path between two randomly selected nodes
																				 #It outputs the start and end nodes, the graph as an array of strings, and the length of the shortest path from dijkstra's
			route_msg = str(answer)	#Convert the answer from an int to a string and store it

			#Create the message that is going to store the graph from the array of strings for visual output
			graphMsg = "SVR TXT " #propagate it with codes for the client
			for line in graph:	#For each string in the array of strings
				graphMsg += "\n" + line  #Add string to message
			
			#Create message that tells the client what path to find between two nodes
			graphMsg += "\nFind shortest path from NODE:" + startNode + " to NODE:" + endNode + "\n" + " "
			
			#For server debug to see visual graph and message
			print(graphMsg)

			#Multicast to all the round information
			netmsg.send_to_all(server_socket, graphMsg, client_list)
			time.sleep(1)

			#Prompt the user to enter their answer using multicasting and speacial code
			netmsg.send_to_all(server_socket, "SVR GM Please enter the length of the shortest path: ", client_list) #Uses special NXT code to tell the user they cant enter input to send
		else:

			rList,  [], [] = select.select(client_list, [], []) #This selects sockets with i/o at OS level and gets the sockets with current i/o storing in list
			
			for soc in rList: #Go through all the sockets that have information
				if soc != server_socket: #If the socket is a client
					try: #Attempt to receive message
						answer = netmsg.receive_message(soc) #This message is designed to be the players answer
					except:#If message could not be received end with error
						print("Error receiving message")
						outState = GAMEOVERSTATE
						return outState, server_socket, client_list, score_dic,answerRecevied_dic, roundWinInfo_dic, route_msg, True
					
					#Get the name of the current socket from player_dic
					name = player_dic[soc]
					answerRecevied_dic[name] = True #Set answer received for socket name to True for game management
					if answer == route_msg: # If the client answered correctly
						#answerResult_dic[name] = True #Note down their correct answer
						#If round won is currently false, meaning no one has answered correctly before this player
						if roundWinInfo_dic["round won"] == "false": 
							score_dic[name] += 1 #Increase score of player from name by 1, player has won a round
							roundWinInfo_dic["round won"] = "true" #Set round won to true so whoever answers after this client will not get any points as they lost
							roundWinInfo_dic["name"] = name #Assign the win info to who won associated with name

							#Create a message for round info about who won the round and what their current score is 
							msg = "SVR TXT " +"\n" + name + " answered correctly first! Their score is: " + str(score_dic[name]) + "/" + str(maxScore) + "\n "
							print(msg) #Display message to server 
							roundWinInfo_dic["msg"] = msg #Assign the message to roundwin info
							if score_dic[name] >= maxScore: #If the player has reached the max score then he has won the match
							
								roundWinInfo_dic["game over"] = "true" #Set game over to true in round info
					
					#Use multicast to Send this to everyone every time someone answers a question, letting everyone know how many players they are waiting on
					answerRecevied = "SVR TXT " + name + " submitted answer, waiting for all answers to be submitted "
					netmsg.send_to_all(server_socket, answerRecevied, client_list)
	except:#If an error occured (Couldent send/receive, client disconnected suddenly) then end the game
		print("A Client disconnected suddenly")
		outState = GAMEOVERSTATE
		return outState, server_socket, client_list, score_dic,answerRecevied_dic, roundWinInfo_dic, route_msg, True #Return with error 
		
				
	return outState, server_socket, client_list, score_dic,answerRecevied_dic, roundWinInfo_dic, route_msg, False #Return for looping purposes, no error
	
#gameOverState: sends a message to all the clients explaining that the game is over. 
			  # It will explain why the game ended, if errorOccured passed in is = to true then the game ended because of an error
			  # If it is false then the game ended because someone won. 
			  # Now that the game is over send appropriate end message then wait 5 seconds before sending disconnect message to client 
			  # Before closing the socket of all the clients and then the server
def gameOverState(server_socket, client_list, roundWinInfo_dic,errorOccured):
	time.sleep(1)
	GO_msg = "DC " #Client codes
	#If error create error message
	if errorOccured:
		GO_msg += "\n|-------------------------------------|"
		GO_msg += "\n|             Quick Route             |"
		GO_msg += "\n|                                     |"
		GO_msg += "\n|           An Error occured          |"
		GO_msg += "\n|                                     |"
		GO_msg += "\n|     Disconnecting in 5 seconds      |"
		GO_msg += "\n|-------------------------------------|"
	else: #If not error create win message
		GO_msg += "\n|-------------------------------------|"
		GO_msg += "\n|             Quick Route             |"
		GO_msg += "\n|                                     |"
		GO_msg +=  "\n*      Player: " + roundWinInfo_dic["name"] + " has won this match!      *"
		GO_msg += "\n|                                     |"
		GO_msg += "\n|     Disconnecting in 5 seconds      |"
		GO_msg += "\n|-------------------------------------| "
	
	#Muilticast and send resulting message to all clients
	netmsg.send_to_all(server_socket,GO_msg,client_list)
	print(GO_msg)
	time.sleep(5) #Wait five seconds and then for each client send the disconnect message
	#netmsg.send_to_all(server_socket, "DC Disconnecting user...", client_list) #DC is disconnect client message code
	for sock in client_list:
		sock.close() #Close client
	server_socket.close() #Close socket

#runServerStateMachine: This function manages a small state machine that runs the core game loop. 
					   # Takes in a maximum amount of players (p), and the max score (s) needed to win a match
					   # It firstly opens a server then opens a lobby waiting for players to join
					   # Once all the players have joined then it will switch to running state which is the game
					   # loop where players compete to find the shortest path between two points in a network routing graph
					   # Once someone has won all the rounds it lets everyone know and then disconnects everyone and closes the server
def runServerStateMachine(p, s):
	
	os.system('cls' if os.name == 'nt' else 'clear') #Clear terminal for clean printing
		
	isRunning = True   #While loop control condition
	state = LOBBYSTATE #Sets the state mchine to start in the lobby state

	server_socket = netmsg.open_host_socket(p, 1111) #Opens a socket to host connections on for port 1111 (As long as the number is not small)
	clientList = [server_socket] #Creates an array of sockets and makes the server socket the first one added
	players = {} 			#Dictionary to contain player names associated with sockets
	scores = {}  			#Dictionary to contain player scores associated with names
	socket_mapping = {}		#Dictionary to assign names to sockets
	answersRecevied = {}	#Dictionary to tell if answers have been received (true/false), associated to player names
	player_count = 0 		#Player count is the amount of connected players used to determine lobby state info
	#Round info dictionary contains important info about a round. #Stores: wether a round has been won 
	roundInfo = {"round won" : "false","name" : "", "msg" : "", "new round" : "true", "game over" : "false"} 
				# "round won" : ("true"/"false")
				# Name of person who won round "name" : (name associated with socket)
				# A winners message that contains winner name and score
				# Information on weather new round should be started "new round" condition : ("true"/"false")
				# Information on weather the game is over, either through error handling or win condition reached "game over" : condition ("true"/"false")

	routeAnswer_msg = "" #Variable to store the length of the correct path as a string to be sent over network
	
	isError = False #This is used as output to tell if an error occured in either of the states

	#Server is officially ready and open
	print("Quickstart Server Open. Waiting for connections...")

	#While isRunning is true the state machine will run, it is only ever changed when the game is over, if error occurs the game will enter gameover state
	while isRunning:
		if state == LOBBYSTATE:#----------> Lobby state is the game lobby, where the host waits for players to connect.	
									  	  # This state listens for connections and accepts them while setting up player info needed to socket
									  	  # Once the max number of players connect then the state will switch to running which runs game loop
									  	  # If an error occurs, such as client suddenly disconnecting, or failing to send/receive data then the state will 
									  	  # Change to game over
			state,server_socket,clientList,players,player_count,scores,socket_mapping,answersRecevied,isError = serverLobbyState(server_socket,p,clientList,players,socket_mapping,player_count,scores,answersRecevied)
		elif state == RUNNINGSTATE:#------> Running state is the core game loop. Where the server does not act as a player
										  # This state prompts users with simulated routing graphs and the distance between two nodes on said graph
										  # Prompts by sending messages over the server, then waiting to receive messages (answers) from the clients back in the client list
										  # Keeps track of answers, if the round has been won (someone answered correctly first), if new round should start, and if game has been won and is over
										  # If error occurs, such as client suddenly disconnecting, or failing to send/receive data, then state will change to game over
			state,server_socket,clientList,scores,answersRecevied,roundInfo,routeAnswer_msg,isError = serverRunningState(server_socket,clientList,players,scores,answersRecevied,roundInfo,s,routeAnswer_msg)
		elif state == GAMEOVERSTATE:#-----> Game over state will send a message to all the clients, Will send a message telling 
										  # If the game ended because of an error (someone left or something went wrong),
										  # or if someone has won the match
										  # After sending it will send the disconnect code to the client
										  # And then close all of the client sockets before changing isRunning to false
			gameOverState(server_socket, clientList, roundInfo,isError)
			isRunning = False #Once false the function will exit
	

	
	
