#Author: Pearson Lawrence
#Finished on 12/11/2022
#Purpose: THis program contains the logic needed for a client to send/receive messages to a server. It slightly manages the game loop by deciding what type of message is received
#based on codes sent from the server. This file will Disconnect if told to through DC code, If code is server (SVR) then it will look for 1 of 3 codes being:
#NM = Name request, TXT = Receive TXT message from server, or GM = game content request from server. Depending on the code the client will send their answers or name to the server
#While receiving messages to display to client, so the client can understand what is happening in the game loop
import socket
import select
import netmsg
import time
#-----------Message codes for receiving----------#
DISCONNECT_MSG = "DC"
GAME_MSG = "GM"
SERVER_MSG = "SVR"
TEXT_MSG = "TXT"
GAMEOVER_MSG = "GO"
WIN_MSG = "WIN"
NXTROUND_MSG = "NXT"
NAMERQST_MSG = "NM"
#------------------------------------------------#

#clientGameLoop: This function takes in an IP and port to connect to
				   # First the function connects to a socket and returns that socket for use
				   # It uses the three way handshake to confirm the connection
				   # It will loop listening for messages from the server.
				   # The "game loop" is managed by the server so the client only has simple logic
				   # that decodes the message received, and will only send answer if the server prompts with NXT msg
				   # The client will receive a disconnect message that will break the loop if the game ended or an error occured
def clientGameLoop(IP, PORT):

	#If the IP is empty then it means that the client selected to join a LAN match
	if IP == "":
		IP = socket.gethostname() #Set IP to LAN host machine
		PORT = 1111 #Match port to the port used by server to open socket
		
	client, connected = netmsg.sonnect_to_socket(IP, PORT) #Connect to a socket, and store the connected socket, and a bool that determines if the socket was connected successfully
	if connected == False: #If it could not connect return out of function
		time.sleep(2)
		return
	
	print("Connected to server. Loading lobby...") #Connection successful
	netmsg.send_to_one(client, "Connected")		   #Send first syn in three way handshake to server

	#Loop while bool is true
	isPlaying = True
	while isPlaying:

		#Try to send and receive messages from and to server
		try:
			sockets_list = [client] #Array that stores all the sockets (Will only need the client socket thats connected)
			read_sockets,[], [] = select.select(sockets_list,[],[]) #Select sockets in list that have information
			
			#For each socket in the sockets with information (So if the server has sent any information to the client)
			for currentSocket in read_sockets: 
				if currentSocket == client: #If socket is correct socket
					
					encoded_message = netmsg.receive_message(currentSocket) #Receive a coded message from the server (current socket)
					
					if encoded_message == "error": #If the message received is an error, then an error occured when trying to receive the message (an exception is thrown in order to return error)
						print("An error occured, disconnecting...") #Display error msg and then close the socket
						time.sleep(3)
						client.close()
						break #End the program by breaking the loop

					code = encoded_message.split(" ") #This splits off all of the codes into an array of strings
													  #The first word in the message will always be the message type code
													  #If the message starts with SVR then the following 1 or two words will also be codes
					
					#If the first code is "DC" then disconnect the client (this is like a fin message)
					if DISCONNECT_MSG in code:
						#Set loop condition to false
						isPlaying = False
						#------------------------------------------#
						#These sets of messages get the message without any possible codes
						#Remove all codes because possible that an error will occur and received messages will merge
						#This cleans up the output
						m1 = encoded_message.replace(SERVER_MSG,'')  #replace the codes:
						m2 = m1.replace(GAME_MSG,'') 
						m3 = m2.replace(TEXT_MSG,'') 
						m4 = m3.replace(NAMERQST_MSG,'') 
						m5 = m4.replace(DISCONNECT_MSG,'') 
						print(m5) #Print message without codes
						time.sleep(5)
						client.close()#Close connection

						#If the first code is "SVR" then a message from the server has been received and needs further clarification
					elif code[0] == SERVER_MSG:
							#If the second code (Because first code was svr it means there is 1 or two more codes) is a game msg (GM) then it means the server is asking for an answer
							#This message will contain all of the graph information needed to determine the distance between two nodes. 
							if code[1] == GAME_MSG:
								#Clear codes out of message
								m1 = encoded_message.replace(code[0],'')
								m2 = m1.replace(code[1],'')
								#Display graph, and desired route to find
								#Ask for user input
								print(m2)
								pathDist = input("			>", ) #This is the users answer for the length of shortest path
								
								success = netmsg.send_to_one(client, pathDist) #Will try to send and will have a success message
								if success == False: 						   #Success is checked in case that the server ran into an error and closed all the connections before the client tried sending
													 						   #This will ensure that the client stops running the game loop if it failed
									print("An error occured, disconnecting...")
									time.sleep(3)
									client.close() #Close client and break loop
									break
							
							#If the code is TXT then the server simply wants to display this information to client
							elif code[1] == TEXT_MSG: 
								#Replace codes for clean output
								m1 = encoded_message.replace(code[0],'')
								m2 = m1.replace(code[1],'')
								print(m2) #Display received message
							#If the code is NM then the server is requesting a username from the client
							elif code[1] == NAMERQST_MSG:
								#Replace codes for clean output to prompt player for name
								m1 = encoded_message.replace(code[0],'')
								m2 = m1.replace(code[1],'')
								print(m2) #Display request
								
								#Get the users name
								name = ""
								while name == "": #Loop until the user enters valid input
									temp = (input("      > "))
									#If the user entered a name that conflicts with any of the message code, prompt them to choose a different name
									if temp == SERVER_MSG or temp == GAME_MSG or temp == TEXT_MSG or temp == NAMERQST_MSG or temp == DISCONNECT_MSG:
										name = "" #"" for looping purpose
										print("entered invalid name. Please re-enter")
									else: #If the name is valid then assign name
										name = temp
								
								success = netmsg.send_to_one(client, name) 	   #Will try to send and will have a success message
								if success == False: 						   #Success is checked in case that the server ran into an error and closed all the connections before the client tried sending
													 						   #This will ensure that the client stops running the game loop if it failed
									print("An error occured, disconnecting...")
									time.sleep(3)
									client.close() #Close client and break loop
									break
					
		except: #If an error occured during this loop (Could not send/receive from server, server suddenly disconnected)
			print("An error occured, disconnecting...") #Display error
			time.sleep(3)
			client.close() #Close socket
			break #Break out of loop and return to a different game state





   