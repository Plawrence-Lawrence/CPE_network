
import os
import clientStates
import serverStates
import socket
LAUNCHSTATE = 0
STARTSTATE = 1
QUITSTATE = 2
CREATESTATE = 3
JOINSTATE = 4
SERVERRUNSTATE = 5
CLIENTRUNSTATE = 6
LOBBYOPTIONSSTATE = 7
EXITSTATE = 8

def launchState():
    print("|---------------------|")
    print("|   - Welcome To -    |")
    print("|   | QuickRoute |    |")
    print("|                     |")
    print("|        Enter        |")
    print("|  Start(1)  Quit(2)  |")
    print("|                     |")
    Choice = input("         > ")
    print("|---------------------|")
    print("                      ")
    if Choice == '1':
        return STARTSTATE
    elif Choice == '2':
        return QUITSTATE
    #os.system('cls' if os.name == 'nt' else 'clear')

    return LAUNCHSTATE

def startState():
    print("|-------------------------------|")
    print("|                               |")
    print("|           QuickRoute          |")
    print("|                               |")
    print("|              Enter            |")
    print("|  Host Game (1)   Join Game(2) |")
    print("|             Quit(3)           |")
    print("|                               |")
    Choice = input("               > ") 
    print("|-------------------------------|")
    print("                               ")
    if Choice == '1':
        return CREATESTATE
    elif Choice == '2':
        return JOINSTATE
    elif Choice == '3':
        return QUITSTATE
       
    #os.system('cls' if os.name == 'nt' else 'clear')
    return STARTSTATE

def createState():
    print("|-----------------------------------------|")
    print("|                                         |")
    print("|              QuickRoute                 |")
    print("|             Creating Game               |")
    print("|                                         |")
    print("|   Note: Host does not count as player   |")
    print("|                                         |")
    print("|        Start(1)   Lobby Options(2)      |")
    print("|         Back(3)       Quit(3)           |")
    print("|                                         |")
    Choice = input("                   > ") 
    print("|-----------------------------------------|")
    if Choice == '1':
        return SERVERRUNSTATE
    elif Choice == '2':
        return LOBBYOPTIONSSTATE
    elif Choice == '3':
        return STARTSTATE
    elif Choice == '4':
        return QUITSTATE
    return CREATESTATE

def lobbyOptionsState(currentPlayers, currentScore):
    print("|----------------------------------|")
    print("|                                  |")
    print("|           QuickRoute             |")
    print("|          Lobby Options           |")
    print("|                                  |")
    print("|    Set Options(1)  Back(2)       |")
    print("|             Quit(3)              |")
    print("|                                  |")
    Choice = input("                > ") 
    print("|----------------------------------|")
    print("                               ")
    if Choice == '1':
        os.system('cls' if os.name == 'nt' else 'clear')
        print("|----------------------------------|")
        print("|                                  |")
        print("|           QuickRoute             |")
        print("|                                  |")
        print("|         Players (2-10):          |")
        playercount = input("                > ") 
        print("|         Score Limit (1+):        |")
        scorelim = input("                > ") 
        print("                               ")
        pcr = int(playercount)
        scr = int(scorelim)
        return LOBBYOPTIONSSTATE, pcr, scr
    elif Choice == '2':
        os.system('cls' if os.name == 'nt' else 'clear')
        return CREATESTATE, currentPlayers, currentScore
    elif Choice == '3':
        return QUITSTATE, 0, 0
    
    return LOBBYOPTIONSSTATE, currentPlayers, currentScore

def joinState():

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
    if Choice == '1':
        return CLIENTRUNSTATE, "F", -1
    elif Choice == '2':
        os.system('cls' if os.name == 'nt' else 'clear')
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
        return CLIENTRUNSTATE, ipa, port
    elif Choice == '3':
        return STARTSTATE
    elif Choice == '4':
        return QUITSTATE
    
    return JOINSTATE

def quitState():
    

    os.system('cls' if os.name == 'nt' else 'clear')
    print("|-------------------------------|")
    print("|                               |")
    print("|           QuickRoute          |")
    print("|      Is Sad to see you go     |")
    print("|                               |")
    print("|-------------------------------|")
    
    return EXITSTATE
def serverRunState(players, score):
    serverStates.runServerStateMachine(players, score)
    return CREATESTATE
def clientRunState(ip, port):
    clientStates.clientStateMachine(ip, port)
    return JOINSTATE

def stateMachine(state, p, s, r):
    os.system('cls' if os.name == 'nt' else 'clear')
    players = p
    score = s
    returnState = state
    isRunning = r
    ip = ""
    port = 0
    if state == LAUNCHSTATE:
        returnState = launchState()
    elif state == STARTSTATE:
        returnState = startState()
    elif state == CREATESTATE:
        returnState = createState()
    elif state == LOBBYOPTIONSSTATE:
        returnState, players, score = lobbyOptionsState(players, score)
    elif state == SERVERRUNSTATE:
        returnState = serverRunState(players, score)
        returnState = CREATESTATE
    elif state == CLIENTRUNSTATE:
        clientRunState(ip, port)
        returnState = STARTSTATE
    elif state == JOINSTATE:
        returnState, ip, port = joinState()
    elif state == QUITSTATE:
        returnState = quitState()
    elif state == EXITSTATE:
        returnState = EXITSTATE

    return returnState, players, score, isRunning

