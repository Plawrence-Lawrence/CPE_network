
#Author: Pearson Lawrence
#Finished on 12/10/2022
#This file stores the definitions of functions needed to create a state machine
#The state machine is used to manage the "UI" and decide when to quit the game
import os
import clientStates
import serverStates

#----------------------State machine definitions------------------------#
#-------See the def of the state machine to see implementation----------#
LAUNCHSTATE = 0
STARTSTATE = 1
QUITSTATE = 2
CREATESTATE = 3
JOINSTATE = 4
SERVERRUNSTATE = 5
CLIENTRUNSTATE = 6
LOBBYOPTIONSSTATE = 7
EXITSTATE = 8
#------------------------------------------#

#LaunchState: sends the user to main menu or exits
#This function 
# 1.) displays options to the user
# 3.) Gets the option the user selected
# 4.) returns the state the user selected
def launchState():
    #Print launch menu
    print("|---------------------|")
    print("|   - Welcome To -    |")
    print("|   | QuickRoute |    |")
    print("|                     |")
    print("|        Enter        |")
    print("|  Start(1)  Quit(2)  |")
    print("|                     |")
    Choice = input("         > ")    #Gets desired state change
    print("|---------------------|")
    print("                      ")
    if Choice == '1':
        return STARTSTATE #Move to main menu if 1
    elif Choice == '2':
        return QUITSTATE  #Move to quit menu if 2
    return LAUNCHSTATE    #Safguard: if invalid input then it will reloop

#startState: sends the user to Host a game, Join a game, or quit
#This function 
# 1.) displays options to the user
# 3.) Gets the option the user selected
# 4.) returns the state the user selected
def startState():
    #Print main menu display
    print("|-------------------------------|")
    print("|                               |")
    print("|           QuickRoute          |")
    print("|                               |")
    print("|              Enter            |")
    print("|  Host Game (1)   Join Game(2) |")
    print("|             Quit(3)           |")
    print("|                               |")
    Choice = input("               > ")        #Get state choice
    print("|-------------------------------|")
    print("                               ")
    if Choice == '1':
        return CREATESTATE #If 1 then player wants to host a game
    elif Choice == '2':
        return JOINSTATE   #if 2 then player wants to join a game
    elif Choice == '3':
        return QUITSTATE   #if 3 then user wants to quit the program
    return STARTSTATE      #Safeguard: If invalid option, it will re-loop

#createState: User decides if they want to launvh the server or modify the game options (player count and max score)
            # Allows user to return to the start state or quit state
#This function 
# 1.) displays options to the user
# 3.) Gets the option the user selected
# 4.) returns the state the user selected
def createState():
    #print the host options menu
    print("|-----------------------------------------|")
    print("|                                         |")
    print("|              QuickRoute                 |")
    print("|             Creating Game               |")
    print("|                                         |")
    print("|   Note: Host does not count as player   |")
    print("|                                         |")
    print("|        Start(1)   Lobby Options(2)      |")
    print("|         Back(3)       Quit(4)           |")
    print("|                                         |")
    Choice = input("                   > ") 
    print("|-----------------------------------------|")
    if Choice == '1':
        return SERVERRUNSTATE       #If 1 then launch server
    elif Choice == '2':
        return LOBBYOPTIONSSTATE    #If 2 then modify lobby game options
    elif Choice == '3':
        return STARTSTATE           #If 3 then go back to the main menu
    elif Choice == '4':
        return QUITSTATE            #If 4 then go to quit menu
    return CREATESTATE

#lobbyOptionsState: User decides if they want to modify game options (players/score), go back to create state with lobby options selected
                    # If the user selects to modify the options, it prompts the user with max players and max score
                    # If no options are changed then it goes back to create state with passed in values
#This function 
# 1.) displays options to the user
# 3.) Gets the option the user selected
# 4.) If user selected to modify then prompt user to enter players then score
# 5.) returns the state the user selected, as well as the new options if changed, if not then options passed in
def lobbyOptionsState(currentPlayers, currentScore):
    #Print the options menu
    print("|----------------------------------|")
    print("|                                  |")
    print("|           QuickRoute             |")
    print("|          Lobby Options           |")
    print("|                                  |")
    print("|    Set Options(1)  Back(2)       |")
    print("|             Quit(3)              |")
    print("|                                  |")
    Choice = input("                > ")          #Get initial input
    print("|----------------------------------|")
    print("                               ")
    if Choice == '1':   #if 1 then user wants to modify options

        #Clear the last UI          
        os.system('cls' if os.name == 'nt' else 'clear')
        # print new UI that first asks for desired players      
        print("|----------------------------------|")
        print("|                                  |")
        print("|           QuickRoute             |")
        print("|                                  |")
        print("|         Players (2-10):          |")
        playercount = input("                > ") 
        print("|         Score Limit (1+):        |") #Ask player for max score
        scorelim = input("                > ") 
        print("                               ")

        #Casts the strings passed in to ints for game logic
        pcr = int(playercount) 
        scr = int(scorelim)

        return LOBBYOPTIONSSTATE, pcr, scr  #Returns to the first options menu with new values
    elif Choice == '2': #If 2 then user wants to go back to the host lobby with the options passed in
                        #Note: That if the user modified the options then the items passed in can be the new values player chose
        os.system('cls' if os.name == 'nt' else 'clear')
        return CREATESTATE, currentPlayers, currentScore
    elif Choice == '3': #If 3 user wants to quit game, send to quit menu
        return QUITSTATE, 0, 0

    return LOBBYOPTIONSSTATE, currentPlayers, currentScore #If invalid input re loop with the values passed in

#joinState: User decides if they want to join a game on LAN or on a remote host IP
            #Note: If the user wants to join remote IP the remote host must use port forwarding to allow connections
            #Also decides if they want to return to main menu or quit game
#This function 
# 1.) displays options to the user
# 3.) Gets the option the user selected
# 4.) If user selected to join remote IP then prompt user for IP and Port
# 5.) returns the state the user selected, as well as the IP and port
#Note: If the Lan was launched then the IP returned will "" for IP and -1 for PORT because it will connect to a local host manually
def joinState():
    #Print Join options
    print("|----------------------------------|")
    print("|                                  |")
    print("|           QuickRoute             |")
    print("|           Join Lobby             |")
    print("|                                  |")
    print("|        LAN(1)  Remote IP(2)      |")
    print("|        Back(3)   Quit(4)         |")
    print("|                                  |")
    Choice = input("                > ") 
    print("|----------------------------------|")
    print("                               ")
    if Choice == '1':                   #If 1 then user wants to connect to a LAN
        return CLIENTRUNSTATE, "", -1   # returns "" and -1 because local host connection will be done automatically
                                        #When IP is ""
    elif Choice == '2': #If 2 then user wants to connect to remote host. Note: Remote host must allow port connections (port forwarding)
        #Clear last menu
        os.system('cls' if os.name == 'nt' else 'clear') #cls for windows, clear for linux
        #print menu to prompt user to enter desired Ip then Port 
        print("|----------------------------------|")
        print("|                                  |")
        print("|           QuickRoute             |")
        print("|           Join Lobby             |")
        print("|                                  |")
        print("|           IP Address:            |")
        ipa = input("                > ") 
        print("|              Port:               |")
        port = input("               > ") 
        print("|----------------------------------|")
        print("                               ")
        return CLIENTRUNSTATE, ipa, port #Returns the IP and port out and then send the state to launch client
    elif Choice == '3':
        return STARTSTATE   #Do not have to return IP or port here, user wants to send to main menu
    elif Choice == '4':
        return QUITSTATE    #Do not have to return IP or port here, user wants to send to Quit
    
    return JOINSTATE #Invalid input then re-loop

#QuitState: This function prints a goodby message before telling state machine to exit
#This function 
# 1.) displays goodbye message
# 2.) Sends to exit state through return
def quitState():
    #Clear the terminal to print goodbye message
    os.system('cls' if os.name == 'nt' else 'clear')
    #print goodbye
    print("|-------------------------------|")
    print("|                               |")
    print("|           QuickRoute          |")
    print("|      Is Sad to see you go     |")
    print("|                               |")
    print("|-------------------------------|")
    
    return EXITSTATE #Send to exit state closing down the state machine and ending the program
    
#QuitState: This function prints a goodby message before telling state machine to exit
#This function 
# 1.) displays goodbye message
# 2.) Sends to exit state through return
def serverRunState(players, score): 
    
    return CREATESTATE
def clientRunState(ip, port):
    clientStates.clientStateMachine(ip, port)
    return JOINSTATE

#This is the actual state machine, it takes in the next state it is supposed to run, Max Players, and Max Score
def stateMachine(state, p, s):
    os.system('cls' if os.name == 'nt' else 'clear')    #Clears terminal each loop to ensure it stays clean
    players = p          #Is set to max players passed in. Is updated each loop because it can be modified in LOBBYOPTIONSSTATE
    score = s            #Is set to max players passed in. Is updated each loop because it can be modified in LOBBYOPTIONSSTATE
    returnState = state  #Sets the current return state to the state passed in
                         #Note: State gets modified by what is returned out of the function for state machine functionality
    ip = ""              #Note: If IP remains "" it will eventually be set to LAN
    port = 0             #Note: If IP remains "" port will be set to 111
    
    #Actual state machine
    #Each state sets the return state which will be ran on next time this is looped
    if state == LAUNCHSTATE:#-------------->Launch state is the first state to be called. Opens start "screen"
        returnState = launchState()

    elif state == STARTSTATE:#-------------->Start state is the second state that comes after launch state
                                            #It allows the user to select if they want to host or join a match
        returnState = startState()

    elif state == CREATESTATE:#------------->Create state is the resulting state if host is selected
                                            #Allows user to choose if they want to modify default options (max players/score)
                                            #And allows user to start a server
        returnState = createState()

    elif state == LOBBYOPTIONSSTATE:#------>Lobby Options State allows the palyer to set desired max players/score
        returnState, players, score = lobbyOptionsState(players, score) #returns the desired players/score

    elif state == SERVERRUNSTATE:#--------->The server run state is responsible for starting the server
                                           #And running all of the game logic needed to create a functional game
        serverStates.runServerStateMachine(players, score) #Note runServerStateMachine is a state machine so it will only need to be called once
        returnState = CREATESTATE      #Hence serverRunState does not return a state so set state back to Create State menu
        
    elif state == CLIENTRUNSTATE:#--------->Client Run State connects the client to the server and receives messages from server
        clientStates.clientGameLoop(ip, port)    #clientGameLoop Not much game logic is done other than getting simple input to send to server
        returnState = STARTSTATE                 #As this function also is only ran once and loops inside it does not return a state
                                                 #Therefore after clientrunstate is over it means the game is over and the client is sent back to main menu

    elif state == JOINSTATE:#-------------->Join state is responsible for getting the ip and port that player wants to connect to
        returnState, ip, port = joinState()

    elif state == QUITSTATE:#-------------->Quit State is responsible for displaying a closing message before sending to exit state
        returnState = quitState()

    elif state == EXITSTATE:#-------------->Exit state simply sets return state to exit state which is meant to stop the state machine
        returnState = EXITSTATE

    return returnState, players, score #return next state to run, and updated Max player and max score if they were modified

